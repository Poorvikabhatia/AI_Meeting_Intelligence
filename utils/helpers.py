"""
Helper functions for AI Meeting Intelligence System
"""

import json
import os
from datetime import datetime
from utils.constants import DATA_DIR, TASKS_FILE, LOGS_FILE


def ensure_data_directories():
    """Create data directory if it doesn't exist"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_tasks():
    """Load tasks from JSON file"""
    ensure_data_directories()
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_tasks(tasks):
    """Save tasks to JSON file"""
    ensure_data_directories()
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def load_logs():
    """Load audit logs from JSON file"""
    ensure_data_directories()
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_logs(logs):
    """Save audit logs to JSON file"""
    ensure_data_directories()
    with open(LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def add_log(agent: str, action: str):
    """Add a log entry"""
    logs = load_logs()
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "action": action
    })
    save_logs(logs)


def get_current_timestamp():
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()


def parse_date(date_string):
    """Parse various date formats"""
    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_string.strip(), fmt)
        except ValueError:
            continue
    return None
