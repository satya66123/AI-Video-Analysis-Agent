"""
recovery_agent.py

Recovery Agent

Responsibilities
----------------
- Recover failed workflows
- Retry failed agents
- Resume interrupted workflows
- Store recovery history
- Restore workflow state

Business logic belongs to processing agents.
"""

from __future__ import annotations

import copy
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent
from .agent_registry import AgentRegistry

logger = logging.getLogger(__name__)


class RecoveryAgent(BaseAgent):
    """
    Handles workflow recovery and retry operations.
    """

    def __init__(
        self,
        registry: AgentRegistry,
        max_retries: int = 3,
    ):

        super().__init__(
            name="RecoveryAgent",
            description="Handles workflow recovery."
        )

        self.registry = registry
        self.max_retries = max_retries

    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        logger.info(
            "[RecoveryAgent] Checking workflow."
        )

        recovery = context.setdefault(
            "recovery",
            {}
        )

        recovery.setdefault(
            "history",
            []
        )

        recovery["checked_at"] = (
            datetime.utcnow().isoformat()
        )

        if context.get("status") != "failed":
            recovery["action"] = "none"
            context["current_agent"] = self.name
            return context

        recovered = self.recover(context)

        recovery["action"] = (
            "recovered"
            if recovered
            else "failed"
        )

        context["current_agent"] = self.name

        return context

    def recover(
        self,
        context: Dict[str, Any],
    ) -> bool:

        failed_agent = context.get(
            "current_agent"
        )

        if not failed_agent:
            return False

        retry_count = context.setdefault(
            "retry_count",
            {}
        )

        current = retry_count.get(
            failed_agent,
            0,
        )

        if current >= self.max_retries:

            logger.warning(
                "Maximum retries exceeded for %s",
                failed_agent,
            )

            return False

        retry_count[failed_agent] = current + 1

        snapshot = copy.deepcopy(context)

        context["recovery"]["history"].append(
            {
                "agent": failed_agent,
                "attempt": current + 1,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        try:

            agent = self.registry.get(
                failed_agent
            )

            logger.info(
                "Retrying %s",
                failed_agent,
            )

            result = agent.execute(
                snapshot
            )

            result["status"] = "completed"
            result["error"] = None

            return self._merge_context(
                context,
                result,
            )

        except Exception as exc:

            logger.exception(exc)

            context["error"] = str(exc)

            return False

    def resume(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Resume workflow after recovery.
        """

        context["status"] = "running"

        context.setdefault(
            "recovery",
            {}
        )

        context["recovery"][
            "resumed_at"
        ] = datetime.utcnow().isoformat()

        return context

    def rollback(
        self,
        context: Dict[str, Any],
        snapshot: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Restore previous snapshot.
        """

        snapshot["status"] = "rolled_back"

        snapshot.setdefault(
            "recovery",
            {}
        )

        snapshot["recovery"][
            "rollback_at"
        ] = datetime.utcnow().isoformat()

        return snapshot

    def failed_agent(
        self,
        context: Dict[str, Any],
    ) -> Optional[str]:

        return context.get(
            "current_agent"
        )

    def retry_attempts(
        self,
        context: Dict[str, Any],
        agent_name: str,
    ) -> int:

        return context.get(
            "retry_count",
            {}
        ).get(
            agent_name,
            0,
        )

    def can_retry(
        self,
        context: Dict[str, Any],
        agent_name: str,
    ) -> bool:

        return (
            self.retry_attempts(
                context,
                agent_name,
            )
            < self.max_retries
        )

    def recovery_history(
        self,
        context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        return context.get(
            "recovery",
            {}
        ).get(
            "history",
            []
        )

    def clear_history(
        self,
        context: Dict[str, Any],
    ) -> None:

        context.setdefault(
            "recovery",
            {}
        )["history"] = []

    def _merge_context(
        self,
        original: Dict[str, Any],
        recovered: Dict[str, Any],
    ) -> bool:

        original.clear()
        original.update(recovered)

        original["status"] = "completed"

        original.setdefault(
            "recovery",
            {}
        )

        original["recovery"][
            "recovered_at"
        ] = datetime.utcnow().isoformat()

        return True