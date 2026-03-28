"""
Audit Agent - Logs all system activities
"""

from typing import List, Dict
from utils.helpers import load_logs, add_log as write_log


class AuditAgent:
    def __init__(self):
        pass

    def get_all_logs(self) -> List[Dict]:
        """
        Retrieve all audit logs
        """
        try:
            logs = load_logs()
            write_log("Audit Agent", f"Retrieved {len(logs)} audit logs")
            return logs
        except Exception as e:
            print(f"Error loading logs: {e}")
            return []

    def get_logs_by_agent(self, agent_name: str) -> List[Dict]:
        """
        Get logs from a specific agent
        """
        try:
            logs = load_logs()
            filtered = [l for l in logs if l.get("agent") == agent_name]
            return filtered
        except Exception as e:
            print(f"Error filtering logs: {e}")
            return []

    def get_recent_logs(self, count: int = 20) -> List[Dict]:
        """
        Get most recent logs
        """
        try:
            logs = load_logs()
            return logs[-count:] if len(logs) > count else logs
        except Exception as e:
            print(f"Error getting recent logs: {e}")
            return []

    def export_logs(self, format: str = "json") -> str:
        """
        Export logs in specified format
        """
        try:
            logs = load_logs()
            if format == "json":
                import json
                return json.dumps(logs, indent=2)
            elif format == "csv":
                import csv
                from io import StringIO
                output = StringIO()
                if logs:
                    writer = csv.DictWriter(output, fieldnames=["timestamp", "agent", "action"])
                    writer.writeheader()
                    writer.writerows(logs)
                return output.getvalue()
            else:
                return ""
        except Exception as e:
            print(f"Error exporting logs: {e}")
            return ""

    def clear_logs(self) -> bool:
        """
        Clear all audit logs
        """
        try:
            from utils.helpers import save_logs
            save_logs([])
            write_log("Audit Agent", "Cleared all audit logs")
            return True
        except Exception as e:
            print(f"Error clearing logs: {e}")
            return False

    def get_log_summary(self) -> Dict:
        """
        Get summary of audit logs
        """
        try:
            logs = load_logs()
            agents = {}
            
            for log in logs:
                agent = log.get("agent", "Unknown")
                agents[agent] = agents.get(agent, 0) + 1
            
            return {
                "total_logs": len(logs),
                "agents": agents,
                "first_log": logs[0] if logs else None,
                "last_log": logs[-1] if logs else None
            }
        except Exception as e:
            print(f"Error getting log summary: {e}")
            return {
                "total_logs": 0,
                "agents": {},
                "first_log": None,
                "last_log": None
            }
