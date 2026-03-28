# Configuration & Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Streamlit UI Layer                          │
│  (Dashboard, Task Manager, Audit Logs, Home Page)              │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│                    Multi-Agent Pipeline                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Understanding Agent → LLM Task Extraction                    │
│ 2. Task Manager Agent → Persistent Storage                      │
│ 3. Tracking Agent → Metrics Calculation                         │
│ 4. Escalation Agent → Deadline Monitoring                       │
│ 5. Audit Agent → Activity Logging                               │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│                    Service Layer                                 │
├─────────────────────────────────────────────────────────────────┤
│ • LLM Service (Groq API)                                        │
│ • Task Parser & Validator                                       │
│ • File I/O & Persistence                                        │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│                   Data Storage Layer                             │
├─────────────────────────────────────────────────────────────────┤
│ • tasks.json (Task Storage)                                     │
│ • logs.json (Audit Logs)                                        │
│ • External APIs (Groq)                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Component Map

### Agents
| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| Understanding | Extract tasks from text | Transcript | Task list |
| Task Manager | Store & manage tasks | Task list | Persistent tasks |
| Tracking | Calculate metrics | Tasks | Metrics dict |
| Escalation | Monitor deadlines | Tasks + Date | Alerts |
| Audit | Log activities | Action | Log entries |

### Services
| Service | Purpose | Dependencies |
|---------|---------|--------------|
| LLM Service | Groq API communication | groq package |
| Parser | JSON parsing & validation | json module |

### Data Models

#### Task Object
```python
{
    "task": str,           # Task description
    "owner": str,          # Responsible person
    "deadline": str,       # YYYY-MM-DD format
    "priority": str,       # High/Medium/Low
    "status": str,         # Pending/Completed/Delayed
    "created_at": str      # ISO timestamp
}
```

#### Log Entry Object
```python
{
    "timestamp": str,      # ISO timestamp
    "agent": str,          # Agent name
    "action": str          # Action description
}
```

#### Metrics Object
```python
{
    "total": int,              # Total tasks
    "completed": int,          # Completed count
    "pending": int,            # Pending count
    "delayed": int,            # Delayed count
    "completion_rate": float   # Percentage
}
```

## Configuration Parameters

### LLM Configuration (utils/constants.py)
```python
GROQ_MODEL = "llama3-8b-8192"          # Model ID
GROQ_TEMPERATURE = 0.7                 # 0.0-1.0, higher = more creative
GROQ_MAX_TOKENS = 1024                 # Max response length
```

### Task Configuration
```python
TASK_STATUSES = ["Pending", "Completed", "Delayed"]
PRIORITIES = ["High", "Medium", "Low"]
```

### File Paths
```python
DATA_DIR = "data"
TASKS_FILE = "data/tasks.json"
LOGS_FILE = "data/logs.json"
PROMPTS_DIR = "prompts"
```

### UI Colors
```python
COLOR_SUCCESS = "#00D9FF"      # Cyan
COLOR_WARNING = "#FFA500"      # Orange
COLOR_DANGER = "#FF6B6B"       # Red
COLOR_INFO = "#4ECDC4"         # Teal
```

## Groq API Integration

### Authentication
```python
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
```

### API Parameters
- **Model**: llama3-8b-8192
- **Temperature**: 0.7 (balanced creativity)
- **Max Tokens**: 1024 (response length)

### Error Handling
1. **API Unavailable** → Fallback to mock data
2. **Invalid JSON** → Return empty list
3. **Rate Limiting** → Automatic retry

## Data Persistence

### Task Storage (JSON)
- **File**: `data/tasks.json`
- **Format**: JSON array of task objects
- **Behavior**: Append-only with deduplication

### Audit Logs (JSON)
- **File**: `data/logs.json`
- **Format**: JSON array of log entries
- **Retention**: All entries preserved

### Backup Strategy
```bash
# Manual backup
cp data/tasks.json data/tasks.backup.json
cp data/logs.json data/logs.backup.json

# Export for analysis
# Use Audit Agent export functionality
```

## Streamlit Configuration

### Session State Variables
```python
st.session_state.current_page    # Navigation state
st.session_state.transcript      # Input text
```

### Layout Components
- `st.sidebar` - Navigation menu
- `st.columns()` - Multi-column layouts
- `st.container()` - Grouping
- `st.expander()` - Collapsible sections

## Performance Optimization

### Caching
```python
@st.cache_resource
def init_agents():
    # Agents initialized once per session
    return {...}
```

### Load Limits
- Max transcript length: No hard limit (Groq API default: ~4000 tokens)
- Max tasks per batch: No limit
- Max logs retained: Unlimited (export old logs periodically)

## Security Considerations

1. **API Key**: Store in `.env`, never commit
2. **Data Privacy**: Tasks stored locally in JSON files
3. **Audit Trail**: All actions logged for compliance
4. **Input Validation**: All inputs sanitized before LLM
5. **Error Messages**: No sensitive info exposed

## Scaling Considerations

### For Production
1. Replace JSON with database (PostgreSQL/MongoDB)
2. Add authentication/authorization
3. Implement rate limiting
4. Add caching layer (Redis)
5. Deploy to cloud (AWS/GCP/Azure)
6. Add monitoring/alerting

### Current Limitations
- Single-user (session-based state)
- No database (file-based storage)
- No authentication
- No real-time sync
- No horizontal scaling

## Debugging

### Enable Debug Mode
```python
# Add to app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs
```bash
# View audit logs
cat data/logs.json | python -m json.tool

# View tasks
cat data/tasks.json | python -m json.tool
```

### Test Individual Agents
```python
from agents.understanding_agent import UnderstandingAgent

agent = UnderstandingAgent()
result = agent.process_transcript("Your test transcript")
print(result)
```

## Environment Variables

### Required
```
GROQ_API_KEY=your_api_key_here
```

### Optional
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
LOG_LEVEL=INFO
```

## Dependencies Overview

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web framework |
| groq | 0.4.2 | LLM API client |
| python-dotenv | 1.0.0 | Environment config |
| plotly | 5.17.0 | Charts |
| pandas | 2.1.2 | Data manipulation |
| requests | 2.31.0 | HTTP client |

---

**Last Updated**: March 22, 2026
