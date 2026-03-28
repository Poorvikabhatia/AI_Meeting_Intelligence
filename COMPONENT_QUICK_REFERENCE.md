# 🎨 Quick Reference - Modern UI Components

## Color Codes

| Element | Color | Hex | Usage |
|---------|-------|-----|-------|
| **Primary** | Blue | `#0066cc` | Buttons, primary actions |
| **Success** | Green | `#10b981` | Completed, success |
| **Warning** | Orange | `#f59e0b` | Pending, caution |
| **Danger** | Red | `#ef4444` | Delayed, errors |
| **White BG** | White | `#ffffff` | Card backgrounds |
| **Gray BG** | Light Gray | `#f8f9fa` | Alternate sections |
| **Dark Text** | Almost Black | `#111111` | Titles, main text |
| **Gray Text** | Dark Gray | `#333333` | Body content |
| **Muted Text** | Gray | `#666666` | Secondary info |

---

## Quick Component Usage

### 📊 Metric Card
```python
create_metric_card("Label", "Value", "Icon")
# Example:
create_metric_card("Total Meetings", "24", "📅")
```

### 📝 Task Card
```python
create_task_card(id, title, description, priority, status, due_date)
# Example:
create_task_card(
    1,
    "Task Title",
    "Task description here",
    "High",  # or "Medium", "Low"
    "Pending",  # or "Completed", "Delayed"
    "Mar 29"
)
```

### 🏷️ Badges (Standalone)
```python
# Priority Badges
render_priority_badge("High")    # Red: 🔴 High
render_priority_badge("Medium")  # Yellow: 🟡 Medium
render_priority_badge("Low")     # Green: 🟢 Low

# Status Badges
render_status_badge("Completed")  # Green: ✓ Completed
render_status_badge("Pending")    # Yellow: ⏳ Pending
render_status_badge("Delayed")    # Red: ⚠️ Delayed
```

### 📦 Info Box
```python
create_info_box(title, content, "info")  # Blue
create_info_box(title, content, "success")  # Green
create_info_box(title, content, "warning")  # Yellow
```

### 🎴 Custom Card
```python
st.markdown("""
<div class="card">
    <div class="card-title">Title Here</div>
    <div class="card-text">Your content</div>
    <div class="card-description">Optional details</div>
</div>
""", unsafe_allow_html=True)
```

---

## CSS Classes Reference

### Text Classes
- `.card-title` - Large, bold heading (18px)
- `.card-subtitle` - Secondary heading (14px muted)
- `.card-text` - Body text (14px dark)
- `.card-description` - Small secondary text (13px muted)
- `.text-muted` - Muted gray text
- `.text-primary` - Blue primary color
- `.text-success` - Green success color
- `.text-warning` - Orange warning color
- `.text-danger` - Red danger color

### Container Classes
- `.card` - Main card container
- `.task-item` - Task list item
- `.metric-card` - KPI/metric display
- `.info-box` - Info message
- `.success-box` - Success message
- `.warning-box` - Warning message

### Status Classes
- `.task-item-completed` - Completed task styling
- `.task-item-pending` - Pending task styling
- `.task-item-delayed` - Delayed task styling

---

## Layout Examples

### Two Column Layout
```python
col1, col2 = st.columns(2)
with col1:
    create_metric_card("Label 1", "Value 1", "Icon1")
with col2:
    create_metric_card("Label 2", "Value 2", "Icon2")
```

### Three Column Layout
```python
col1, col2, col3 = st.columns(3)
with col1:
    create_metric_card("Metrics", "Value", "Icon")
# ... repeat
```

### Four Column Layout (Recommended for KPIs)
```python
col1, col2, col3, col4 = st.columns(4)
with col1:
    create_metric_card("Total", "24", "📊")
with col2:
    create_metric_card("Completed", "18", "✓")
with col3:
    create_metric_card("Pending", "4", "⏳")
with col4:
    create_metric_card("Delayed", "2", "⚠️")
```

