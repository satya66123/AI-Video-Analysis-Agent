"""
supervisor_agent.py

Supervisor Agent

Responsibilities
----------------
- Supervise workflow execution
- Validate workflow context
- Coordinate workflow execution
- Track workflow lifecycle
- Handle unexpected failures

Business logic belongs to WorkflowAgent
and the individual processing agents.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict

from .base_agent import BaseAgent
from .workflow_agent import WorkflowAgent

logger = logging.getLogger(__name__)


def workflow_failed(
        context: Dict[str, Any],
) -> bool:
    """
    Check if workflow failed.
    """

    return (
        context.get("status")
        == "failed"
    )


class SupervisorAgent(BaseAgent):
    """
    High-level supervisor responsible for
    coordinating workflow execution.
    """

    def __init__(
        self,
        workflow_agent: WorkflowAgent,
    ):

        super().__init__(
            name="SupervisorAgent",
            description="Supervises AI workflow execution.",
        )

        self.workflow_agent = workflow_agent

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        logger.info(
            "[SupervisorAgent] Starting supervision."
        )



        context["supervisor"]["started_at"] = (
            datetime.utcnow().isoformat()
        )

        context["supervisor"]["status"] = (
            "running"
        )

        try:

            context = self.workflow_agent.execute(
                context
            )

            context["supervisor"]["status"] = (
                "completed"
            )

            logger.info(
                "[SupervisorAgent] Workflow completed."
            )

        except Exception as exc:

            logger.exception(exc)

            context["supervisor"]["status"] = (
                "failed"
            )

            context["supervisor"]["error"] = (
                str(exc)
            )

            context["status"] = "failed"

        context["supervisor"]["finished_at"] = (
            datetime.utcnow().isoformat()
        )

        context["current_agent"] = self.name

        return context

    @staticmethod
    def validate_context(
            context: Dict[str, Any],
    ) -> bool:
        """
        Validate the workflow context.
        """

        required = [
            "uploaded_file",
        ]

        return all(
            key in context
            for key in required
        )

    @staticmethod
    def workflow_status(
            context: Dict[str, Any],
    ) -> str:
        """
        Return workflow status.
        """

        return context.get(
            "status",
            "unknown",
        )

    @staticmethod
    def workflow_completed(
            context: Dict[str, Any],
    ) -> bool:
        """
        Check if workflow completed.
        """

        return (
            context.get("status")
            == "completed"
        )

