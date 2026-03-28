"""
Constants and configuration for AI Meeting Intelligence System
"""

GROQ_MODEL = "llama3-8b-8192"
GROQ_TEMPERATURE = 0
GROQ_MAX_TOKENS = 1024

TASK_STATUSES = ["Pending", "Completed", "Delayed"]
PRIORITIES = ["High", "Medium", "Low"]

# File paths
DATA_DIR = "data"
TASKS_FILE = f"{DATA_DIR}/tasks.json"
LOGS_FILE = f"{DATA_DIR}/logs.json"
PROMPTS_DIR = "prompts"

# UI Theme colors
COLOR_SUCCESS = "#00D9FF"
COLOR_WARNING = "#FFA500"
COLOR_DANGER = "#FF6B6B"
COLOR_INFO = "#4ECDC4"
