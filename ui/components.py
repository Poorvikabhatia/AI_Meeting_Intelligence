"""
UI Components for Streamlit
"""

import streamlit as st
from typing import List, Dict


def render_header():
    """Render application header"""
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #00D9FF; font-size: 2.5em;">🚀 AI Meeting Intelligence System</h1>
        <h3 style="color: #4ECDC4;">⚡ Powered by Groq (LLaMA 3)</h3>
        <hr style="border-top: 3px solid #00D9FF;">
    </div>
    """, unsafe_allow_html=True)


def render_how_it_works():
    """Render 'How it Works' section"""
    with st.expander("📖 How It Works", expanded=False):
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("""
            <div style="text-align: center;">
                <h4>📝</h4>
                <p style="font-size: 0.8em;"><strong>Input</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='text-align: center; font-size: 1.5em;'>→</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center;">
                <h4>🤖</h4>
                <p style="font-size: 0.8em;"><strong>Agents</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("<div style='text-align: center; font-size: 1.5em;'>→</div>", unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div style="text-align: center;">
                <h4>✅</h4>
                <p style="font-size: 0.8em;"><strong>Output</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        **Process Flow:**
        1. **Understanding Agent** - Analyzes transcript using Groq LLM
        2. **Task Agent** - Stores extracted tasks
        3. **Tracking Agent** - Calculates metrics
        4. **Escalation Agent** - Monitors deadlines
        5. **Audit Agent** - Logs all activities
        """)


def render_status_badge(status: str) -> str:
    """Render colored status badge"""
    badges = {
        "Completed": "🟢 Completed",
        "Pending": "🟡 Pending",
        "Delayed": "🔴 Delayed"
    }
    return badges.get(status, status)


def render_priority_badge(priority: str) -> str:
    """Render priority badge with color"""
    if priority == "High":
        return "🔴 High"
    elif priority == "Medium":
        return "🟡 Medium"
    elif priority == "Low":
        return "🟢 Low"
    return priority


def render_task_card(task: Dict, index: int = 0):
    """Render a single task as a card"""
    status_badge = render_status_badge(task.get("status", "Pending"))
    priority_badge = render_priority_badge(task.get("priority", "Medium"))
    
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### 📋 {task.get('task', 'Untitled Task')}")
            
            col_owner, col_deadline = st.columns(2)
            with col_owner:
                st.markdown(f"**👤 Owner:** {task.get('owner', 'Unassigned')}")
            with col_deadline:
                st.markdown(f"**📅 Deadline:** {task.get('deadline', 'Not specified')}")
        
        with col2:
            st.markdown(f"{priority_badge}")
        
        col_status, col_created = st.columns(2)
        with col_status:
            st.markdown(f"**Status:** {status_badge}")
        with col_created:
            st.markdown(f"**Created:** {task.get('created_at', '')[:10]}")


def render_metrics(metrics: Dict):
    """Render metrics dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Tasks", metrics.get("total", 0))
    
    with col2:
        st.metric("✅ Completed", metrics.get("completed", 0))
    
    with col3:
        st.metric("⏳ Pending", metrics.get("pending", 0))
    
    with col4:
        st.metric("⚠️ Delayed", metrics.get("delayed", 0))


def render_alert(message: str, alert_type: str = "info"):
    """Render alert message"""
    if alert_type == "success":
        st.success(message)
    elif alert_type == "error":
        st.error(message)
    elif alert_type == "warning":
        st.warning(message)
    else:
        st.info(message)


def render_loading_spinner(message: str = "Processing..."):
    """Render loading spinner"""
    with st.spinner(message):
        return True


def create_task_table(tasks: List[Dict]):
    """Create a table view of tasks"""
    import pandas as pd
    
    data = []
    for task in tasks:
        data.append({
            "Task": task.get("task", ""),
            "Owner": task.get("owner", ""),
            "Deadline": task.get("deadline", ""),
            "Priority": task.get("priority", ""),
            "Status": task.get("status", "")
        })
    
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No tasks to display")


def render_sidebar_nav():
    """Render sidebar navigation"""
    st.sidebar.markdown("### 📌 Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["🏠 Home", "📊 Dashboard", "📋 Task Manager", "📜 Audit Logs"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    return page


def render_input_section():
    """Render input section for meeting transcript"""
    st.subheader("📝 Input Meeting Transcript")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        transcript = st.text_area(
            "Paste your meeting transcript here:",
            height=200,
            placeholder="E.g., Rahul will prepare the sales report by Friday. Priya will finalize the presentation by tomorrow..."
        )
    
    with col2:
        st.markdown("### 🎯 Actions")
        
        generate_btn = st.button("🚀 Generate Tasks", use_container_width=True, type="primary")
        
        demo_btn = st.button("📚 Load Demo Data", use_container_width=True)
        
        clear_btn = st.button("🗑️ Clear All Tasks", use_container_width=True)
    
    return transcript, generate_btn, demo_btn, clear_btn
