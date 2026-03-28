# 📚 Complete Implementation Examples

## Example 1: Basic Dashboard Layout

```python
import streamlit as st

# Page setup (already in main app.py)
st.set_page_config(
    page_title="AI Meeting Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS and helpers are already injected at app startup
# Just use the helper functions!

# ================================================================
# HEADER SECTION
# ================================================================

st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">📊 AI Meeting Intelligence</div>
    <div class="dashboard-subtitle">Real-time meeting insights and task management</div>
</div>
""", unsafe_allow_html=True)

# ================================================================
# KEY METRICS SECTION
# ================================================================

st.markdown("<div class='section-header'>📈 Key Metrics</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    create_metric_card("Total Meetings", "24", "📅")

with col2:
    create_metric_card("Action Items", "12", "✓")

with col3:
    create_metric_card("Completed Tasks", "8", "✅")

with col4:
    create_metric_card("Pending", "4", "⏳")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ================================================================
# RECENT TASKS SECTION
# ================================================================

st.markdown("<div class='section-header'>📋 Recent Tasks</div>", unsafe_allow_html=True)

# Sample data
tasks = [
    {
        "id": 1,
        "title": "Finalize Q2 Budget Proposal",
        "description": "Complete the financial review and prepare final budget for stakeholder approval.",
        "priority": "High",
        "status": "Pending",
        "due_date": "Mar 29, 2026"
    },
    {
        "id": 2,
        "title": "Team Training Session",
        "description": "Conduct training session on new project management tools.",
        "priority": "Medium",
        "status": "Completed",
        "due_date": "Mar 25, 2026"
    },
    {
        "id": 3,
        "title": "Client Presentation Review",
        "description": "Review and finalize presentation deck for client meeting.",
        "priority": "High",
        "status": "Pending",
        "due_date": "Mar 27, 2026"
    },
]

# Render task cards
for task in tasks:
    create_task_card(
        task["id"],
        task["title"],
        task["description"],
        task["priority"],
        task["status"],
        task["due_date"]
    )

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ================================================================
# LATEST MEETING SECTION
# ================================================================

st.markdown("<div class='section-header'>💬 Latest Meeting Summary</div>", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <div class="card-title">📌 Q2 Strategy Planning</div>
    <div class="card-subtitle">March 26, 2026 · 2:00 PM - 3:30 PM</div>
    <div class="card-text">
        <strong>Attendees:</strong> 8 people | <strong>Duration:</strong> 90 mins
        <div style="margin-top: 12px;">
            <strong>Key Takeaways:</strong>
            <ul>
                <li>Approved new product roadmap for Q2 launch</li>
                <li>Budget allocated for 3 new team members</li>
                <li>Marketing campaign to begin April 1st</li>
            </ul>
        </div>
        <div style="margin-top: 12px;">
            <strong>Decision:</strong> Moved forward with expansion plan
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
```

---

## Example 2: Task Filtering Dashboard

```python
# ================================================================
# FILTERED TASK VIEW
# ================================================================

st.markdown("<div class='section-header'>✓ Task Management</div>", unsafe_allow_html=True)

# Filter controls
col1, col2, col3 = st.columns(3)

with col1:
    priority_filter = st.selectbox(
        "Filter by Priority:",
        ["All", "High", "Medium", "Low"]
    )

with col2:
    status_filter = st.selectbox(
        "Filter by Status:",
        ["All", "Completed", "Pending", "Delayed"]
    )

with col3:
    sort_by = st.selectbox(
        "Sort by:",
        ["Due Date", "Priority", "Status"]
    )

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Sample data
all_tasks = [
    {"id": 1, "title": "Finalize Q2 Budget", "desc": "Budget review and approval", "priority": "High", "status": "Pending", "date": "Mar 29"},
    {"id": 2, "title": "Team Training", "desc": "Tool training session", "priority": "Medium", "status": "Completed", "date": "Mar 25"},
    {"id": 3, "title": "Client Presentation", "desc": "Final presentation deck", "priority": "High", "status": "Pending", "date": "Mar 27"},
    {"id": 4, "title": "Update Documentation", "desc": "Update project docs", "priority": "Low", "status": "Delayed", "date": "Mar 20"},
]

# Filter tasks
filtered_tasks = all_tasks

if priority_filter != "All":
    filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority_filter]

if status_filter != "All":
    filtered_tasks = [t for t in filtered_tasks if t["status"] == status_filter]

# Display filtered tasks
if filtered_tasks:
    for task in filtered_tasks:
        create_task_card(
            task["id"],
            task["title"],
            task["desc"],
            task["priority"],
            task["status"],
            task["date"]
        )
else:
    create_info_box(
        "No tasks found",
        "Try adjusting your filters",
        "info"
    )
```

