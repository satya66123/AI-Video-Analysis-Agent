"""
workflow_engine.py

Workflow Engine

Responsibilities
----------------
- Execute agent pipelines
- Maintain workflow context
- Track workflow status
- Handle workflow failures

Business logic belongs to individual agents.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from agents.agent_pipeline import AgentPipeline

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """
    Executes registered agent pipelines.
    """

    def __init__(
        self,
        pipeline: AgentPipeline,
    ):

        self.pipeline = pipeline

    def run(
        self,
        pipeline_name: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute a pipeline.
        """

        agents = self.pipeline.get(
            pipeline_name
        )



        context["pipeline"] = pipeline_name
        context["status"] = "running"

        logger.info(
            "[WorkflowEngine] Running pipeline: %s",
            pipeline_name,
        )

        for agent in agents:

            logger.info(
                "[WorkflowEngine] Executing %s",
                agent.name,
            )

            try:

                context = agent.execute(
                    context
                )

                context["workflow_log"].append(
                    {
                        "agent": agent.name,
                        "status": "completed",
                    }
                )

            except Exception as exc:

                logger.exception(exc)

                context["workflow_log"].append(
                    {
                        "agent": agent.name,
                        "status": "failed",
                        "error": str(exc),
                    }
                )

                context["status"] = "failed"
                context["current_agent"] = agent.name
                context["error"] = str(exc)

                return context

        context["status"] = "completed"

        logger.info(
            "[WorkflowEngine] Pipeline completed."
        )

        return context

    def run_agent(
        self,
        agent,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute a single agent.
        """

        logger.info(
            "[WorkflowEngine] Running %s",
            agent.name,
        )

        return agent.execute(
            context
        )

    def available_pipelines(
        self,
    ):
        """
        Return available pipelines.
        """

        return self.pipeline.list_pipelines()

    def exists(
        self,
        pipeline_name: str,
    ) -> bool:
        """
        Check whether a pipeline exists.
        """

        return self.pipeline.exists(
            pipeline_name
        )