"""
export_agent.py

Export Agent

Responsibilities
----------------
- Export reports into multiple formats
- Use ExportService only
- Update workflow context
- Store export metadata
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ExportAgent(BaseAgent):
    """
    Agent responsible for exporting reports.
    """

    def __init__(self, export_service):

        super().__init__(
            name="ExportAgent",
            description="Exports reports into multiple formats."
        )

        self.export_service = export_service

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        report = context.get("report")

        if not report:
            raise ValueError(
                "Workflow context does not contain a report."
            )

        video_metadata = context.get(
            "video_metadata",
            {}
        )

        video_name = video_metadata.get(
            "filename",
            "video"
        )

        report_type = context.get(
            "report_type",
            "analysis"
        )

        filename = self.export_service.generate_filename(
            video_name=video_name,
            report_type=report_type,
        )

        # Default: export ALL supported formats
        export_formats: List[str] = context.get(
            "export_formats",
            [
                "pdf",
                "html",
                "md",
                "txt",
                "json",
            ],
        )

        exported_files: Dict[str, Dict[str, Any]] = {}

        for export_format in export_formats:

            logger.info(
                "[ExportAgent] Exporting %s...",
                export_format,
            )

            result = self.export_service.export(
                filename=filename,
                content=report,
                export_format=export_format,
                data={
                    "video": video_metadata,
                    "audio": context.get(
                        "audio_metadata",
                        {}
                    ),
                    "transcript": context.get(
                        "transcript",
                        ""
                    ),
                    "analysis": context.get(
                        "analysis",
                        ""
                    ),
                    "provider": context.get(
                        "provider_name",
                        ""
                    ),
                    "model": context.get(
                        "model_name",
                        ""
                    ),
                },
            )

            exported_files[export_format] = result

        context["exports"] = exported_files
        context["current_agent"] = self.name
        context["status"] = "export_completed"

        logger.info(
            "[ExportAgent] Successfully exported %d formats.",
            len(exported_files),
        )

        return context