---

## Example 3: Analytics Dashboard

```python
# ================================================================
# ANALYTICS PAGE
# ================================================================

st.markdown("<div class='section-header'>📊 Analytics & Reports</div>", unsafe_allow_html=True)

# KPI Row
col1, col2, col3 = st.columns(3)

with col1:
    create_metric_card("Meeting Frequency", "4.2/day", "📈")

with col2:
    create_metric_card("Avg Meeting Duration", "45 min", "⏱️")

with col3:
    create_metric_card("Task Completion Rate", "67%", "📊")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">Meeting Frequency by Day</div>
        <div class="card-text">Average 4.2 meetings per day</div>
        <div style="height: 150px; background: linear-gradient(135deg, #f0f4ff, #e0e9ff); border-radius: 8px; margin-top: 12px;"></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">Task Completion Trend</div>
        <div class="card-text">67% of tasks completed on time</div>
        <div style="height: 150px; background: linear-gradient(135deg, #f0fdf4, #dcfce7); border-radius: 8px; margin-top: 12px;"></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Status Distribution
col1, col2, col3 = st.columns(3)

with col1:
    create_metric_card("Completed", "18", "✓")

with col2:
    create_metric_card("In Progress", "8", "⌛")

with col3:
    create_metric_card("Not Started", "4", "❎")
```

---

## Example 4: Alerts & Notifications

```python
# ================================================================
# ALERTS SECTION
# ================================================================

st.markdown("<div class='section-header'>⚠️ Alerts & Notifications</div>", unsafe_allow_html=True)

# Critical Alert
create_info_box(
    "🔴 High Priority: Budget Review Due",
    "The Q2 budget review is due today. Please finalize and submit by 5 PM.",
    box_type="warning"
)

# Success Alert
create_info_box(
    "✓ Team Training Completed",
    "28 team members have completed the new project management tools training.",
    box_type="success"
)

# Info Alert
create_info_box(
    "ℹ️ System Maintenance Scheduled",
    "The system will undergo maintenance on Saturday from 2-4 AM UTC. Plan accordingly.",
    box_type="info"
)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Upcoming Events
st.markdown("<div class='section-header'>📅 Upcoming Events</div>", unsafe_allow_html=True)

upcoming = [
    {"time": "2:00 PM", "title": "Strategy Meeting", "attendees": 8, "status": "Confirmed"},
    {"time": "3:30 PM", "title": "Team Standup", "attendees": 12, "status": "Confirmed"},
    {"time": "4:00 PM", "title": "Client Call", "attendees": 5, "status": "Pending"},
]

for event in upcoming:
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="card-title">{event['title']}</div>
                <div class="card-description">{event['time']} • {event['attendees']} attendees</div>
            </div>
            <div>
                {render_status_badge(event['status'])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
```

---

## Example 5: Data Table with Badges

```python
# ================================================================
# TEAM MEMBERS TABLE
# ================================================================

st.markdown("<div class='section-header'>👥 Team Members</div>", unsafe_allow_html=True)

teams = [
    {"name": "Alice Johnson", "role": "Project Manager", "tasksCompleted": 12, "status": "Completed"},
    {"name": "Bob Smith", "role": "Developer", "tasksCompleted": 8, "status": "Pending"},
    {"name": "Carol White", "role": "Designer", "tasksCompleted": 10, "status": "Completed"},
    {"name": "David Brown", "role": "QA Engineer", "tasksCompleted": 5, "status": "Pending"},
]

for person in teams:
    st.markdown(f"""
    <div class="card" style="padding: 12px 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">
                <div class="card-title" style="margin-bottom: 4px;">{person['name']}</div>
                <div class="card-description">{person['role']}</div>
            </div>
            <div style="text-align: right;">
                <div class="card-text">{person['tasksCompleted']} tasks</div>
                {render_status_badge(person['status'])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
```

