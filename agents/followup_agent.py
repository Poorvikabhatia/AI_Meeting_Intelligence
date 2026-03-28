"""
AI Follow-up Agent
- Generates reminder, escalation, and professional follow-up messages for tasks
"""

from datetime import datetime
from typing import Dict, Any


class FollowupAgent:
    """Generate follow-up messages for tasks"""
    
    def __init__(self):
        self.current_time = datetime.now()
    
    def generate_followup_messages(self, task: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate reminder, escalation, and follow-up messages for a task
        
        Args:
            task: Task dictionary with 'title', 'description', 'assigned_to', 'deadline'
            
        Returns:
            Dictionary with reminder, escalation, and followup messages
        """
        task_name = task.get('title', 'Task')
        assigned_to = task.get('assigned_to', 'Team Member')
        description = task.get('description', '')
        deadline = task.get('deadline', 'Not specified')
        
        # Generate Reminder Message
        reminder = self._generate_reminder(task_name, assigned_to, deadline)
        
        # Generate Escalation Message
        escalation = self._generate_escalation(task_name, assigned_to, description)
        
        # Generate Professional Follow-up Message
        followup = self._generate_followup(task_name, assigned_to, deadline, description)
        
        return {
            "reminder": reminder,
            "escalation": escalation,
            "followup": followup
        }
    
    def _generate_reminder(self, task_name: str, assigned_to: str, deadline: str) -> str:
        """Generate a friendly reminder message"""
        return (
            f"Hi {assigned_to},\n\n"
            f"This is a friendly reminder about the task: '{task_name}'\n"
            f"Deadline: {deadline}\n\n"
            f"Please ensure you complete this task on time.\n\n"
            f"Best regards"
        )
    
    def _generate_escalation(self, task_name: str, assigned_to: str, description: str) -> str:
        """Generate an escalation message for overdue tasks"""
        desc_snippet = description[:100] if description else "No description provided"
        return (
            f"⚠️ URGENT ESCALATION NOTICE\n\n"
            f"Hi {assigned_to},\n\n"
            f"The task '{task_name}' requires immediate attention.\n"
            f"Task details: {desc_snippet}{'...' if len(description) > 100 else ''}\n\n"
            f"Please prioritize this task and provide a status update.\n\n"
            f"This is a critical follow-up."
        )
    
    def _generate_followup(self, task_name: str, assigned_to: str, deadline: str, description: str) -> str:
        """Generate a professional follow-up message"""
        desc_snippet = description[:100] if description else "No description provided"
        return (
            f"Dear {assigned_to},\n\n"
            f"I am writing to follow up on the task: '{task_name}'\n\n"
            f"Task Summary:\n"
            f"- Deadline: {deadline}\n"
            f"- Details: {desc_snippet}{'...' if len(description) > 100 else ''}\n\n"
            f"Could you please provide an update on the progress? "
            f"If you have any blockers or need assistance, do not hesitate to reach out.\n\n"
            f"Thank you for your attention to this matter.\n\n"
            f"Best regards"
        )


# Initialize agent instance
followup_agent = FollowupAgent()


def get_followup_messages(task: Dict[str, Any]) -> Dict[str, str]:
    """
    Convenience function to get follow-up messages for a task
    
    Args:
        task: Task dictionary
        
    Returns:
        Dictionary with reminder, escalation, and followup messages
    """
    return followup_agent.generate_followup_messages(task)
