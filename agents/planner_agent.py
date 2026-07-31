"""
planner_agent.py

Planner Agent

Responsibilities
----------------
- Inspect incoming workflow requests
- Select the most appropriate pipeline
- Validate execution requirements
- Build execution plan
- Store planning metadata

Business logic belongs to the processing agents.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    """
    Determines which workflow should execute.
    """

    def __init__(self):

        super().__init__(
            name="PlannerAgent",
            description="Plans workflow execution."
        )

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        logger.info(
            "[PlannerAgent] Planning workflow."
        )

        plan = self.create_plan(context)

        context["plan"] = plan
        context["pipeline"] = plan["pipeline"]
        context["current_agent"] = self.name

        logger.info(
            "[PlannerAgent] Selected pipeline: %s",
            plan["pipeline"],
        )

        return context

    def create_plan(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        workflow = context.get(
            "workflow",
            "standard",
        )

        plan = {
            "created_at": datetime.utcnow().isoformat(),
            "workflow": workflow,
            "pipeline": self.select_pipeline(context),
            "priority": context.get("priority", "normal"),
            "steps": self.build_steps(workflow),
        }

        return plan

    @staticmethod
    def select_pipeline(
            context: Dict[str, Any],
    ) -> str:

        workflow = context.get(
            "workflow",
            "standard",
        ).lower()

        if workflow == "analysis":
            return "analysis"

        if workflow == "report":
            return "report"

        if workflow == "chat":
            return "chat"

        return "standard"

    def build_steps(
        self,
        workflow: str,
    ) -> List[str]:

        mapping = {
            "standard": [
                "upload",
                "audio",
                "transcript",
                "analysis",
                "report",
                "export",
            ],
            "analysis": [
                "analysis",
            ],
            "report": [
                "report",
                "export",
            ],
            "chat": [
                "chat",
            ],
        }

        return mapping.get(
            workflow,
            mapping["standard"],
        )

    def estimate_duration(
        self,
        context: Dict[str, Any],
    ) -> int:
        """
        Estimated execution time (seconds).
        """

        workflow = context.get(
            "workflow",
            "standard",
        )

        estimates = {
            "standard": 180,
            "analysis": 60,
            "report": 30,
            "chat": 5,
        }

        return estimates.get(
            workflow,
            180,
        )

    def validate(
        self,
        context: Dict[str, Any],
    ) -> bool:

        workflow = context.get(
            "workflow",
            "standard",
        )

        supported = {
            "standard",
            "analysis",
            "report",
            "chat",
        }

        return workflow in supported