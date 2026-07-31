"""
monitor_agent.py

Monitor Agent

Responsibilities
----------------
- Monitor workflow execution
- Track agent status
- Measure execution time
- Record workflow metrics
- Detect failures
- Provide runtime statistics

Business logic belongs to individual agents.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class MonitorAgent(BaseAgent):
    """
    Monitors workflow execution.
    """

    def __init__(self):

        super().__init__(
            name="MonitorAgent",
            description="Monitors workflow execution.",
        )

    def execute(
            self,
            context: Dict[str, Any],
    ) -> Dict[str, Any]:

        logger.info(
            "[MonitorAgent] Monitoring workflow."
        )

        # Ensure context is a dictionary
        if not isinstance(context, dict):
            context = {}

        # Create monitor dictionary if it doesn't exist
        monitor = context.setdefault(
            "monitor",
            {},
        )

        monitor["last_updated"] = (
            datetime.utcnow().isoformat()
        )

        monitor["status"] = context.get(
            "status",
            "unknown",
        )

        monitor["current_agent"] = context.get(
            "current_agent",
        )

        monitor["completed_agents"] = len(
            self.completed_agents(context)
        )

        monitor["failed"] = (
                context.get("status") == "failed"
        )

        monitor["progress"] = self.progress(
            context
        )

        monitor["execution_time"] = (
            self.execution_time(context)
        )

        monitor["workflow_log"] = context.get(
            "workflow_log",
            [],
        )

        context["current_agent"] = self.name

        return context

    def progress(
        self,
        context: Dict[str, Any],
    ) -> float:
        """
        Calculate workflow completion percentage.
        """

        workflow = context.get(
            "workflow_log",
            []
        )

        total = context.get(
            "expected_agents",
            6,
        )

        if total <= 0:
            return 0.0

        completed = len(
            [
                item
                for item in workflow
                if item.get("status") == "completed"
            ]
        )

        return round(
            (completed / total) * 100,
            2,
        )

    def completed_agents(
        self,
        context: Dict[str, Any],
    ) -> List[str]:

        return [
            item["agent"]
            for item in context.get(
                "workflow_log",
                []
            )
            if item.get("status") == "completed"
        ]

    def failed_agents(
        self,
        context: Dict[str, Any],
    ) -> List[str]:

        return [
            item["agent"]
            for item in context.get(
                "workflow_log",
                []
            )
            if item.get("status") == "failed"
        ]

    def execution_time(
        self,
        context: Dict[str, Any],
    ) -> float:
        """
        Return elapsed workflow time in seconds.
        """

        started = context.get(
            "started_at",
        )

        if not started:
            return 0.0

        try:

            start = datetime.fromisoformat(
                started
            )

            return round(
                (
                    datetime.utcnow() - start
                ).total_seconds(),
                2,
            )

        except Exception:

            return 0.0

    def is_running(
        self,
        context: Dict[str, Any],
    ) -> bool:

        return (
            context.get("status")
            == "running"
        )

    def is_completed(
        self,
        context: Dict[str, Any],
    ) -> bool:

        return (
            context.get("status")
            == "completed"
        )

    def is_failed(
        self,
        context: Dict[str, Any],
    ) -> bool:

        return (
            context.get("status")
            == "failed"
        )

    def summary(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {
            "status": context.get("status"),
            "progress": self.progress(
                context
            ),
            "completed_agents": self.completed_agents(
                context
            ),
            "failed_agents": self.failed_agents(
                context
            ),
            "execution_time": self.execution_time(
                context
            ),
        }