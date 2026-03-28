"""
AI Meeting Intelligence System - Main Streamlit Application
"""

import streamlit as st
import json
from datetime import datetime, timedelta

# Import agents
from agents.understanding_agent import UnderstandingAgent
from agents.task_agent import TaskAgent
from agents.tracking_agent import TrackingAgent
from agents.escalation_agent import EscalationAgent
from agents.audit_agent import AuditAgent

# Import UI components
from ui.components import (
    render_header,
    render_how_it_works,
    render_input_section,
    render_metrics,
    render_task_card,
    render_status_badge,
    render_priority_badge,
    render_alert,
    render_sidebar_nav,
    create_task_table
)

# Import helpers
from utils.helpers import load_tasks, save_tasks, add_log

# Page configuration
st.set_page_config(
    page_title="AI Meeting Intelligence System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-container {
        background: linear-gradient(135deg, #00D9FF 0%, #4ECDC4 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .task-card {
        border: 2px solid #00D9FF;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f0f9ff;
    }
    .alert-box {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .alert-success {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

if "transcript" not in st.session_state:
    st.session_state.transcript = ""


# Initialize agents
@st.cache_resource
def init_agents():
    return {
        "understanding": UnderstandingAgent(),
        "task": TaskAgent(),
        "tracking": TrackingAgent(),
        "escalation": EscalationAgent(),
        "audit": AuditAgent()
    }


agents = init_agents()


def load_demo_data():
    """Load demo transcript"""
    try:
        with open("assets/demo_data.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Demo data not found. Please check assets/demo_data.txt"


def process_transcript(transcript: str):
    """Process meeting transcript through all agents"""
    if not transcript or not transcript.strip():
        render_alert("Please enter a meeting transcript", "error")
        return
    
    with st.spinner("🤖 Processing meeting transcript..."):
        # Step 1: Understanding Agent
        add_log("Main App", "Started processing transcript")
        render_alert("Step 1/5: Analyzing transcript with AI...", "info")
        
        tasks = agents["understanding"].process_transcript(transcript)
        
        if not tasks:
            render_alert("No tasks extracted from transcript. Please try again.", "warning")
            add_log("Main App", "No tasks extracted")
            return
        
        # Step 2: Task Agent
        render_alert(f"Step 2/5: Storing {len(tasks)} tasks...", "info")
        agents["task"].store_tasks(tasks)
        
        # Step 3: Tracking Agent
        render_alert("Step 3/5: Calculating metrics...", "info")
        metrics = agents["tracking"].calculate_metrics()
        
        # Step 4: Escalation Agent
        render_alert("Step 4/5: Checking deadlines...", "info")
        escalation_result = agents["escalation"].check_deadlines()
        
        if escalation_result["escalated_count"] > 0:
            render_alert(
                f"⚠️ {escalation_result['escalated_count']} task(s) marked as delayed",
                "warning"
            )
        
        # Step 5: Audit Agent
        render_alert("Step 5/5: Recording in audit log...", "info")
        add_log("Main App", f"Successfully processed {len(tasks)} tasks")
        
        render_alert(f"✅ Successfully processed {len(tasks)} tasks!", "success")
        st.rerun()


def home_page():
    """Render home page"""
    render_header()
    render_how_it_works()
    
    st.markdown("---")
    
    # Input section
    transcript, generate_btn, demo_btn, clear_btn = render_input_section()
    
    # Handle button clicks
    if demo_btn:
        st.session_state.transcript = load_demo_data()
        render_alert("✅ Demo data loaded!", "success")
        st.rerun()
    
    if generate_btn:
        process_transcript(transcript)
    
    if clear_btn:
        if st.confirm("Are you sure you want to clear all tasks?"):
            save_tasks([])
            render_alert("✅ All tasks cleared!", "success")
            add_log("Main App", "Cleared all tasks")
            st.rerun()
    
    # Show current tasks count
    current_tasks = load_tasks()
    if current_tasks:
        st.markdown("---")
        st.subheader(f"📊 Current Tasks: {len(current_tasks)}")
        
        # Quick preview
        col1, col2, col3 = st.columns(3)
        
        pending = len([t for t in current_tasks if t.get("status") == "Pending"])
        completed = len([t for t in current_tasks if t.get("status") == "Completed"])
        delayed = len([t for t in current_tasks if t.get("status") == "Delayed"])
        
        with col1:
            st.metric("🟡 Pending", pending)
        with col2:
            st.metric("✅ Completed", completed)
        with col3:
            st.metric("🔴 Delayed", delayed)


def dashboard_page():
    """Render dashboard page"""
    st.header("📊 Dashboard")
    
    metrics = agents["tracking"].calculate_metrics()
    render_metrics(metrics)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Task Status Distribution")
        status_data = {
            "Completed": metrics["completed"],
            "Pending": metrics["pending"],
            "Delayed": metrics["delayed"]
        }
        st.bar_chart(status_data)
    
    with col2:
        st.subheader("Priority Distribution")
        distribution = agents["tracking"].get_task_distribution()
        priority_data = distribution["by_priority"]
        st.bar_chart(priority_data)
    
    st.markdown("---")
    
    # Owner breakdown
    st.subheader("Tasks by Owner")
    owner_data = distribution["by_owner"]
    if owner_data:
        st.bar_chart(owner_data)
    else:
        st.info("No owner data to display")
    
    # Escalation alerts
    st.markdown("---")
    st.subheader("⚠️ Escalation Alerts")
    
    urgent_tasks = agents["escalation"].get_urgent_tasks()
    if urgent_tasks:
        for task in urgent_tasks:
            alert_msg = agents["escalation"].generate_escalation_alert(task)
            render_alert(alert_msg, "warning")
    else:
        st.info("✅ No escalation alerts")


def task_manager_page():
    """Render task manager page"""
    st.header("📋 Task Manager")
    
    tasks = load_tasks()
    
    if not tasks:
        st.info("No tasks yet. Go to Home and generate some tasks!")
        return
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        owner_filter = st.multiselect(
            "Filter by Owner:",
            options=list(set([t.get("owner", "Unassigned") for t in tasks])),
            default=None
        )
    
    with col2:
        status_filter = st.multiselect(
            "Filter by Status:",
            options=["Pending", "Completed", "Delayed"],
            default=None
        )
    
    # Apply filters
    filtered_tasks = tasks
    
    if owner_filter:
        filtered_tasks = [t for t in filtered_tasks if t.get("owner") in owner_filter]
    
    if status_filter:
        filtered_tasks = [t for t in filtered_tasks if t.get("status") in status_filter]
    
    st.markdown(f"### Showing {len(filtered_tasks)} of {len(tasks)} tasks")
    
    st.markdown("---")
    
    # Display tasks as cards
    for idx, task in enumerate(filtered_tasks):
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"### 📋 {task.get('task', 'Untitled')}")
                st.markdown(f"👤 **Owner:** {task.get('owner', 'Unassigned')}")
                st.markdown(f"📅 **Deadline:** {task.get('deadline', 'Not specified')}")
            
            with col2:
                st.markdown(f"**Priority:** {render_priority_badge(task.get('priority', 'Medium'))}")
                st.markdown(f"**Status:** {render_status_badge(task.get('status', 'Pending'))}")
            
            with col3:
                # Toggle status
                new_status = st.selectbox(
                    "Change Status:",
                    options=["Pending", "Completed", "Delayed"],
                    index=["Pending", "Completed", "Delayed"].index(task.get("status", "Pending")),
                    key=f"status_{idx}"
                )
                
                if new_status != task.get("status"):
                    agents["task"].update_task_status(task.get("task"), new_status)
                    render_alert(f"✅ Task status updated to {new_status}", "success")
                    st.rerun()
                
                if st.button("🗑️ Delete", key=f"delete_{idx}"):
                    agents["task"].delete_task(task.get("task"))
                    render_alert("✅ Task deleted", "success")
                    st.rerun()
            
            st.caption(f"Created: {task.get('created_at', 'Unknown')[:19]}")


def audit_logs_page():
    """Render audit logs page"""
    st.header("📜 Audit Logs")
    
    logs = agents["audit"].get_all_logs()
    
    if not logs:
        st.info("No audit logs yet")
        return
    
    # Log summary
    summary = agents["audit"].get_log_summary()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total Logs", summary["total_logs"])
    
    with col2:
        agents_count = len(summary["agents"])
        st.metric("🤖 Agents", agents_count)
    
    with col3:
        st.metric("⏱️ Latest Entry", "Available" if logs else "None")
    
    st.markdown("---")
    
    # Logs table
    st.subheader("Recent Audit Activities")
    
    import pandas as pd
    
    log_data = []
    for log in logs[-50:]:  # Show last 50 logs
        log_data.append({
            "Timestamp": log.get("timestamp", "")[:19],
            "Agent": log.get("agent", ""),
            "Action": log.get("action", "")
        })
    
    df = pd.DataFrame(log_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Export button
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Logs (JSON)"):
            json_export = agents["audit"].export_logs("json")
            st.download_button(
                label="Download JSON",
                data=json_export,
                file_name=f"audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📥 Export Logs (CSV)"):
            csv_export = agents["audit"].export_logs("csv")
            st.download_button(
                label="Download CSV",
                data=csv_export,
                file_name=f"audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )


def main():
    """Main application"""
    # Sidebar navigation
    st.session_state.current_page = render_sidebar_nav()
    
    # Page routing
    if st.session_state.current_page == "🏠 Home":
        home_page()
    elif st.session_state.current_page == "📊 Dashboard":
        dashboard_page()
    elif st.session_state.current_page == "📋 Task Manager":
        task_manager_page()
    elif st.session_state.current_page == "📜 Audit Logs":
        audit_logs_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.8em; padding: 20px;">
        <p>🚀 AI Meeting Intelligence System | Built with Streamlit & Groq API | © 2026</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
