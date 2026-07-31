"""
audio_agent.py

Audio Agent

Responsibilities
----------------
- Extract audio from uploaded video
- Prevent duplicate extraction (handled by AudioService)
- Update workflow context
- Record audio metadata

Business logic remains inside AudioService.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class AudioAgent(BaseAgent):
    """
    Agent responsible for extracting audio
    from uploaded videos.
    """

    def __init__(self, audio_service):

        super().__init__(
            name="AudioAgent",
            description="Extracts audio from uploaded videos."
        )

        self.audio_service = audio_service

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        video_path = context.get("video")

        if not video_path:
            raise ValueError(
                "Workflow context does not contain a video path."
            )

        logger.info(
            "[AudioAgent] Extracting audio from %s",
            video_path,
        )

        progress_bar = context.get("progress_bar")
        status_text = context.get("status_text")

        audio_path = self.audio_service.extract_audio(
            video_path=video_path,
            progress_bar=progress_bar,
            status_text=status_text,
        )

        if audio_path is None:
            raise RuntimeError(
                "Audio extraction failed."
            )

        metadata = {
            "filename": os.path.basename(audio_path),
            "filepath": audio_path,
            "extension": os.path.splitext(audio_path)[1],
            "created_at": datetime.utcnow().isoformat(),
        }

        context["audio"] = audio_path
        context["audio_metadata"] = metadata
        context["current_agent"] = self.name
        context["status"] = "audio_extracted"

        logger.info(
            "[AudioAgent] Audio extraction completed."
        )

        return context