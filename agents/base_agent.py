"""
base_agent.py

Base class for all AI Video Analysis Agents.

Every agent in the system inherits from BaseAgent.

Responsibilities
----------------
- Standardized lifecycle
- Logging
- Status management
- Execution timing
- Retry handling
- Context updates
- Event publishing
- Error tracking
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from time import perf_counter
from typing import Any, Dict, Optional


logger = logging.getLogger(__name__)


class AgentStatus(str, Enum):
    """Possible states of an agent."""

    IDLE = "idle"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


class BaseAgent(ABC):
    """
    Base class for every autonomous agent.
    """

    MAX_RETRIES = 3

    def __init__(
        self,
        name: str,
        description: str = "",
    ) -> None:

        self.name = name
        self.description = description

        self.status = AgentStatus.IDLE

        self.created_at = datetime.utcnow()

        self.last_started: Optional[datetime] = None
        self.last_finished: Optional[datetime] = None

        self.execution_count = 0
        self.success_count = 0
        self.failure_count = 0

        self.last_execution_time = 0.0
        self.total_execution_time = 0.0

        self.last_error: Optional[str] = None

        self.enabled = True

        logger.info("[%s] Agent created", self.name)

    # --------------------------------------------------------
    # Lifecycle
    # --------------------------------------------------------

    def initialize(self) -> None:
        """Initialize the agent."""

        self.status = AgentStatus.INITIALIZING

        logger.info("[%s] Initializing...", self.name)

        self.on_initialize()

        self.status = AgentStatus.READY

        logger.info("[%s] Ready", self.name)

    def shutdown(self) -> None:
        """Shutdown the agent."""

        logger.info("[%s] Shutting down...", self.name)

        self.on_shutdown()

        self.status = AgentStatus.STOPPED

    # --------------------------------------------------------
    # Execution
    # --------------------------------------------------------

    def run(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Executes the agent.

        Parameters
        ----------
        context:
            Shared workflow context.

        Returns
        -------
        Updated workflow context.
        """

        if not self.enabled:
            logger.warning("[%s] Agent disabled", self.name)
            return context

        retries = 0

        while retries < self.MAX_RETRIES:

            try:

                self.status = AgentStatus.RUNNING

                self.last_started = datetime.utcnow()

                self.execution_count += 1

                logger.info("[%s] Started", self.name)

                start = perf_counter()

                context = self.execute(context)

                elapsed = perf_counter() - start

                self.last_execution_time = elapsed
                self.total_execution_time += elapsed

                self.last_finished = datetime.utcnow()

                self.success_count += 1

                self.status = AgentStatus.COMPLETED

                logger.info(
                    "[%s] Completed in %.2f seconds",
                    self.name,
                    elapsed,
                )

                return context

            except Exception as exc:

                retries += 1

                self.failure_count += 1

                self.last_error = str(exc)

                logger.exception(
                    "[%s] Attempt %d failed",
                    self.name,
                    retries,
                )

                self.on_error(exc)

                if retries >= self.MAX_RETRIES:

                    self.status = AgentStatus.FAILED



                    return context

        return context

    # --------------------------------------------------------
    # Required Implementation
    # --------------------------------------------------------

    @abstractmethod
    def execute(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute agent logic.
        """
        raise NotImplementedError

    # --------------------------------------------------------
    # Optional Hooks
    # --------------------------------------------------------

    def on_initialize(self) -> None:
        """Called during initialize()."""

    def on_shutdown(self) -> None:
        """Called during shutdown()."""

    def on_error(
        self,
        exception: Exception,
    ) -> None:
        """Called when execution fails."""

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def reset_statistics(self) -> None:
        self.execution_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.total_execution_time = 0.0
        self.last_execution_time = 0.0

    # --------------------------------------------------------
    # Information
    # --------------------------------------------------------

    @property
    def success_rate(self) -> float:

        if self.execution_count == 0:
            return 0.0

        return (
            self.success_count
            / self.execution_count
        ) * 100

    @property
    def average_execution_time(self) -> float:

        if self.success_count == 0:
            return 0.0

        return (
            self.total_execution_time
            / self.success_count
        )

    # --------------------------------------------------------
    # Serialization
    # --------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:

        return {
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
            "last_started": (
                self.last_started.isoformat()
                if self.last_started
                else None
            ),
            "last_finished": (
                self.last_finished.isoformat()
                if self.last_finished
                else None
            ),
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": round(
                self.success_rate,
                2,
            ),
            "last_execution_time": round(
                self.last_execution_time,
                4,
            ),
            "average_execution_time": round(
                self.average_execution_time,
                4,
            ),
            "last_error": self.last_error,
        }

    def __str__(self) -> str:

        return (
            f"{self.name}"
            f"({self.status.value})"
        )

    def __repr__(self) -> str:

        return (
            f"<{self.__class__.__name__}"
            f" name={self.name}"
            f" status={self.status.value}>"
        )