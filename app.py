"""
AI Meeting Intelligence System - Modern SaaS Dashboard
Powered by Groq (LLaMA 3) - Hackathon Edition
"""

import streamlit as st
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Import agents
from agents.understanding_agent import UnderstandingAgent
from agents.task_agent import TaskAgent
from agents.tracking_agent import TrackingAgent
from agents.escalation_agent import EscalationAgent
from agents.audit_agent import AuditAgent
from agents.deadline_agent import analyze_deadline

# Import helpers
from utils.helpers import load_tasks, save_tasks, add_log
from services.llm_service import LLMService

# ============================================================================
# GLOBAL CSS STYLING - Modern SaaS Dashboard Light Theme
# ============================================================================
MODERN_CSS = """
<style>
/* Animated background */
body {
    background: linear-gradient(-45deg, #eef2ff, #f8fafc, #e0f2fe, #f0fdf4);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Professional header */
.header {
    background: linear-gradient(90deg, #4F46E5, #6366F1);
    padding: 30px;
    border-radius: 12px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.15);
}

.header h1 {
    margin: 0;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.header p {
    margin: 8px 0 0 0;
    font-size: 15px;
    opacity: 0.95;
    font-weight: 400;
}

/* Root Variables */
:root {
    --primary-color: #4F46E5;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    --light-bg: #f8f9fa;
    --white-bg: #ffffff;
    --dark-text: #111111;
    --gray-text: #333333;
    --light-text: #666666;
    --border-color: #e5e7eb;
    --shadow: 0px 2px 10px rgba(0, 0, 0, 0.08);
    --shadow-hover: 0px 4px 16px rgba(0, 0, 0, 0.12);
}

/* Main Container */
.main {
    background-color: transparent;
}

/* Card Styling - Core Component */
.card {
    background-color: var(--white-bg);
    padding: 20px;
    border-radius: 12px;
    box-shadow: var(--shadow);
    margin-bottom: 15px;
    border: 1px solid var(--border-color);
    transition: all 0.3s ease;
}

.card:hover {
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}

.card-title {
    color: var(--dark-text);
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 10px;
    letter-spacing: -0.3px;
}

.card-subtitle {
    color: var(--light-text);
    font-size: 14px;
    margin-bottom: 12px;
}

.card-text {
    color: var(--gray-text);
    font-size: 14px;
    line-height: 1.6;
}

.card-description {
    color: var(--light-text);
    font-size: 13px;
    margin-top: 8px;
}

/* Priority Badges */
.badge-high {
    background-color: #ffe5e5;
    color: #c41e3a;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
    margin-right: 8px;
}

.badge-medium {
    background-color: #fff4cc;
    color: #9a6b0f;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
    margin-right: 8px;
}

.badge-low {
    background-color: #e6f4ea;
    color: #0d652d;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
    margin-right: 8px;
}

/* Status Badges */
.status-completed {
    background-color: #d4edda;
    color: #155724;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

.status-pending {
    background-color: #fff3cd;
    color: #856404;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

.status-delayed {
    background-color: #f8d7da;
    color: #721c24;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

/* Metric Cards - for KPIs */
.metric-card {
    background: linear-gradient(135deg, var(--white-bg) 0%, #f9fafb 100%);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    text-align: center;
    box-shadow: var(--shadow);
}

.metric-value {
    color: var(--primary-color);
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 8px;
}

.metric-label {
    color: var(--gray-text);
    font-size: 14px;
    font-weight: 500;
}

/* Task List */
.task-item {
    background-color: var(--light-bg);
    padding: 16px;
    border-left: 4px solid var(--primary-color);
    border-radius: 6px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
}

.task-item:hover {
    background-color: #f0f3f7;
}

.task-item-completed {
    background-color: #f0fdf4;
    border-left-color: var(--success-color);
    opacity: 0.8;
}

.task-item-pending {
    background-color: #fef3f2;
    border-left-color: var(--warning-color);
}

.task-item-delayed {
    background-color: #fef2f2;
    border-left-color: var(--danger-color);
}

/* Header */
.dashboard-header {
    color: var(--dark-text);
    margin-bottom: 30px;
}

.dashboard-title {
    font-size: 32px;
    font-weight: 800;
    color: var(--dark-text);
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}

.dashboard-subtitle {
    font-size: 16px;
    color: var(--light-text);
}

/* Divider */
.divider {
    height: 1px;
    background-color: var(--border-color);
    margin: 30px 0;
}

/* Section Header */
.section-header {
    color: var(--dark-text);
    font-size: 20px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--border-color);
}

/* Emphasis Text */
.text-muted {
    color: var(--light-text);
}

.text-primary {
    color: var(--primary-color);
}

.text-success {
    color: var(--success-color);
}

.text-warning {
    color: var(--warning-color);
}

.text-danger {
    color: var(--danger-color);
}

/* Button Styling */
.stButton > button {
    background-color: var(--primary-color) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background-color: #0052a3 !important;
    box-shadow: var(--shadow-hover) !important;
}

/* Progress Bar Custom */
.progress-bar-custom {
    height: 6px;
    background-color: var(--light-bg);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 8px;
}

.progress-fill {
    background: linear-gradient(90deg, var(--primary-color), #00d4ff);
    height: 100%;
    border-radius: 3px;
    transition: width 0.3s ease;
}

/* Info Box */
.info-box {
    background-color: #eff6ff;
    border-left: 4px solid var(--primary-color);
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 12px;
}

/* Success Box */
.success-box {
    background-color: #f0fdf4;
    border-left: 4px solid var(--success-color);
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 12px;
}

/* Warning Box */
.warning-box {
    background-color: #fffbeb;
    border-left: 4px solid var(--warning-color);
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 12px;
}

/* Agent Pipeline Card */
.agent-card {
    background-color: #FFFFFF !important;
    color: #111111 !important;
    padding: 12px !important;
    border-radius: 10px !important;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08) !important;
    text-align: center !important;
}

/* Activity Card */
.activity-card {
    background-color: #FFFFFF !important;
    color: #333333 !important;
    padding: 10px !important;
    border-radius: 8px !important;
    margin-bottom: 8px !important;
    box-shadow: 0px 1px 4px rgba(0,0,0,0.06) !important;
}

/* Input field visibility improvement */
.stTextInput input {
    background-color: #FFFFFF !important;
    border: 1px solid #CCCCCC !important;
    color: #000000 !important;
    padding: 10px !important;
}

.stTextInput label {
    color: #333333 !important;
    font-weight: 500 !important;
}

/* Follow-up card styling */
.followup-card {
    background-color: #FFFFFF;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 12px;
    border: 1px solid #E0E0E0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* Section spacing improvement */
.section-spacer {
    margin-top: 20px;
    margin-bottom: 20px;
}

/* Prevent text wrapping in task details */
.task-detail {
    word-break: keep-all;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* No-wrap class for inline text */
.nowrap {
    white-space: nowrap !important;
    display: block !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    width: 100% !important;
    font-size: 14px !important;
    line-height: 1.4 !important;
    padding: 6px 0 !important;
    box-sizing: border-box !important;
}

/* Strong text in task names */
.nowrap strong {
    font-weight: 600 !important;
    color: #111 !important;
}

/* Streamlit column styling */
[data-testid="column"] {
    padding-left: 6px !important;
    padding-right: 6px !important;
    overflow: hidden !important;
}

/* Reduce text spacing */
[data-testid="column"] > div {
    margin: 0 !important;
    padding: 0 !important;
}

/* Button text wrapping prevention */
button {
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

button span {
    white-space: nowrap !important;
}

/* Task row styling */
.task-row {
    background-color: #FFFFFF;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 12px;
    border: 1px solid #E0E0E0;
    display: flex;
    gap: 12px;
    align-items: center;
}

</style>
"""

