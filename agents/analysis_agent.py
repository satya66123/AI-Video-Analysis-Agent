"""
analysis_agent.py

Analysis Agent

Responsibilities
----------------
- Perform AI analysis using AIAnalysisService
- Save analysis to disk
- Update workflow context
- Record analysis metadata

Business logic remains inside AIAnalysisService.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class AnalysisAgent(BaseAgent):
    """
    Agent responsible for AI-powered transcript analysis.
    """

    def __init__(self, analysis_service):

        super().__init__(
            name="AnalysisAgent",
            description="Analyzes transcript using configured AI provider.",
        )

        self.analysis_service = analysis_service

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        transcript = context.get("transcript")

        if not transcript:
            raise ValueError(
                "Workflow context does not contain a transcript."
            )

        provider_name = context.get("provider_name")
        model_name = context.get("model_name")



        if not provider_name:
            raise ValueError("provider_name not found in workflow context.")

        if not model_name:
            raise ValueError("model_name not found in workflow context.")

        prompt = context.get(
            "analysis_prompt",
            "Generate a comprehensive analysis of this transcript.",
        )

        analysis_type = context.get(
            "analysis_type",
            "general",
        )

        logger.info(
            "[AnalysisAgent] Starting %s analysis using %s (%s)",
            analysis_type,
            provider_name,
            model_name,
        )

        analysis_result = self.analysis_service.analyze(
            provider_name=provider_name,
            model_name=model_name,
            transcript=transcript,
            prompt=prompt,
        )

        if not analysis_result:
            raise RuntimeError(
                "AI analysis returned no content."
            )

        analysis = analysis_result["content"]

        video_path = context.get("video")

        if video_path:
            filename = os.path.splitext(
                os.path.basename(video_path)
            )[0]
        else:
            filename = "analysis"

        output_path = self.analysis_service.save_analysis(
            filename=filename,
            analysis_type=analysis_type,
            content=analysis,
        )

        metadata = {
            "provider": analysis_result["provider"],
            "model": analysis_result["model"],
            "analysis_type": analysis_type,
            "output_file": output_path,
            "characters": len(analysis),
            "words": len(analysis.split()),
            "generated_at": analysis_result["generated_at"],
        }

        context["analysis"] = analysis
        context["analysis_file"] = output_path
        context["analysis_metadata"] = metadata
        context["current_agent"] = self.name
        context["status"] = "analysis_completed"

        logger.info(
            "[AnalysisAgent] Analysis completed successfully."
        )

        return context