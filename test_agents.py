"""
Test file for AI Meeting Intelligence System
Run with: pytest test_agents.py
"""

import pytest
import json
from datetime import datetime, timedelta
from agents.understanding_agent import UnderstandingAgent
from agents.task_agent import TaskAgent
from agents.tracking_agent import TrackingAgent
from agents.escalation_agent import EscalationAgent
from agents.audit_agent import AuditAgent
from services.parser import TaskParser
from utils.helpers import load_tasks, save_tasks, load_logs


class TestTaskParser:
    """Test TaskParser functionality"""
    
    def test_parse_valid_tasks(self):
        """Test parsing valid task JSON"""
        raw_data = [
            {
                "task": "Complete report",
                "owner": "John",
                "deadline": "2026-03-25",
                "priority": "High"
            }
        ]
        
        parsed = TaskParser.parse_tasks(raw_data)
        assert len(parsed) == 1
        assert parsed[0]["task"] == "Complete report"
        assert parsed[0]["status"] == "Pending"
    
    def test_parse_string_json(self):
        """Test parsing JSON string"""
        json_str = '[{"task": "Task 1", "owner": "Alice", "deadline": "2026-03-25", "priority": "High"}]'
        parsed = TaskParser.parse_tasks(json_str)
        assert len(parsed) == 1
    
    def test_parse_invalid_json(self):
        """Test handling invalid JSON"""
        parsed = TaskParser.parse_tasks("{invalid json")
        assert parsed == []
    
    def test_validate_task(self):
        """Test task validation"""
        valid_task = {
            "task": "Task",
            "owner": "Owner",
            "deadline": "2026-03-25",
            "priority": "High"
        }
        assert TaskParser.validate_task(valid_task) == True
        
        invalid_task = {"task": "Task"}
        assert TaskParser.validate_task(invalid_task) == False


class TestUnderstandingAgent:
    """Test Understanding Agent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        agent = UnderstandingAgent()
        assert agent is not None
    
    def test_process_empty_transcript(self):
        """Test handling empty transcript"""
        agent = UnderstandingAgent()
        result = agent.process_transcript("")
        assert isinstance(result, list)
    
    def test_process_transcript_with_fallback(self):
        """Test fallback to mock data"""
        agent = UnderstandingAgent()
        transcript = "Someone will do something by some date"
        result = agent.process_transcript(transcript)
        
        # Should have mock data
        assert isinstance(result, list)
        # Can't rely on API, but should have something
        assert all("task" in t for t in result)
    
    def test_validate_tasks(self):
        """Test task validation"""
        agent = UnderstandingAgent()
        tasks = [
            {
                "task": "Task 1",
                "owner": "Owner 1",
                "deadline": "2026-03-25",
                "priority": "High"
            }
        ]
        assert agent.validate_tasks(tasks) == True


class TestTaskAgent:
    """Test Task Manager Agent"""
    
    def test_store_and_retrieve(self):
        """Test storing and retrieving tasks"""
        agent = TaskAgent()
        
        test_tasks = [
            {
                "task": "Test Task",
                "owner": "Test Owner",
                "deadline": "2026-03-25",
                "priority": "High",
                "status": "Pending",
                "created_at": datetime.now().isoformat()
            }
        ]
        
        agent.store_tasks(test_tasks)
        retrieved = agent.get_all_tasks()
        
        assert len(retrieved) > 0
        task_names = [t.get("task") for t in retrieved]
        assert "Test Task" in task_names
    
    def test_update_status(self):
        """Test updating task status"""
        agent = TaskAgent()
        tasks = load_tasks()
        
        if tasks:
            first_task = tasks[0].get("task")
            agent.update_task_status(first_task, "Completed")
            updated_tasks = load_tasks()
            status = [t.get("status") for t in updated_tasks if t.get("task") == first_task][0]
            assert status == "Completed"
    
    def test_filter_by_owner(self):
        """Test filtering tasks by owner"""
        agent = TaskAgent()
        filtered = agent.filter_tasks(owner="Test Owner")
        assert isinstance(filtered, list)
    
    def test_filter_by_status(self):
        """Test filtering tasks by status"""
        agent = TaskAgent()
        filtered = agent.filter_tasks(status="Pending")
        assert isinstance(filtered, list)
        assert all(t.get("status") == "Pending" for t in filtered)


class TestTrackingAgent:
    """Test Tracking Agent"""
    
    def test_calculate_metrics(self):
        """Test metrics calculation"""
        agent = TrackingAgent()
        metrics = agent.calculate_metrics()
        
        assert "total" in metrics
        assert "completed" in metrics
        assert "pending" in metrics
        assert "delayed" in metrics
        assert "completion_rate" in metrics
        assert 0 <= metrics["completion_rate"] <= 100
    
    def test_get_distribution(self):
        """Test getting task distribution"""
        agent = TrackingAgent()
        dist = agent.get_task_distribution()
        
        assert "by_priority" in dist
        assert "by_status" in dist
        assert "by_owner" in dist


class TestEscalationAgent:
    """Test Escalation Agent"""
    
    def test_check_deadlines(self):
        """Test deadline checking"""
        agent = EscalationAgent()
        result = agent.check_deadlines()
        
        assert "escalated_count" in result
        assert "alerts" in result
        assert isinstance(result["escalated_count"], int)
        assert isinstance(result["alerts"], list)
    
    def test_get_urgent_tasks(self):
        """Test getting urgent tasks"""
        agent = EscalationAgent()
        urgent = agent.get_urgent_tasks()
        assert isinstance(urgent, list)
    
    def test_generate_alert(self):
        """Test alert generation"""
        agent = EscalationAgent()
        task = {
            "task": "Urgent Task",
            "owner": "John",
            "deadline": "2026-03-20"
        }
        alert = agent.generate_escalation_alert(task)
        assert "ESCALATION ALERT" in alert
        assert "Urgent Task" in alert


class TestAuditAgent:
    """Test Audit Agent"""
    
    def test_get_all_logs(self):
        """Test retrieving all logs"""
        agent = AuditAgent()
        logs = agent.get_all_logs()
        assert isinstance(logs, list)
    
    def test_get_recent_logs(self):
        """Test getting recent logs"""
        agent = AuditAgent()
        recent = agent.get_recent_logs(count=10)
        assert isinstance(recent, list)
        assert len(recent) <= 10
    
    def test_get_log_summary(self):
        """Test log summary"""
        agent = AuditAgent()
        summary = agent.get_log_summary()
        
        assert "total_logs" in summary
        assert "agents" in summary
        assert "first_log" in summary
        assert "last_log" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