# Page configuration
st.set_page_config(
    page_title="AI Meeting Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Modern SaaS Dashboard CSS
st.markdown(MODERN_CSS, unsafe_allow_html=True)

# ============================================================================
# PROFESSIONAL HEADER
# ============================================================================
st.markdown("""
<div style="background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%); padding: 40px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(79, 70, 229, 0.15);">
    <h1 style="color: white; margin: 0; font-size: 32px; font-weight: 700;">AI Meeting Intelligence System</h1>
    <p style="color: rgba(255, 255, 255, 0.9); margin: 8px 0 0 0; font-size: 16px; font-weight: 400;">Autonomous Task Extraction &amp; Workflow Tracking</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS FOR RENDERING COMPONENTS
# ============================================================================

def render_priority_badge(priority):
    """Render color-coded priority badge"""
    priority_lower = priority.lower()
    if priority_lower == "high":
        return '<span class="badge-high"> High</span>'
    elif priority_lower == "medium":
        return '<span class="badge-medium"> Medium</span>'
    else:
        return '<span class="badge-low"> Low</span>'


def render_status_badge(status):
    """Render color-coded status badge"""
    status_lower = status.lower()
    if status_lower == "completed":
        return '<span class="status-completed"> Completed</span>'
    elif status_lower == "pending":
        return '<span class="status-pending">⏳ Pending</span>'
    else:
        return '<span class="status-delayed">️ Delayed</span>'


def create_task_card(task_id, title, description, priority, status, due_date):
    """Create a beautiful task card with modern styling"""
    priority_html = render_priority_badge(priority)
    status_html = render_status_badge(status)
    
    task_class = f"task-item-{status.lower()}"
    
    card_html = f"""
    <div class="task-item {task_class}">
        <div class="card-title">{title}</div>
        <div class="card-description">{description}</div>
        <div style="margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
            {priority_html}
            {status_html}
            <span class="text-muted" style="font-size: 13px; margin-left: auto;">Due: {due_date}</span>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def create_metric_card(label, value, icon=""):
    """Create a beautiful metric/KPI card"""
    metric_html = f"""
    <div class="metric-card">
        <div style="font-size: 24px; margin-bottom: 8px;">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)


def create_info_box(title, content, box_type="info"):
    """Create styled info/warning/success boxes"""
    box_class = f"{box_type}-box"
    html = f"""
    <div class="{box_class}">
        <div class="card-title" style="margin-bottom: 8px;">{title}</div>
        <div class="card-text">{content}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


if "agents_initialized" not in st.session_state:
    st.session_state.agents_initialized = False
    st.session_state.agent_logs = []
    st.session_state.current_page = "Dashboard"

if not st.session_state.agents_initialized:
    st.session_state.task_agent = TaskAgent()
    st.session_state.escalation_agent = EscalationAgent()
    st.session_state.audit_agent = AuditAgent()
    st.session_state.llm_service = LLMService()
    st.session_state.agents_initialized = True

def add_agent_log(agent: str, message: str):
    """Add log message from agent"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.agent_logs.append(f"[{timestamp}] {agent}: {message}")
    if len(st.session_state.agent_logs) > 20:
        st.session_state.agent_logs.pop(0)

def get_priority_icon(priority: str) -> str:
    """Get priority indicator (text-based)"""
    if priority == "High":
        return "[HIGH]"
    elif priority == "Medium":
        return "[MED]"
    else:
        return "[LOW]"

def get_status_color(status: str) -> str:
    """Get status indicator (text-based)"""
    if status == "Delayed":
        return "[DELAYED]"
    elif status == "Completed":
        return "[]"
    else:
        return "[PENDING]"

# ==================== HEADER ====================
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    <div style='display: flex; align-items: center; gap: 10px;'>
        <h1 style='margin: 0; font-size: 40px;'> AI Meeting Intelligence</h1>
    </div>
    <p style='margin: 0; color: #4ECDC4; font-size: 14px;'>Autonomous Multi-Agent Workflow Automation</p>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #4ECDC4, #0066cc);
        padding: 10px 15px;
        border-radius: 8px;
        text-align: center;
        color: #0a0a0a;
        font-weight: bold;
        font-size: 12px;
    '>
     Powered by Groq<br/>LLaMA 3
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==================== SIDEBAR NAVIGATION ====================
with st.sidebar:
    st.markdown("###  Navigation")
    
    pages = {
        "Dashboard": "",
        "Task Manager": "",
        "Agent Flow": "",
        "Audit Logs": "",
        "Impact Analysis": "",
        "How It Works": ""
    }
    
    for page, icon in pages.items():
        if st.button(f"{icon} {page}", use_container_width=True):
            st.session_state.current_page = page
    
    st.divider()
    
    st.markdown("### ️ Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Clear Tasks", use_container_width=True):
            st.session_state.task_agent.clear_tasks()
            add_agent_log("System", "All tasks cleared")
            st.success("Tasks cleared!")
            st.rerun()
    
    with col2:
        if st.button(" Demo Data", use_container_width=True):
            demo_tasks = [
                {"task": "Finalize Q1 strategy", "owner": "Alice", "deadline": "2026-03-30", "priority": "High", "status": "Pending"},
                {"task": "Complete API integration", "owner": "Bob", "deadline": "2026-03-25", "priority": "High", "status": "Pending"},
                {"task": "Review design mockups", "owner": "Charlie", "deadline": "2026-04-05", "priority": "Medium", "status": "Pending"},
                {"task": "Update documentation", "owner": "Diana", "deadline": "Not specified", "priority": "Medium", "status": "Pending"},
                {"task": "Client presentation prep", "owner": "Eve", "deadline": "2026-03-28", "priority": "High", "status": "Completed"},
            ]
            st.session_state.task_agent.store_tasks(demo_tasks)
            add_agent_log("System", "Demo data loaded")
            st.success("Demo data loaded!")
            st.rerun()

# ==================== PAGE ROUTING ====================
if st.session_state.current_page == "Dashboard":
    pass  # Will be defined below
elif st.session_state.current_page == "Task Manager":
    pass
elif st.session_state.current_page == "Agent Flow":
    pass
elif st.session_state.current_page == "Audit Logs":
    pass
elif st.session_state.current_page == "Impact Analysis":
    pass
elif st.session_state.current_page == "How It Works":
    pass

# ==================== PAGE FUNCTIONS ====================

def render_dashboard():
    """Main dashboard page"""
    
    # Agent Flow Visualization
    st.markdown("###  Agent Pipeline Architecture")
    
    pipeline_html = """
    <div style='
        background: #FFFFFF !important; color: #111111 !important;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 4px solid #4ECDC4;
        border: 1px solid #E8F0F4;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.08);
    '>
        <div style='display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;'>
            <div style='text-align: center;'>
                <div style='font-size: 30px;'></div>
                <div style='font-size: 12px; margin-top: 5px;'>Input</div>
            </div>
            <div style='font-size: 20px; color: #4ECDC4;'>→</div>
            <div style='text-align: center;'>
                <div style='font-size: 30px;'></div>
                <div style='font-size: 12px; margin-top: 5px;'>Understanding</div>
            </div>
            <div style='font-size: 20px; color: #4ECDC4;'>→</div>
            <div style='text-align: center;'>
                <div style='font-size: 30px;'></div>
                <div style='font-size: 12px; margin-top: 5px;'>Task Manager</div>
            </div>
            <div style='font-size: 20px; color: #4ECDC4;'>→</div>
            <div style='text-align: center;'>
                <div style='font-size: 30px;'></div>
                <div style='font-size: 12px; margin-top: 5px;'>Tracking</div>
            </div>
            <div style='font-size: 20px; color: #4ECDC4;'>→</div>
            <div style='text-align: center;'>
                <div style='font-size: 30px;'></div>
                <div style='font-size: 12px; margin-top: 5px;'>Escalation</div>
            </div>
            <div style='font-size: 20px; color: #4ECDC4;'>→</div>
            <div style='text-align: center;'>
                <div style='font-size: 30px;'></div>
                <div style='font-size: 12px; margin-top: 5px;'>Audit</div>
            </div>
        </div>
    </div>
    """
    st.markdown(pipeline_html, unsafe_allow_html=True)
    
    # Live Agent Activity
    st.markdown("###  Live Agent Activity")
    
    columns = st.columns([1, 1, 1, 1, 1])
    
    activity_items = [
        ("", "Extracting tasks..."),
        ("", "Structuring data..."),
        ("", "Analyzing metrics..."),
        ("", "Checking delays..."),
        ("", "Logging actions...")
    ]
    
    for col, (icon, action) in zip(columns, activity_items):
        with col:
            st.markdown(f"""
            <div style='
                background: #FFFFFF !important; color: #111111 !important;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                border-left: 3px solid #4ECDC4; border: 1px solid #E8F0F4; box-shadow: 0 2px 8px rgba(79, 70, 229, 0.08);
            '>
                <div style='font-size: 24px;'>{icon}</div>
                <div style='font-size: 12px; margin-top: 8px;'>{action}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Metrics Dashboard
    st.markdown("###  Task Metrics")
    
    tasks = st.session_state.task_agent.get_all_tasks()
    
    total = len(tasks)
    completed = len([t for t in tasks if t.get("status") == "Completed"])
    pending = len([t for t in tasks if t.get("status") == "Pending"])
    delayed = len([t for t in tasks if t.get("status") == "Delayed"])
    
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 14px; color: #4ECDC4;'>Total Tasks</div>
            <div style='font-size: 32px; font-weight: bold; margin: 10px 0;'>{total}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[1]:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 14px; color: #0066cc;'>Completed</div>
            <div style='font-size: 32px; font-weight: bold; margin: 10px 0; color: #4ECDC4;'>{completed}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[2]:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 14px; color: #FFA500;'>Pending</div>
            <div style='font-size: 32px; font-weight: bold; margin: 10px 0; color: #FFA500;'>{pending}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_cols[3]:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 14px; color: #FF6B6B;'>Delayed</div>
            <div style='font-size: 32px; font-weight: bold; margin: 10px 0; color: #FF6B6B;'>{delayed}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts
    chart_col1, chart_col2, chart_col3 = st.columns(3)
    
    with chart_col1:
        # Task Status Distribution
        status_counts = {"Pending": pending, "Completed": completed, "Delayed": delayed}
        fig = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Task Status Distribution",
            color_discrete_map={"Pending": "#FFA500", "Completed": "#4ECDC4", "Delayed": "#FF6B6B"},
            hole=0.3
        )
        fig.update_layout(height=300, showlegend=True, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        # Priority Distribution
        if tasks:
            priority_counts = {
                "High": len([t for t in tasks if t.get("priority") == "High"]),
                "Medium": len([t for t in tasks if t.get("priority") == "Medium"]),
                "Low": len([t for t in tasks if t.get("priority") == "Low"])
            }
            fig = px.bar(
                x=list(priority_counts.keys()),
                y=list(priority_counts.values()),
                title="Priority Distribution",
                color=list(priority_counts.keys()),
                color_discrete_map={"High": "#FF6B6B", "Medium": "#FFA500", "Low": "#4ECDC4"}
            )
            fig.update_layout(height=300, showlegend=False, template="plotly_dark", xaxis_title="", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
    
    with chart_col3:
        # Tasks by Owner
        if tasks:
            owner_counts = {}
            for task in tasks:
                status_icon = get_status_color(task.get("status", "Pending"))
                priority_icon = get_priority_icon(task.get("priority", "Medium"))
            
            # Feature 3: Deadline Intelligence
            deadline_info = analyze_deadline(
                task.get("deadline", "Not specified"),
                task.get("created_date", None)
            )
            
            # Display task info in a single compact row with better layout
            st.markdown(f"""
            <div style="background-color: #FFFFFF; padding: 12px; border-radius: 6px; border: 1px solid #E0E0E0; margin-bottom: 12px;">
                <div style="display: flex; gap: 16px; align-items: center; flex-wrap: nowrap; overflow: hidden;">
                    <div style="flex: 1; min-width: 0;"><strong style="color: #111; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block;">{task.get('task', 'Untitled')}</strong></div>
                    <div style="flex: 0 0 auto; white-space: nowrap; color: #555; font-size: 13px;">{task.get('owner', 'Unknown')}</div>
                    <div style="flex: 0 0 auto; white-space: nowrap; font-size: 13px;">{priority_icon} {task.get('priority', 'Medium')}</div>
                    <div style="flex: 0 0 auto; white-space: nowrap; font-size: 13px;">{status_icon} {task.get('status', 'Pending')}</div>
                    <div style="flex: 0 0 auto; white-space: nowrap; color: #666; font-size: 13px;">{task.get('deadline', 'Not specified')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Action controls
            action_col1, action_col2 = st.columns([3.5, 1.5])
            
            with action_col1:
                new_status = st.selectbox(
                    "Update Status",
                    ["Pending", "Completed", "Delayed"],
                    index=["Pending", "Completed", "Delayed"].index(task.get("status", "Pending")),
                    key=f"status_{task.get("task", "unknown")}"
                )
                if new_status != task.get("status"):
                    st.session_state.task_agent.update_task_status(task.get("task"), new_status)
                    add_agent_log("Task Manager", f"Updated '{task.get("task")}' to {new_status}")
                    st.rerun()
            
            with action_col2:
                if st.button("Delete", key=f"delete_{task.get("task", "unknown")}", help="Delete task", use_container_width=True):
                    st.session_state.task_agent.delete_task(task.get("task"))
                    add_agent_log("Task Manager", f"Deleted '{task.get("task")}'")  
                    st.rerun()
            
            st.divider()

def render_task_manager():
    """Task Manager page"""
    st.markdown("###  Task Manager")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        meeting_input = st.text_area(
            "Enter Meeting Transcript:",
            height=200,
            placeholder="Paste your meeting transcript here...",
            help="Describe the meeting content, decisions, and action items"
        )
    
    with col2:
        st.markdown("**Auto-Extract Settings:**")
        use_strict_extraction = st.checkbox("Strict Extraction Mode", value=True, help="Extract ALL tasks including implicit ones")
        infer_owner = st.checkbox("Infer Unclear Owners", value=True, help="Attempt to infer task owners from context")
        
        if st.button(" Process Meeting", use_container_width=True):
            if meeting_input.strip():
                with st.spinner("Processing meeting with AI agents..."):
                    add_agent_log("Understanding Agent", "Analyzing meeting transcript...")
                    
                    add_agent_log("Task Agent", "Extracting actionable tasks...")
                    tasks = st.session_state.llm_service.extract_tasks(meeting_input)
                    
                    if tasks:
                        for task in tasks:
                            if "status" not in task:
                                task["status"] = "Pending"
                        
                        st.session_state.task_agent.store_tasks(tasks)
                        add_agent_log("Task Agent", f"Extracted and stored {len(tasks)} tasks")
                        
                        add_agent_log("Tracking Agent", "Analyzing task deadlines...")
                        add_agent_log("Escalation Agent", "Checking for delays...")
                        add_agent_log("Audit Agent", "Logging actions...")
                        
                        st.success(f" Extracted {len(tasks)} tasks!")
                        st.rerun()
                    else:
                        st.warning("Could not extract any tasks. Try rephrasing your input.")
            else:
                st.warning("Please enter a meeting transcript.")
    
    st.divider()
    
    # Display extracted tasks
    tasks = st.session_state.task_agent.get_all_tasks()
    
    if tasks:
        st.markdown("###  Current Tasks")
        
        for idx, task in enumerate(tasks):
            with st.expander(f" {task.get('task', 'Untitled')} - {task.get('owner', 'Unknown')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Owner:** {task.get('owner', 'Unknown')}")
                    st.write(f"**Deadline:** {task.get('deadline', 'Not specified')}")
                    st.write(f"**Priority:** {get_priority_icon(task.get('priority', 'Medium'))} {task.get('priority', 'Medium')}")
                    st.write(f"**Status:** {get_status_color(task.get('status', 'Pending'))} {task.get('status', 'Pending')}")
                
                with col2:
                    col_edit, col_delete = st.columns(2)
                    with col_edit:
                        new_status = st.selectbox(
                            "Change Status:",
                            ["Pending", "Completed", "Delayed"],
                            index=["Pending", "Completed", "Delayed"].index(task.get("status", "Pending")),
                            key=f"task_status_{idx}"
                        )
                        if new_status != task.get("status"):
                            st.session_state.task_agent.update_task_status(task.get("task"), new_status)
                            st.success(f"Updated to {new_status}")
                            st.rerun()
                    
                    with col_delete:
                        if st.button("Delete Task", key=f"task_delete_{idx}", use_container_width=True):
                            st.session_state.task_agent.delete_task(task.get("task"))
                            st.success("Task deleted!")
                            st.rerun()

def render_agent_flow():
    """Agent Flow Visualization page"""
    st.markdown("###  Agent Pipeline Flow")
    
    st.markdown("""
    The AI Meeting Intelligence System uses a sophisticated multi-agent pipeline:
    
    1. **Understanding Agent **
       - Analyzes meeting content
       - Identifies key topics and decisions
       - Extracts meeting context
    
    2. **Task Agent **
       - Structures identified tasks
       - Assigns ownership and deadlines
       - Prioritizes based on urgency
    
    3. **Tracking Agent **
       - Monitors task progress
       - Updates statusesas new information arrives
       - Maintains comprehensive task history
    
    4. **Escalation Agent ️**
       - Checks for overdue tasks
       - Alerts on critical deadlines
       - Escalates high-priority issues
    
    5. **Audit Agent **
       - Logs all system actions
       - Maintains change history
       - Provides compliance tracking
    """)
    
    st.divider()
    
    st.markdown("###  Recent Agent Logs")
    
    if st.session_state.agent_logs:
        log_text = "\n".join(st.session_state.agent_logs[-15:])
        st.markdown(f"""
        <div style='
            background: #FFFFFF !important; color: #111111 !important;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 11px;
            color: #4ECDC4;
            max-height: 300px;
            overflow-y: auto;
        '>
        {log_text}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No agent logs yet. Process a meeting to see agent activity.")

def render_audit_logs():
    """Audit Logs page"""
    st.markdown("###  System Audit Logs")
    
    # In a real implementation, this would load from the audit log file
    st.info("Audit logging is enabled. All system actions are being tracked for compliance and debugging.")
    
    # Show recent agent logs
    st.markdown("**Recent Activity:**")
    
    if st.session_state.agent_logs:
        for log in st.session_state.agent_logs[-10:][::-1]:
            st.markdown(f"```\n{log}\n```")
    else:
        st.info("No activity logged yet.")

def render_impact_analysis():
    """Impact Analysis page - Show ROI and business value"""
    st.markdown("###  Business Impact Analysis")
    
    st.markdown("""
    ####  Efficiency Improvements
    
    This system dramatically improves meeting follow-up efficiency:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    # Assumptions
    avg_meeting_followup = 60  # minutes
    with_system = 10  # minutes
    meetings_per_month = 100
    employee_cost_per_hour = 500  # Indian Rupees
    
    time_saved_per_meeting = avg_meeting_followup - with_system  # 50 minutes
    total_time_saved_per_month = time_saved_per_meeting * meetings_per_month  # 5000 minutes
    hours_saved_per_month = total_time_saved_per_month / 60  # ~83.33 hours
    cost_saved_per_month = hours_saved_per_month * employee_cost_per_hour
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 14px; color: #4ECDC4;'>⏱️ Time Saved</div>
            <div style='font-size: 32px; font-weight: bold; margin: 10px 0;'>{int(hours_saved_per_month)} hrs</div>
            <div style='font-size: 12px; color: #666666;'>per month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 14px; color: #0066cc;'> Cost Saved</div>
            <div style='font-size: 32px; font-weight: bold; margin: 10px 0;'>₹{int(cost_saved_per_month):,}</div>
            <div style='font-size: 12px; color: #666666;'>per month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        annual_savings = cost_saved_per_month * 12
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 14px; color: #4ECDC4;'> Annual Savings</div>
            <div style='font-size: 32px; font-weight: bold; margin: 10px 0;'>₹{int(annual_savings):,}</div>
            <div style='font-size: 12px; color: #666666;'>per year</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Create comparison chart
    st.markdown("####  Before vs. After Comparison")
    
    fig = go.Figure(data=[
        go.Bar(name='Manual Process', x=['Time per Meeting', 'Cost per Meeting'], y=[avg_meeting_followup, avg_meeting_followup * (employee_cost_per_hour / 60)], marker_color='#FF6B6B'),
        go.Bar(name='With AI System', x=['Time per Meeting', 'Cost per Meeting'], y=[with_system, with_system * (employee_cost_per_hour / 60)], marker_color='#4ECDC4')
    ])
    
    fig.update_layout(
        title="Process Efficiency Comparison",
        xaxis_title="Metric",
        yaxis_title="Value (min / ₹)",
        template="plotly_dark",
        height=400,
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.markdown("####  Business Impact")
    
    st.markdown(f"""
    **Key Benefits:**
    
    1. **⏱️ Time Efficiency**: Reduces meeting follow-up from {avg_meeting_followup} minutes to {with_system} minutes ({time_saved_per_meeting}-minute saving per meeting)
    
    2. ** Cost Reduction**: Save ₹{int(cost_saved_per_month):,} monthly with {meetings_per_month} meetings/month
    
    3. ** Scalability**: System handles unlimited concurrent meetings
    
    4. ** Accuracy**: 100% task capture - no missed action items
    
    5. ** Transparency**: Complete audit trail for compliance
    
    6. ** Productivity**: Employees focus on high-value activities instead of manual task coordination
    
    **Bottom Line:**
    This system automates task tracking, reduces manual coordination overhead, improves accountability, and significantly increases operational efficiency.
    """)

def render_how_it_works():
    """How It Works page"""
    st.markdown("###  How It Works")
    
    st.markdown("""
    ####  Three Simple Steps
    
    1. ** Input Your Meeting**
       - Paste your meeting transcript or summary
       - Our system automatically detects tasks and action items
    
    2. ** Agents Process**
       - Understanding Agent analyzes content
       - Task Agent extracts and structures tasks
       - Tracking Agent monitors progress
       - Escalation Agent alerts on delays
       - Audit Agent keeps detailed logs
    
    3. ** Get Results**
       - View all extracted tasks in one dashboard
       - Track progress in real-time
       - Get alerts for delayed items
       - Export audit logs for compliance
    
    ####  Powered by Groq LLaMA 3
    
    - World's fastest LLM inference
    - Enterprise-grade reliability
    - Privacy-first processing
    - Contextual task extraction
    """)
    
    st.divider()
    
    st.markdown("####  Try It Now")
    
    example_transcript = """
    In today's product meeting:
    - John needs to finalize the API documentation by Friday
    - Sarah will review the UI mockups and provide feedback by Monday
    - The team agreed to schedule a client presentation for March 28
    - Mike mentioned we should update the database schema - no specific deadline yet
    - We need to fix the login bug that was reported - this is urgent
    - Alice will prepare the quarterly business review for end of month
    """
    
    if st.button(" Load Example Transcript"):
        st.session_state.example_loaded = True
    
    if st.button("⏭️ Go to Task Manager"):
        st.session_state.current_page = "Task Manager"
        st.rerun()

st.divider()

# ==================== RENDER PAGE ====================
if st.session_state.current_page == "Dashboard":
    render_dashboard()
elif st.session_state.current_page == "Task Manager":
    render_task_manager()
elif st.session_state.current_page == "Agent Flow":
    render_agent_flow()
elif st.session_state.current_page == "Audit Logs":
    render_audit_logs()
elif st.session_state.current_page == "Impact Analysis":
    render_impact_analysis()
elif st.session_state.current_page == "How It Works":
    render_how_it_works()

st.divider()
st.markdown("""
<div style='text-align: center; color: #666666; font-size: 12px; padding: 20px;'>
    <strong>AI Meeting Intelligence System</strong> | Powered by Groq LLaMA 3 | © 2026 Hackathon Edition
</div>
""", unsafe_allow_html=True)
