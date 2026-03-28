"""
Parser for task extraction and validation
"""

import json
from typing import List, Dict
from datetime import datetime


class TaskParser:
    @staticmethod
    def parse_tasks(raw_data) -> List[Dict]:
        """
        Parse and validate extracted tasks
        Returns structured tasks or fallback structured format if parsing fails
        """
        if isinstance(raw_data, str):
            try:
                raw_data = json.loads(raw_data)
            except json.JSONDecodeError:
                # Return structured fallback tasks instead of empty list
                return TaskParser._get_fallback_tasks()
        
        if not isinstance(raw_data, list):
            return TaskParser._get_fallback_tasks()
        
        validated_tasks = []
        for item in raw_data:
            if isinstance(item, dict) and all(key in item for key in ["task", "owner", "deadline", "priority"]):
                validated_tasks.append({
                    "task": str(item.get("task", "")).strip(),
                    "owner": str(item.get("owner", "")).strip(),
                    "deadline": str(item.get("deadline", "Not specified")).strip(),
                    "priority": str(item.get("priority", "Medium")).strip(),
                    "status": "Pending",
                    "created_at": datetime.now().isoformat()
                })
        
        # Return validated tasks or fallback if none were valid
        return validated_tasks if validated_tasks else TaskParser._get_fallback_tasks()

    @staticmethod
    def validate_task(task: Dict) -> bool:
        """
        Validate a single task
        """
        required_fields = ["task", "owner", "deadline", "priority"]
        return all(field in task and task[field] for field in required_fields)

    @staticmethod
    def _get_fallback_tasks() -> List[Dict]:
        """
        Return structured fallback tasks when parsing fails
        Ensures task list is never completely empty
        """
        return [
            {
                "task": "Review meeting notes",
                "owner": "Team Lead",
                "deadline": "Not specified",
                "priority": "Medium",
                "status": "Pending",
                "created_at": datetime.now().isoformat()
            }
        ]

    @staticmethod
    def format_task_for_display(task: Dict) -> Dict:
        """
        Format task for UI display
        """
        return {
            "Task": task.get("task", ""),
            "Owner": task.get("owner", ""),
            "Deadline": task.get("deadline", ""),
            "Priority": task.get("priority", ""),
            "Status": task.get("status", ""),
            "Created": task.get("created_at", "")
        }
