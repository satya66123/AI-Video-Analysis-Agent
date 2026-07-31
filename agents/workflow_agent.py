"""
workflow_agent.py

Workflow Agent

Responsibilities
----------------
- Execute the complete AI Video Analysis workflow
- Coordinate all agents
- Maintain workflow context
- Stop execution on failures

Business logic remains inside the individual agents.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class WorkflowAgent(BaseAgent):
    """
    Executes the complete AI Video Analysis workflow.
    """

    def __init__(
        self,
        upload_agent,
        audio_agent,
        transcript_agent,
        analysis_agent,
        report_agent,
        export_agent,
    ):

        super().__init__(
            name="WorkflowAgent",
            description="Coordinates the complete AI Video Analysis workflow.",
        )

        self.pipeline = [
            upload_agent,
            audio_agent,
            transcript_agent,
            analysis_agent,
            report_agent,
            export_agent,
        ]

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        logger.info(
            "[WorkflowAgent] Workflow started."
        )

        workflow_log: List[Dict[str, str]] = []

        context["status"] = "running"

        for agent in self.pipeline:

            logger.info(
                "[WorkflowAgent] Running %s",
                agent.name,
            )

            workflow_log.append(
                {
                    "agent": agent.name,
                    "status": "started",
                }
            )

            try:

                context = agent.execute(context)

                workflow_log[-1]["status"] = "completed"

            except Exception as exc:

                logger.exception(exc)

                workflow_log[-1]["status"] = "failed"

                workflow_log[-1]["error"] = str(exc)

                context["status"] = "failed"
                context["error"] = str(exc)
                context["workflow_log"] = workflow_log
                context["current_agent"] = agent.name

                return context

        context["status"] = "completed"
        context["workflow_log"] = workflow_log
        context["current_agent"] = self.name

        logger.info(
            "[WorkflowAgent] Workflow completed."
        )

        return context