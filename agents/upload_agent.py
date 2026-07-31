"""
upload_agent.py

Upload Agent

Responsible for:
- Validating uploaded video
- Checking duplicate uploads
- Saving the video
- Updating workflow context
- Returning execution results

Business logic remains inside VideoService.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class UploadAgent(BaseAgent):
    """
    Upload Agent

    Wraps VideoService and updates the workflow context.
    """

    def __init__(self, video_service):

        super().__init__(
            name="UploadAgent",
            description="Handles video upload and metadata."
        )

        self.video_service = video_service

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        uploaded_file = context.get("uploaded_file")

        if uploaded_file is None:
            raise ValueError(
                "No uploaded file found in workflow context."
            )

        logger.info(
            "[UploadAgent] Processing %s",
            uploaded_file.name,
        )

        progress_bar = context.get("progress_bar")
        status_text = context.get("status_text")

        duplicate = self.video_service.is_duplicate(
            uploaded_file
        )

        if duplicate:

            logger.warning(
                "Duplicate upload detected."
            )



            context["duplicate"] = True

            return context

        video_info = self.video_service.save_video(
            uploaded_file=uploaded_file,
            progress_bar=progress_bar,
            status_text=status_text,
        )

        metadata = {
            "filename": video_info["filename"],
            "saved_path": video_info["filepath"],
            "original_filename": video_info["original_filename"],
            "size": video_info["size"],
            "extension": uploaded_file.name.split(".")[-1],
            "uploaded_at": datetime.utcnow().isoformat(),
        }

        context["video"] = video_info["filepath"]  # <-- string path
        context["video_metadata"] = metadata
        context["duplicate"] = False
        context["current_agent"] = self.name
        context["status"] = "video_uploaded"

        logger.info(
            "[UploadAgent] Upload completed."
        )

        return context