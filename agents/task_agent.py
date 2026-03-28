"""
Task Agent - Manages task storage and retrieval
"""

from typing import List, Dict
from utils.helpers import load_tasks, save_tasks, add_log
from services.parser import TaskParser


class TaskAgent:
    def __init__(self):
        self.parser = TaskParser()

    def store_tasks(self, tasks: List[Dict]) -> bool:
        """
        Store tasks in persistent storage (ALWAYS OVERWRITE, not append)
        """
        try:
            # Add default status if not provided
            for task in tasks:
                if "status" not in task:
                    task["status"] = "Pending"
            
            # ALWAYS overwrite - don't append
            save_tasks(tasks)
            
            add_log("Task Agent", f"Stored {len(tasks)} tasks (overwrote previous tasks)")
            return True
        except Exception as e:
            print(f"Error storing tasks: {e}")
            add_log("Task Agent", f"Error storing tasks: {str(e)}")
            return False
    
    def clear_tasks(self) -> bool:
        """
        Clear all tasks from persistent storage
        """
        try:
            save_tasks([])
            add_log("Task Agent", "Cleared all tasks")
            return True
        except Exception as e:
            print(f"Error clearing tasks: {e}")
            add_log("Task Agent", f"Error clearing tasks: {str(e)}")
            return False

    def get_all_tasks(self) -> List[Dict]:
        """
        Retrieve all stored tasks
        """
        try:
            tasks = load_tasks()
            add_log("Task Agent", f"Retrieved {len(tasks)} tasks")
            return tasks
        except Exception as e:
            print(f"Error loading tasks: {e}")
            add_log("Task Agent", f"Error loading tasks: {str(e)}")
            return []

    def update_task_status(self, task_name: str, new_status: str) -> bool:
        """
        Update status of a specific task
        """
        try:
            tasks = load_tasks()
            for task in tasks:
                if task.get("task") == task_name:
                    task["status"] = new_status
                    save_tasks(tasks)
                    add_log("Task Agent", f"Updated task '{task_name}' status to {new_status}")
                    return True
            return False
        except Exception as e:
            print(f"Error updating task: {e}")
            add_log("Task Agent", f"Error updating task: {str(e)}")
            return False

    def delete_task(self, task_name: str) -> bool:
        """
        Delete a task
        """
        try:
            tasks = load_tasks()
            original_count = len(tasks)
            tasks = [t for t in tasks if t.get("task") != task_name]
            
            if len(tasks) < original_count:
                save_tasks(tasks)
                add_log("Task Agent", f"Deleted task '{task_name}'")
                return True
            return False
        except Exception as e:
            print(f"Error deleting task: {e}")
            add_log("Task Agent", f"Error deleting task: {str(e)}")
            return False

    def filter_tasks(self, owner: str = None, status: str = None) -> List[Dict]:
        """
        Filter tasks by owner or status
        """
        try:
            tasks = load_tasks()
            filtered = tasks
            
            if owner:
                filtered = [t for t in filtered if t.get("owner", "").lower() == owner.lower()]
            
            if status:
                filtered = [t for t in filtered if t.get("status", "").lower() == status.lower()]
            
            return filtered
        except Exception as e:
            print(f"Error filtering tasks: {e}")
            return []
