"""
Escalation Agent - Monitors task deadlines and escalates overdue tasks
"""

from datetime import datetime
from typing import List, Dict
from utils.helpers import load_tasks, save_tasks, add_log


class EscalationAgent:
    def __init__(self):
        pass

    def check_deadlines(self) -> Dict:
        """
        Check for overdue tasks and escalate them
        """
        try:
            tasks = load_tasks()
            today = datetime.now().date()
            
            escalated_count = 0
            alerts = []
            
            for task in tasks:
                if task.get("status") in ["Pending", "Completed"]:
                    continue
                
                deadline_str = task.get("deadline", "")
                if deadline_str and deadline_str != "Not specified":
                    try:
                        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                        if deadline < today and task.get("status") != "Completed":
                            task["status"] = "Delayed"
                            escalated_count += 1
                            alerts.append({
                                "task": task.get("task"),
                                "owner": task.get("owner"),
                                "deadline": deadline_str,
                                "days_overdue": (today - deadline).days
                            })
                    except ValueError:
                        pass
            
            if escalated_count > 0:
                save_tasks(tasks)
                add_log("Escalation Agent", f"Escalated {escalated_count} overdue tasks")
            
            return {
                "escalated_count": escalated_count,
                "alerts": alerts
            }
        except Exception as e:
            print(f"Error in escalation check: {e}")
            add_log("Escalation Agent", f"Error checking deadlines: {str(e)}")
            return {
                "escalated_count": 0,
                "alerts": []
            }

    def get_urgent_tasks(self) -> List[Dict]:
        """
        Get all urgent/delayed tasks
        """
        try:
            tasks = load_tasks()
            urgent = [t for t in tasks if t.get("status") == "Delayed" or t.get("priority") == "High"]
            return urgent
        except Exception as e:
            print(f"Error getting urgent tasks: {e}")
            add_log("Escalation Agent", f"Error retrieving urgent tasks: {str(e)}")
            return []

    def generate_escalation_alert(self, task: Dict) -> str:
        """
        Generate an alert message for escalated task
        """
        task_name = task.get("task", "Unknown task")
        owner = task.get("owner", "Unassigned")
        deadline = task.get("deadline", "Not specified")
        
        return f"⚠️ ESCALATION ALERT: Task '{task_name}' assigned to {owner} is overdue (deadline: {deadline})"
