"""
agent_factory.py

Agent Factory

Responsibilities
----------------
- Create all agent instances
- Wire dependencies
- Return configured agents

Business logic belongs to services.
"""

from __future__ import annotations

from typing import Dict

from .analysis_agent import AnalysisAgent
from .audio_agent import AudioAgent
from .chat_agent import ChatAgent
from .export_agent import ExportAgent
from .report_agent import ReportAgent
from .transcript_agent import TranscriptAgent
from .upload_agent import UploadAgent
from .workflow_agent import WorkflowAgent


class AgentFactory:
    """
    Factory responsible for creating agent instances.

    Services must already exist and are injected into
    this factory.
    """

    @staticmethod
    def create_agents(
        *,
        video_service,
        audio_service,
        speech_service,
        analysis_service,
        report_service,
        export_service,
        chat_service,
    ) -> Dict[str, object]:

        upload_agent = UploadAgent(video_service)

        audio_agent = AudioAgent(audio_service)

        transcript_agent = TranscriptAgent(
            speech_service
        )

        analysis_agent = AnalysisAgent(
            analysis_service
        )

        report_agent = ReportAgent(
            report_service
        )

        export_agent = ExportAgent(
            export_service
        )

        chat_agent = ChatAgent(
            chat_service
        )

        workflow_agent = WorkflowAgent(
            upload_agent=upload_agent,
            audio_agent=audio_agent,
            transcript_agent=transcript_agent,
            analysis_agent=analysis_agent,
            report_agent=report_agent,
            export_agent=export_agent,
        )

        return {
            "upload": upload_agent,
            "audio": audio_agent,
            "transcript": transcript_agent,
            "analysis": analysis_agent,
            "report": report_agent,
            "export": export_agent,
            "chat": chat_agent,
            "workflow": workflow_agent,
        }