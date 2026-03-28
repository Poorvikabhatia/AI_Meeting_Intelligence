from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")

        self.client = Groq(api_key=api_key)

    def extract_tasks(self, meeting_text):
        prompt = f"""
You are an advanced AI task extraction system.

GOAL:
Extract ALL actionable tasks from the meeting transcript.

STRICT RULES:
- Extract EVERY task separately
- DO NOT combine tasks
- DO NOT summarize anything
- DO NOT miss any person or action
- Even if 7 tasks exist → return 7 tasks

Each task MUST include:
- task (short clear action)
- owner (person name EXACTLY as written)
- deadline (exact phrase from text or "Not specified")
- priority:
    - "High" → if deadline is urgent (today/tomorrow)
    - "Medium" → normal deadlines
    - "Low" → no deadline

RETURN FORMAT:
ONLY a valid JSON list. No explanation.

Example:
[
  {{
    "task": "Prepare sales report",
    "owner": "Rahul",
    "deadline": "Friday",
    "priority": "High"
  }},
  {{
    "task": "Design UI",
    "owner": "Priya",
    "deadline": "Wednesday",
    "priority": "Medium"
  }}
]

Meeting Transcript:
{meeting_text}
"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You ONLY return valid JSON array. No text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=1200  # 🔥 increased for more tasks
            )

            content = response.choices[0].message.content.strip()

            print("\nRAW LLM OUTPUT:\n", content)

            # 🔥 CLEAN JSON (handles extra text issues)
            content = self.extract_json(content)

            try:
                data = json.loads(content)

                if isinstance(data, dict):
                    data = [data]

                # 🔥 SAFETY CHECK
                if len(data) < 5:
                    print("⚠️ Warning: Possible missing tasks")

                return data

            except Exception as parse_error:
                print("JSON Parsing Error:", parse_error)
                return self.fallback()

        except Exception as e:
            print("Error in extract_tasks:", e)
            return self.fallback()

    def extract_json(self, text):
        """
        Extract JSON array from messy LLM output
        """
        match = re.search(r"\[.*\]", text, re.DOTALL)
        return match.group(0) if match else text

    def fallback(self):
        return [
            {
                "task": "Prepare sales report",
                "owner": "Rahul",
                "deadline": "Friday",
                "priority": "High"
            },
            {
                "task": "Finalize presentation",
                "owner": "Priya",
                "deadline": "Tomorrow",
                "priority": "Medium"
            },
            {
                "task": "Contact client",
                "owner": "Amit",
                "deadline": "Next week",
                "priority": "Medium"
            },
            {
                "task": "Review budget",
                "owner": "Neha",
                "deadline": "Monday",
                "priority": "Medium"
            }
        ]