from __future__ import annotations

import logging
from collections import OrderedDict
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent, AgentStatus

logger = logging.getLogger(__name__)


class AgentManager:
    """
    Manages all registered agents.

    Responsibilities
    ----------------
    - Register agents
    - Remove agents
    - Execute agents
    - Initialize agents
    - Shutdown agents
    - Monitor status
    - Return statistics
    """

    def __init__(self) -> None:

        self._agents: OrderedDict[str, BaseAgent] = OrderedDict()

        logger.info("AgentManager initialized")

    # ----------------------------------------------------------
    # Registration
    # ----------------------------------------------------------

    def register_agent(
        self,
        agent: BaseAgent,
        overwrite: bool = False,
    ) -> None:
        """
        Register an agent.
        """

        if agent.name in self._agents and not overwrite:
            raise ValueError(
                f"Agent '{agent.name}' already registered."
            )

        self._agents[agent.name] = agent

        logger.info(
            "Registered agent: %s",
            agent.name,
        )

    def unregister_agent(
        self,
        name: str,
    ) -> bool:
        """
        Remove an agent.
        """

        if name not in self._agents:
            return False

        del self._agents[name]

        logger.info(
            "Removed agent: %s",
            name,
        )

        return True

    def clear(self) -> None:
        """
        Remove every registered agent.
        """

        self._agents.clear()

        logger.info("All agents removed")

    # ----------------------------------------------------------
    # Lookup
    # ----------------------------------------------------------

    def get_agent(
        self,
        name: str,
    ) -> Optional[BaseAgent]:

        return self._agents.get(name)

    def has_agent(
        self,
        name: str,
    ) -> bool:

        return name in self._agents

    def list_agents(self) -> List[str]:

        return list(self._agents.keys())

    def list_enabled_agents(self) -> List[str]:

        return [
            agent.name
            for agent in self._agents.values()
            if agent.enabled
        ]

    # ----------------------------------------------------------
    # Lifecycle
    # ----------------------------------------------------------

    def initialize_all(self) -> None:
        """
        Initialize every registered agent.
        """

        logger.info(
            "Initializing %d agents...",
            len(self._agents),
        )

        for agent in self._agents.values():

            try:
                agent.initialize()

            except Exception:
                logger.exception(
                    "Failed to initialize %s",
                    agent.name,
                )

    def shutdown_all(self) -> None:
        """
        Shutdown every registered agent.
        """

        logger.info(
            "Shutting down all agents..."
        )

        for agent in reversed(
            list(self._agents.values())
        ):

            try:
                agent.shutdown()

            except Exception:
                logger.exception(
                    "Failed to shutdown %s",
                    agent.name,
                )

    # ----------------------------------------------------------
    # Execution
    # ----------------------------------------------------------

    def execute_agent(
        self,
        name: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute a single agent.
        """

        agent = self.get_agent(name)

        if agent is None:
            raise ValueError(
                f"Agent '{name}' not found."
            )

        logger.info(
            "Executing %s",
            name,
        )

        return agent.run(context)

    def execute_pipeline(
        self,
        agent_names: List[str],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute multiple agents sequentially.
        """

        logger.info(
            "Executing pipeline with %d agents",
            len(agent_names),
        )

        for name in agent_names:

            agent = self.get_agent(name)

            if agent is None:

                logger.warning(
                    "Skipping unknown agent %s",
                    name,
                )

                continue

            if not agent.enabled:

                logger.info(
                    "Skipping disabled agent %s",
                    name,
                )

                continue

            context = agent.run(context)

            if context.get("errors"):

                logger.warning(
                    "%s reported errors",
                    name,
                )

        return context

    # ----------------------------------------------------------
    # Status
    # ----------------------------------------------------------

    def get_status(self) -> Dict[str, str]:
        """
        Return status of all agents.
        """

        return {
            name: agent.status.value
            for name, agent in self._agents.items()
        }

    def get_statistics(self) -> Dict[str, Dict]:
        """
        Return statistics for every agent.
        """

        return {
            name: agent.to_dict()
            for name, agent in self._agents.items()
        }

    def healthy(self) -> bool:
        """
        Check whether every enabled agent is healthy.
        """

        for agent in self._agents.values():

            if not agent.enabled:
                continue

            if agent.status == AgentStatus.FAILED:
                return False

        return True

    # ----------------------------------------------------------
    # Utilities
    # ----------------------------------------------------------

    def enable_agent(
        self,
        name: str,
    ) -> None:

        agent = self.get_agent(name)

        if agent:
            agent.enable()

    def disable_agent(
        self,
        name: str,
    ) -> None:

        agent = self.get_agent(name)

        if agent:
            agent.disable()

    def reset_statistics(self) -> None:

        for agent in self._agents.values():
            agent.reset_statistics()

    def count(self) -> int:

        return len(self._agents)

    def enabled_count(self) -> int:

        return sum(
            1
            for agent in self._agents.values()
            if agent.enabled
        )

    def failed_agents(self) -> List[str]:

        return [
            agent.name
            for agent in self._agents.values()
            if agent.status == AgentStatus.FAILED
        ]

    def running_agents(self) -> List[str]:

        return [
            agent.name
            for agent in self._agents.values()
            if agent.status == AgentStatus.RUNNING
        ]

    def completed_agents(self) -> List[str]:

        return [
            agent.name
            for agent in self._agents.values()
            if agent.status == AgentStatus.COMPLETED
        ]

    # ----------------------------------------------------------
    # Magic Methods
    # ----------------------------------------------------------

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return name in self._agents

    def __len__(self) -> int:

        return len(self._agents)

    def __iter__(self):

        return iter(self._agents.values())

    def __repr__(self) -> str:

        return (
            f"<AgentManager "
            f"agents={len(self._agents)}>"
        )