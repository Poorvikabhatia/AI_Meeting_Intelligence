"""
Deadline Intelligence Agent
- Analyzes deadline text and classifies task urgency
- Detects overdue tasks
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple
import re


class DeadlineAgent:
    """Analyze deadlines and determine urgency levels"""
    
    def __init__(self):
        self.current_date = datetime.now()
    
    def analyze_deadline(self, deadline_text: str, created_date: str = None) -> Dict[str, any]:
        """
        Analyze deadline text and classify urgency
        
        Args:
            deadline_text: String describing the deadline (e.g., "Tomorrow", "Next week")
            created_date: ISO format date string when task was created
            
        Returns:
            Dictionary with urgency level and overdue status
        """
        urgency = self._classify_urgency(deadline_text)
        is_overdue = self._check_overdue(deadline_text, created_date)
        
        return {
            "urgency": urgency,
            "is_overdue": is_overdue,
            "deadline_text": deadline_text
        }
    
    def _classify_urgency(self, deadline_text: str) -> str:
        """
        Classify deadline urgency based on text
        
        Returns: "Critical", "Urgent", "Normal", or "Low Priority"
        """
        deadline_lower = deadline_text.lower().strip()
        
        # Critical - Today or due date has passed
        if any(keyword in deadline_lower for keyword in ['today', 'asap', 'immediately', 'emergency', 'critical', 'right now']):
            return "Critical"
        
        # Urgent - Tomorrow or in a few days
        if any(keyword in deadline_lower for keyword in ['tomorrow', 'urgent', 'this week', 'in 1 day', 'in 2 days', 'in 3 days']):
            return "Urgent"
        
        # Normal - Next week or specific dates within 2-3 weeks
        if any(keyword in deadline_lower for keyword in ['next week', 'upcoming', 'soon', 'in a week', 'in 10 days']):
            return "Normal"
        
        # Low priority - Future or unspecified
        if any(keyword in deadline_lower for keyword in ['not specified', 'none', 'whenever', 'flexible', 'tbd', 'later', 'month']):
            return "Low Priority"
        
        # Try to parse date patterns (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD)
        urgency_from_date = self._parse_date_urgency(deadline_text)
        if urgency_from_date:
            return urgency_from_date
        
        # Default classification
        return "Normal"
    
    def _parse_date_urgency(self, deadline_text: str) -> str:
        """Try to parse date strings and classify urgency"""
        # Common date patterns
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
            r'\d{4}-\d{2}-\d{2}',       # YYYY-MM-DD
            r'\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}',  # 1 Jan 2024
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, deadline_text)
            if match:
                try:
                    date_str = match.group(0)
                    # Try different formats
                    for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%d %b %Y', '%d %B %Y']:
                        try:
                            deadline_date = datetime.strptime(date_str, fmt)
                            days_until = (deadline_date - self.current_date).days
                            
                            if days_until <= 0:
                                return "Critical"
                            elif days_until <= 1:
                                return "Critical"
                            elif days_until <= 3:
                                return "Urgent"
                            elif days_until <= 7:
                                return "Normal"
                            else:
                                return "Low Priority"
                        except ValueError:
                            continue
                except:
                    pass
        
        return None
    
    def _check_overdue(self, deadline_text: str, created_date: str = None) -> bool:
        """
        Check if a task is overdue
        
        Args:
            deadline_text: Deadline description text
            created_date: When task was created (ISO format)
            
        Returns:
            True if task is overdue, False otherwise
        """
        deadline_lower = deadline_text.lower().strip()
        
        # Check for explicit overdue indicators
        if any(keyword in deadline_lower for keyword in ['past', 'overdue', 'expired', 'missed', 'late']):
            return True
        
        # Check if deadline text indicates past date
        if any(keyword in deadline_lower for keyword in ['yesterday', 'last week', 'last month']):
            return True
        
        # Try to parse date and compare
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}-\d{2}-\d{2}',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, deadline_text)
            if match:
                try:
                    date_str = match.group(0)
                    for fmt in ['%m/%d/%Y', '%Y-%m-%d']:
                        try:
                            deadline_date = datetime.strptime(date_str, fmt)
                            if deadline_date < self.current_date:
                                return True
                        except ValueError:
                            continue
                except:
                    pass
        
        return False
    
    def get_urgency_emoji(self, urgency: str) -> str:
        """Get emoji for urgency level"""
        urgency_map = {
            "Critical": "🔴",
            "Urgent": "🟡",
            "Normal": "🟢",
            "Low Priority": "⚪"
        }
        return urgency_map.get(urgency, "⚪")


# Initialize agent instance
deadline_agent = DeadlineAgent()


def analyze_deadline(deadline_text: str, created_date: str = None) -> Dict[str, any]:
    """
    Convenience function to analyze a deadline
    
    Args:
        deadline_text: Deadline description text
        created_date: When task was created (ISO format)
        
    Returns:
        Dictionary with urgency level and overdue status
    """
    return deadline_agent.analyze_deadline(deadline_text, created_date)


def get_urgency_emoji(urgency: str) -> str:
    """
    Convenience function to get urgency emoji
    
    Args:
        urgency: Urgency level string
        
    Returns:
        Emoji representing urgency
    """
    return deadline_agent.get_urgency_emoji(urgency)
