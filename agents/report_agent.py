"""
report_agent.py

Report Agent

Responsibilities
----------------
- Build a complete report from workflow context
- Generate report content using ReportService
- Store report in workflow context

Business logic remains inside ReportService.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ReportAgent(BaseAgent):
    """
    Generates the complete AI Video Analysis report.

    This agent DOES NOT export files.
    Exporting is handled by ExportAgent.
    """

    def __init__(self, report_service):

        super().__init__(
            name="ReportAgent",
            description="Builds the final AI report."
        )

        self.report_service = report_service

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        logger.info(
            "[ReportAgent] Building report..."
        )

        report_data = {
            "video_name": context.get(
                "video_metadata",
                {}
            ).get(
                "filename",
                "N/A",
            ),

            "video_duration": context.get(
                "video_metadata",
                {}
            ).get(
                "duration",
                "N/A",
            ),

            "video_resolution": context.get(
                "video_metadata",
                {}
            ).get(
                "resolution",
                "N/A",
            ),

            "video_fps": context.get(
                "video_metadata",
                {}
            ).get(
                "fps",
                "N/A",
            ),

            "video_format": context.get(
                "video_metadata",
                {}
            ).get(
                "extension",
                "N/A",
            ),

            "video_size": context.get(
                "video_metadata",
                {}
            ).get(
                "size",
                "N/A",
            ),

            "audio_name": context.get(
                "audio_metadata",
                {}
            ).get(
                "filename",
                "N/A",
            ),

            "audio_duration": context.get(
                "audio_metadata",
                {}
            ).get(
                "duration",
                "N/A",
            ),

            "channels": context.get(
                "audio_metadata",
                {}
            ).get(
                "channels",
                "N/A",
            ),

            "sample_rate": context.get(
                "audio_metadata",
                {}
            ).get(
                "sample_rate",
                "N/A",
            ),

            "audio_format": context.get(
                "audio_metadata",
                {}
            ).get(
                "extension",
                "N/A",
            ),

            "audio_size": context.get(
                "audio_metadata",
                {}
            ).get(
                "size",
                "N/A",
            ),

            "provider": context.get(
                "provider_name",
                "N/A",
            ),

            "model": context.get(
                "model_name",
                "N/A",
            ),

            "transcript": context.get(
                "transcript",
                "",
            ),

            "analysis": context.get(
                "analysis",
                "",
            ),

            "chat": context.get(
                "chat_history",
                "",
            ),
        }

        report = self.report_service.generate_complete_report(
            include_video=True,
            include_audio=True,
            include_transcript=True,
            include_analysis=True,
            include_chat=True,
            include_metadata=True,
            data=report_data,
        )

        metadata = {
            "generated_at": datetime.utcnow().isoformat(),
            "length": len(report),
            "words": len(report.split()),
        }

        context["report"] = report
        context["report_metadata"] = metadata
        context["current_agent"] = self.name
        context["status"] = "report_generated"

        logger.info(
            "[ReportAgent] Report generated successfully."
        )

        return context