---

## Priority/Status Quick Reference

### Priority Levels (for data)
```
"High"   → Red background #ffe5e5
"Medium" → Yellow background #fff4cc
"Low"    → Green background #e6f4ea
```

### Status Values (for data)
```
"Completed" → Green background #d4edda
"Pending"   → Yellow background #fff3cd
"Delayed"   → Red background #f8d7da
```

---

## Common Patterns

### Header Section
```python
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">Emoji Title</div>
    <div class="dashboard-subtitle">Subtitle text</div>
</div>
""", unsafe_allow_html=True)
```

### Section Divider
```python
st.markdown("<div class='section-header'>Section Title</div>", unsafe_allow_html=True)
```

### Button Row
```python
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Action 1"):
        pass
with col2:
    if st.button("Action 2"):
        pass
```

### Loop Through Data
```python
for item in data_list:
    create_task_card(
        item["id"],
        item["title"],
        item["description"],
        item["priority"],
        item["status"],
        item["due_date"]
    )
```

---

## Styling Guidelines

### Spacing
- Card padding: `20px`
- Between elements: `15px`
- Between inline items: `8px`
- Top margin for sections: `25px`

### Shadows
- Normal: `0px 2px 10px rgba(0,0,0,0.08)`
- Hover: `0px 4px 16px rgba(0,0,0,0.12)`

### Border Radius
- Cards: `12px`
- Badges: `6px`
- Buttons: `8px`

### Transitions
- Hover effects: `0.3s ease`
- Button clicks: `0.2s ease`

---

## Color Combinations (Recommended)

### High Priority + Pending
```html
<span class="badge-high">🔴 High</span>
<span class="status-pending">⏳ Pending</span>
```
Result: Alert users immediately

### Medium Priority + Completed
```html
<span class="badge-medium">🟡 Medium</span>
<span class="status-completed">✓ Completed</span>
```
Result: Acknowledge completion

### Low Priority + Delayed
```html
<span class="badge-low">🟢 Low</span>
<span class="status-delayed">⚠️ Delayed</span>
```
Result: Lower urgency, monitor

---

## Icons You Can Use

### Common Emoji Icons
- 📊 Dashboard
- 📋 Tasks/Lists
- ✓ Completed/Success
- ⏳ Pending/Waiting
- ⚠️ Warning/Alert
- 🔴 High Priority
- 🟡 Medium Priority
- 🟢 Low Priority
- 📅 Calendar/Date
- 👥 People/Team
- 💬 Messages/Chat
- 📈 Analytics/Growth
- 🎯 Goals/Target
- 🔔 Notifications

---

## Testing Checklist

- [ ] Light background (white #fff or light gray #f8f9fa)
- [ ] Dark text (nearly black #111111 or dark gray #333333)
- [ ] Color contrast passes WCAG AA
- [ ] Cards have subtle shadows
- [ ] Badges are clearly visible
- [ ] Hover effects are smooth
- [ ] Mobile layout is responsive
- [ ] No overlapping elements
- [ ] Icons render correctly
- [ ] Font sizes are readable (14px+ for body)

---

## Performance Tips

1. **Reuse components** - Don't create unique HTML each time
2. **Batch renders** - Loop through data instead of multiple st.markdown calls
3. **Cache data** - Use @st.cache decorator for expensive operations
4. **Lazy load** - Use st.columns() to control layout
5. **Minimize markup** - Keep HTML clean and simple

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Text not readable | Check bg is light, text is dark |
| Badges not showing | Verify CSS classes in `.card` context |
| Cards too crowded | Add spacing with `<div style="height: 20px;"></div>` |
| Colors wrong | Check hex codes match exactly |
| Mobile breaks | Use `st.columns()` for responsive layout |
| Slow rendering | Reduce st.markdown() calls, batch operations |

---

**Version**: 1.0  
**Created**: 2026-03-26  
**Theme**: Modern Light SaaS Dashboard  
**Status**: ✅ LIVE
