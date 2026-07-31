"""
dashboard_agent.py

Dashboard Agent

Responsibilities
----------------
- Build dashboard data
- Aggregate workflow statistics
- Summarize execution results
- Track recent workflow activity
- Provide metrics for Streamlit UI

Business logic belongs to services and
processing agents.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class DashboardAgent(BaseAgent):
    """
    Generates dashboard information for the UI.
    """

    def __init__(self):

        super().__init__(
            name="DashboardAgent",
            description="Builds dashboard statistics."
        )

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        logger.info(
            "[DashboardAgent] Building dashboard."
        )

        dashboard = self.build_dashboard(
            context
        )

        context["dashboard"] = dashboard
        context["current_agent"] = self.name

        return context

    def build_dashboard(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        dashboard = {
            "generated_at": datetime.utcnow().isoformat(),
            "status": context.get("status", "unknown"),
            "pipeline": context.get("pipeline"),
            "workflow": context.get("workflow"),
            "progress": self.progress(context),
            "statistics": self.statistics(context),
            "summary": self.summary(context),
            "recent_activity": self.recent_activity(context),
            "alerts": self.alerts(context),
        }

        return dashboard

    def progress(
        self,
        context: Dict[str, Any],
    ) -> float:

        workflow_log = context.get(
            "workflow_log",
            []
        )

        expected = context.get(
            "expected_agents",
            max(len(workflow_log), 1)
        )

        completed = sum(
            1
            for item in workflow_log
            if item.get("status") == "completed"
        )

        return round(
            (completed / expected) * 100,
            2,
        )

    def statistics(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        workflow_log = context.get(
            "workflow_log",
            []
        )

        completed = sum(
            1
            for item in workflow_log
            if item.get("status") == "completed"
        )

        failed = sum(
            1
            for item in workflow_log
            if item.get("status") == "failed"
        )

        return {
            "total_agents": context.get(
                "expected_agents",
                len(workflow_log),
            ),
            "completed_agents": completed,
            "failed_agents": failed,
            "execution_time": context.get(
                "monitor",
                {},
            ).get(
                "execution_time",
                0,
            ),
            "retry_count": sum(
                context.get(
                    "retry_count",
                    {},
                ).values()
            ),
        }

    def summary(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {
            "current_agent": context.get(
                "current_agent"
            ),
            "status": context.get(
                "status"
            ),
            "error": context.get(
                "error"
            ),
        }

    def recent_activity(
        self,
        context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        return context.get(
            "workflow_log",
            []
        )

    def alerts(
        self,
        context: Dict[str, Any],
    ) -> List[Dict[str, str]]:

        alerts = []

        if context.get("status") == "failed":
            alerts.append(
                {
                    "level": "error",
                    "message": context.get(
                        "error",
                        "Workflow failed.",
                    ),
                }
            )

        retry_count = sum(
            context.get(
                "retry_count",
                {},
            ).values()
        )

        if retry_count > 0:
            alerts.append(
                {
                    "level": "warning",
                    "message": (
                        f"{retry_count} retry attempt(s) "
                        "performed."
                    ),
                }
            )

        return alerts

    def clear_dashboard(
        self,
        context: Dict[str, Any],
    ) -> None:

        context["dashboard"] = {}