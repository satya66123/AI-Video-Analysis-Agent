"""
AI Video Analysis Agent Package

This package contains all autonomous agents responsible for orchestrating
the AI Video Analysis workflow.

Agent Architecture
------------------
SupervisorAgent
    └── PlannerAgent
            └── WorkflowAgent
                    ├── UploadAgent
                    ├── AudioAgent
                    ├── TranscriptAgent
                    ├── AnalysisAgent
                    ├── ReportAgent
                    ├── ExportAgent
                    ├── ChatAgent
                    ├── DashboardAgent
                    ├── NotificationAgent
                    ├── MonitorAgent
                    └── RecoveryAgent

Each agent inherits from BaseAgent and performs one specific responsibility.
Business logic should remain inside the services layer, while agents
coordinate execution and workflow.
"""

from .base_agent import BaseAgent
from .agent_manager import AgentManager
from .workflow_agent import WorkflowAgent
from .supervisor_agent import SupervisorAgent
from .planner_agent import PlannerAgent

from .upload_agent import UploadAgent
from .audio_agent import AudioAgent
from .transcript_agent import TranscriptAgent
from .analysis_agent import AnalysisAgent
from .report_agent import ReportAgent
from .export_agent import ExportAgent

from .chat_agent import ChatAgent
from .dashboard_agent import DashboardAgent
from .notification_agent import NotificationAgent
from .monitor_agent import MonitorAgent
from .recovery_agent import RecoveryAgent

__all__ = [
    "BaseAgent",
    "AgentManager",
    "WorkflowAgent",
    "SupervisorAgent",
    "PlannerAgent",
    "UploadAgent",
    "AudioAgent",
    "TranscriptAgent",
    "AnalysisAgent",
    "ReportAgent",
    "ExportAgent",
    "ChatAgent",
    "DashboardAgent",
    "NotificationAgent",
    "MonitorAgent",
    "RecoveryAgent",
]

__version__ = "1.0.0"

AGENT_PACKAGE_NAME = "AI Video Analysis Agents"

SUPPORTED_AGENTS = [
    "SupervisorAgent",
    "PlannerAgent",
    "WorkflowAgent",
    "UploadAgent",
    "AudioAgent",
    "TranscriptAgent",
    "AnalysisAgent",
    "ReportAgent",
    "ExportAgent",
    "ChatAgent",
    "DashboardAgent",
    "NotificationAgent",
    "MonitorAgent",
    "RecoveryAgent",
]