"""
notification_agent.py

Notification Agent

Responsibilities
----------------
- Create workflow notifications
- Record informational messages
- Record warnings
- Record errors
- Record success events
- Manage notification history

Business logic belongs to processing agents.
This agent only manages notifications.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class NotificationAgent(BaseAgent):
    """
    Creates and manages workflow notifications.
    """

    def __init__(self):

        super().__init__(
            name="NotificationAgent",
            description="Manages workflow notifications.",
        )

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        logger.info(
            "[NotificationAgent] Processing notifications."
        )

        context.setdefault(
            "notifications",
            []
        )

        status = context.get(
            "status",
            "unknown",
        )

        if status == "completed":

            self.success(
                context,
                "Workflow completed successfully.",
            )

        elif status == "failed":

            self.error(
                context,
                context.get(
                    "error",
                    "Workflow execution failed.",
                ),
            )

        elif status == "running":

            self.info(
                context,
                "Workflow is running.",
            )

        context["current_agent"] = self.name

        return context

    def create(
        self,
        context: Dict[str, Any],
        *,
        level: str,
        title: str,
        message: str,
        source: Optional[str] = None,
    ) -> Dict[str, Any]:

        notification = {
            "id": len(
                context.setdefault(
                    "notifications",
                    []
                )
            )
            + 1,
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.lower(),
            "title": title,
            "message": message,
            "source": source,
            "read": False,
        }

        context["notifications"].append(
            notification
        )

        logger.info(
            "[Notification] %s - %s",
            title,
            message,
        )

        return notification

    def success(
        self,
        context: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self.create(
            context,
            level="success",
            title="Success",
            message=message,
            source=context.get(
                "current_agent"
            ),
        )

    def info(
        self,
        context: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self.create(
            context,
            level="info",
            title="Information",
            message=message,
            source=context.get(
                "current_agent"
            ),
        )

    def warning(
        self,
        context: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self.create(
            context,
            level="warning",
            title="Warning",
            message=message,
            source=context.get(
                "current_agent"
            ),
        )

    def error(
        self,
        context: Dict[str, Any],
        message: str,
    ) -> Dict[str, Any]:

        return self.create(
            context,
            level="error",
            title="Error",
            message=message,
            source=context.get(
                "current_agent"
            ),
        )

    def unread(
        self,
        context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        return [
            notification
            for notification in context.get(
                "notifications",
                []
            )
            if not notification.get(
                "read",
                False,
            )
        ]

    def mark_read(
        self,
        context: Dict[str, Any],
        notification_id: int,
    ) -> bool:

        for notification in context.get(
            "notifications",
            []
        ):

            if notification["id"] == notification_id:

                notification["read"] = True

                return True

        return False

    def clear(
        self,
        context: Dict[str, Any],
    ) -> None:

        context["notifications"] = []

    def history(
        self,
        context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        return context.get(
            "notifications",
            []
        )

    def count(
        self,
        context: Dict[str, Any],
    ) -> int:

        return len(
            context.get(
                "notifications",
                []
            )
        )

    def unread_count(
        self,
        context: Dict[str, Any],
    ) -> int:

        return len(
            self.unread(
                context
            )
        )