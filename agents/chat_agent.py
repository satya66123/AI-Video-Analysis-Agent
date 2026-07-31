"""
chat_agent.py

Chat Agent

Responsibilities
----------------
- Chat with video transcripts
- Manage conversation history
- Save chat history
- Update workflow context

Business logic remains inside AIChatService.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ChatAgent(BaseAgent):
    """
    AI Chat Agent.
    """

    def __init__(self, chat_service):

        super().__init__(
            name="ChatAgent",
            description="Chat with video transcripts."
        )

        self.chat_service = chat_service

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        transcript = context.get("transcript")

        if not transcript:
            raise ValueError(
                "Workflow context does not contain a transcript."
            )

        question = context.get("question")

        if not question:
            logger.info(
                "[ChatAgent] No question supplied. Skipping chat."
            )

            context.setdefault("chat_history", [])
            context["chat_answer"] = None
            context["current_agent"] = self.name
            context["status"] = "chat_skipped"

            return context

        provider_name = context.get("provider_name")

        model_name = context.get("model_name")

        history: List[Dict[str, str]] = context.get(
            "chat_history",
            [],
        )

        logger.info(
            "[ChatAgent] Asking question..."
        )

        answer = self.chat_service.ask(
            transcript=transcript,
            history=history,
            question=question,
            provider_name=provider_name,
            model_name=model_name,
        )

        history.append(
            {
                "user": question,
                "assistant": answer,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        video_name = Path(
            context.get(
                "video",
                "video",
            )
        ).stem

        chat_filename = (
            f"{video_name}_chat.json"
        )

        chat_path = self.chat_service.save_chat(
            chat_filename,
            history,
        )

        context["chat_answer"] = answer
        context["chat_history"] = history
        context["chat_file"] = chat_path
        context["current_agent"] = self.name
        context["status"] = "chat_completed"

        logger.info(
            "[ChatAgent] Chat completed."
        )

        return context