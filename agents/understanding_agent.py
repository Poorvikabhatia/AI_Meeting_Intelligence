"""
Understanding Agent - Processes meeting transcript using LLM
"""

from typing import List, Dict
from services.llm_service import LLMService
from services.parser import TaskParser
from utils.helpers import add_log


# Mock data fallback
MOCK_TASKS = [
    {
        "task": "Prepare the sales report",
        "owner": "Rahul",
        "deadline": "2026-03-26",
        "priority": "High"
    },
    {
        "task": "Finalize the presentation",
        "owner": "Priya",
        "deadline": "2026-03-23",
        "priority": "High"
    },
    {
        "task": "Contact the client",
        "owner": "Amit",
        "deadline": "2026-03-29",
        "priority": "Medium"
    }
]


class UnderstandingAgent:
    def __init__(self):
        try:
            self.llm_service = LLMService()
            self.use_api = True
        except ValueError:
            print("Warning: Groq API not configured, using mock data")
            self.use_api = False
        self.parser = TaskParser()

    def process_transcript(self, transcript: str) -> List[Dict]:
        """
        Process meeting transcript and extract tasks
        Returns list of validated task dictionaries
        """
        if not transcript or not transcript.strip():
            add_log("Understanding Agent", "Empty transcript received")
            return []

        try:
            if self.use_api:
                tasks = self.llm_service.extract_tasks(transcript)
                validated = self.parser.parse_tasks(tasks)
                add_log("Understanding Agent", f"Extracted {len(validated)} tasks using API")
                return validated
            
            # Fallback to mock data
            tasks = self.parser.parse_tasks(MOCK_TASKS)
            add_log("Understanding Agent", f"Used mock data: {len(tasks)} tasks")
            return tasks

        except Exception as e:
            print(f"Error in Understanding Agent: {e}")
            add_log("Understanding Agent", f"Error: {str(e)}")
            return self.parser.parse_tasks(MOCK_TASKS)

    def validate_tasks(self, tasks: List[Dict]) -> bool:
        """
        Validate extracted tasks
        """
        return all(self.parser.validate_task(task) for task in tasks)
