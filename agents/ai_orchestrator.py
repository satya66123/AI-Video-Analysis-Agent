"""
ai_orchestrator.py

AI Orchestrator

Responsibilities
----------------
- Initialize all agents
- Register agents
- Register pipelines
- Execute workflows
- Execute individual agents
- Backward compatibility for chat
"""

from __future__ import annotations

from typing import Any, Dict, List

from agents.agent_factory import AgentFactory
from agents.agent_pipeline import AgentPipeline
from agents.agent_registry import AgentRegistry
from agents.workflow_engine import WorkflowEngine


class AIOrchestrator:
    """
    Central coordinator for the AI Video Analysis Agent.
    """

    def __init__(
        self,
        *,
        video_service,
        audio_service,
        speech_service,
        analysis_service,
        report_service,
        export_service,
        chat_service,
    ):

        # Services
        self.video_service = video_service
        self.audio_service = audio_service
        self.speech_service = speech_service
        self.analysis_service = analysis_service
        self.report_service = report_service
        self.export_service = export_service
        self.chat_service = chat_service

        # Create agents
        self.agents = AgentFactory.create_agents(
            video_service=video_service,
            audio_service=audio_service,
            speech_service=speech_service,
            analysis_service=analysis_service,
            report_service=report_service,
            export_service=export_service,
            chat_service=chat_service,
        )

        # Registry
        self.registry = AgentRegistry()
        self.registry.register_many(self.agents)

        # Pipelines
        self.pipeline = AgentPipeline()
        self.pipeline.register_default_pipelines(self.registry)

        # Workflow Engine
        self.engine = WorkflowEngine(self.pipeline)

    # ------------------------------------------------------------------
    # Full workflow
    # ------------------------------------------------------------------

    def run(
        self,
        context: Dict[str, Any],
        pipeline: str = "standard",
    ) -> Dict[str, Any]:

        if not isinstance(context, dict):
            raise TypeError(
                f"Expected context to be dict, got {type(context).__name__}"
            )

        context.setdefault("workflow_log", [])

        return self.engine.run(
            pipeline_name=pipeline,
            context=context,
        )

    # ------------------------------------------------------------------
    # Run a single agent
    # ------------------------------------------------------------------

    def run_chat(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.engine.run_agent(
            self.registry.get("chat"),
            context,
        )

    # ------------------------------------------------------------------
    # Backward compatibility
    # ------------------------------------------------------------------

    def chat(
        self,
        transcript: str,
        question: str,
        provider_name: str,
        model_name: str,
        history: List[Dict[str, str]] | None = None,
    ) -> str:
        """
        Compatibility wrapper for older UI code.
        """

        context = {
            "transcript": transcript,
            "question": question,
            "provider_name": provider_name,
            "model_name": model_name,
            "chat_history": history or [],
        }

        result = self.run_chat(context)

        return result.get("chat_answer", "")

    # ------------------------------------------------------------------
    # Registry helpers
    # ------------------------------------------------------------------

    def get_agent(
        self,
        name: str,
    ):
        return self.registry.get(name)

    def list_agents(
        self,
    ):
        return self.registry.list_agents()

    def list_pipelines(
        self,
    ):
        return self.pipeline.list_pipelines()