---

## Example 6: Custom Action Cards

```python
# ================================================================
# ACTION CARDS
# ================================================================

st.markdown("<div class='section-header'>🎯 Quick Actions</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card" style="text-align: center; cursor: pointer;">
        <div style="font-size: 32px; margin-bottom: 12px;">📝</div>
        <div class="card-title" style="font-size: 16px;">Create Meeting</div>
        <div class="card-description">Schedule a new meeting</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card" style="text-align: center; cursor: pointer;">
        <div style="font-size: 32px; margin-bottom: 12px;">✓</div>
        <div class="card-title" style="font-size: 16px;">Add Task</div>
        <div class="card-description">Create a new task</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card" style="text-align: center; cursor: pointer;">
        <div style="font-size: 32px; margin-bottom: 12px;">📊</div>
        <div class="card-title" style="font-size: 16px;">Generate Report</div>
        <div class="card-description">Export analytics report</div>
    </div>
    """, unsafe_allow_html=True)
```

---

## Example 7: Settings/Preferences Page

```python
# ================================================================
# SETTINGS PAGE
# ================================================================

st.markdown("<div class='section-header'>⚙️ Settings</div>", unsafe_allow_html=True)

# Theme Settings
st.markdown("""
<div class="card">
    <div class="card-title">Appearance</div>
    <div style="margin-top: 16px;">
        <div style="margin-bottom: 12px;">
            <strong>Theme:</strong> Light Mode (default)
        </div>
        <div style="margin-bottom: 12px;">
            <strong>Compact View:</strong> Enabled
        </div>
        <div style="margin-bottom: 12px;">
            <strong>Font Size:</strong> Normal (14px)
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Notification Settings
st.markdown("""
<div class="card">
    <div class="card-title">Notifications</div>
    <div style="margin-top: 16px;">
        <div style="margin-bottom: 12px;">
            <strong>Email Notifications:</strong> Enabled
        </div>
        <div style="margin-bottom: 12px;">
            <strong>Desktop Alerts:</strong> Enabled
        </div>
        <div style="margin-bottom: 12px;">
            <strong>Sound Alerts:</strong> Disabled
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Account Settings
st.markdown("""
<div class="card">
    <div class="card-title">Account</div>
    <div style="margin-top: 16px;">
        <div style="margin-bottom: 12px;">
            <strong>Email:</strong> user@example.com
        </div>
        <div style="margin-bottom: 12px;">
            <strong>Last Login:</strong> Today at 2:34 PM
        </div>
        <div style="margin-top: 16px;">
            <button onclick="alert('Change Password clicked')" 
                    style="background: #0066cc; color: white; border: none; padding: 8px 16px; 
                            border-radius: 6px; cursor: pointer; font-weight: 600;">
                Change Password
            </button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
```

---

## Key Takeaways

1. **Always inject CSS at startup** - Call `st.markdown(MODERN_CSS, unsafe_allow_html=True)` once
2. **Use helper functions** - `create_task_card()`, `create_metric_card()`, etc.
3. **Organize with sections** - Use `st.markdown(...section-header...)` for clarity
4. **Add spacing** - Use `<div style='height: 20px;'></div>` between sections
5. **Use columns for layout** - `st.columns(4)` for metrics, `st.columns(2)` for content
6. **Loop for repeated elements** - Don't write HTML multiple times
7. **Add context** - Use `.card-subtitle` and `.card-description` for extra info
8. **Combine colors** - Priority + Status badges together for clarity

---

**These examples show best practices for:**
- Dashboard layouts
- Task management
- Analytics views
- Alert systems
- Data tables
- Action cards
- Settings pages
