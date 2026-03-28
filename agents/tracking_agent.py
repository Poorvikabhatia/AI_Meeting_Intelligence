"""
Tracking Agent - Computes task metrics
"""

from typing import Dict
from utils.helpers import load_tasks, add_log


class TrackingAgent:
    def __init__(self):
        pass

    def calculate_metrics(self) -> Dict:
        """
        Calculate task metrics
        """
        try:
            tasks = load_tasks()
            
            total_tasks = len(tasks)
            completed_tasks = len([t for t in tasks if t.get("status") == "Completed"])
            pending_tasks = len([t for t in tasks if t.get("status") == "Pending"])
            delayed_tasks = len([t for t in tasks if t.get("status") == "Delayed"])
            
            metrics = {
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": pending_tasks,
                "delayed": delayed_tasks,
                "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            }
            
            add_log("Tracking Agent", f"Calculated metrics: {total_tasks} total, {completed_tasks} completed")
            return metrics
        except Exception as e:
            print(f"Error calculating metrics: {e}")
            add_log("Tracking Agent", f"Error calculating metrics: {str(e)}")
            return {
                "total": 0,
                "completed": 0,
                "pending": 0,
                "delayed": 0,
                "completion_rate": 0
            }

    def get_task_distribution(self) -> Dict:
        """
        Get task distribution by priority and status
        """
        try:
            tasks = load_tasks()
            
            distribution = {
                "by_priority": {
                    "High": len([t for t in tasks if t.get("priority") == "High"]),
                    "Medium": len([t for t in tasks if t.get("priority") == "Medium"]),
                    "Low": len([t for t in tasks if t.get("priority") == "Low"])
                },
                "by_status": {
                    "Pending": len([t for t in tasks if t.get("status") == "Pending"]),
                    "Completed": len([t for t in tasks if t.get("status") == "Completed"]),
                    "Delayed": len([t for t in tasks if t.get("status") == "Delayed"])
                },
                "by_owner": {}
            }
            
            # Count by owner
            for task in tasks:
                owner = task.get("owner", "Unassigned")
                distribution["by_owner"][owner] = distribution["by_owner"].get(owner, 0) + 1
            
            return distribution
        except Exception as e:
            print(f"Error getting distribution: {e}")
            add_log("Tracking Agent", f"Error getting distribution: {str(e)}")
            return {
                "by_priority": {"High": 0, "Medium": 0, "Low": 0},
                "by_status": {"Pending": 0, "Completed": 0, "Delayed": 0},
                "by_owner": {}
            }
