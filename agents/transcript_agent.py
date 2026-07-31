"""
transcript_agent.py

Transcript Agent

Responsibilities
----------------
- Generate transcript using SpeechService
- Update workflow context
- Store transcript metadata
- Handle transcription failures

Business logic remains inside SpeechService.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class TranscriptAgent(BaseAgent):
    """
    Agent responsible for generating
    transcripts from extracted audio.
    """

    def __init__(self, speech_service):

        super().__init__(
            name="TranscriptAgent",
            description="Generates transcript using Whisper."
        )

        self.speech_service = speech_service

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        audio_path = context.get("audio")

        if not audio_path:
            raise ValueError(
                "Workflow context does not contain an audio file."
            )

        logger.info(
            "[TranscriptAgent] Transcribing %s",
            audio_path,
        )

        progress_bar = context.get("progress_bar")
        status_text = context.get("status_text")

        model_name = context.get(
            "whisper_model",
            "base"
        )

        chunk_minutes = context.get(
            "chunk_minutes",
            5
        )

        result = self.speech_service.transcribe(
            audio_path=audio_path,
            progress_bar=progress_bar,
            status_text=status_text,
            model_name=model_name,
            chunk_minutes=chunk_minutes,
        )

        if result is None:
            raise RuntimeError(
                "Transcript generation failed."
            )

        metadata = {
            "filename": os.path.basename(result["path"]),
            "filepath": result["path"],
            "model": result["model"],
            "chunk_minutes": chunk_minutes,
            "characters": result["character_count"],
            "words": result["word_count"],
            "generated_at": datetime.utcnow().isoformat(),
        }

        context["transcript"] = result["text"]
        context["transcript_path"] = result["path"]
        context["transcript_metadata"] = metadata
        context["current_agent"] = self.name
        context["status"] = "transcript_generated"

        logger.info(
            "[TranscriptAgent] Transcript generated successfully."
        )

        return context