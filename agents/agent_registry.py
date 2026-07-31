"""
agent_registry.py

Agent Registry

Responsibilities
----------------
- Register agents
- Retrieve agents
- Remove agents
- List registered agents
- Check agent existence

The registry stores only agent instances.
"""

from __future__ import annotations

from typing import Dict, List

from .base_agent import BaseAgent


class AgentRegistry:
    """
    Registry for all available agents.
    """

    def __init__(self):

        self._agents: Dict[str, BaseAgent] = {}

    def register(
        self,
        name: str,
        agent: BaseAgent,
    ) -> None:
        """
        Register an agent.
        """

        self._agents[name] = agent

    def get(
        self,
        name: str,
    ) -> BaseAgent:
        """
        Retrieve an agent.

        Raises
        ------
        KeyError
            If the agent does not exist.
        """

        if name not in self._agents:
            raise KeyError(
                f"Agent '{name}' is not registered."
            )

        return self._agents[name]

    def remove(
        self,
        name: str,
    ) -> None:
        """
        Remove an agent.
        """

        self._agents.pop(name, None)

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether an agent exists.
        """

        return name in self._agents

    def list_agents(
        self,
    ) -> List[str]:
        """
        Return registered agent names.
        """

        return sorted(
            self._agents.keys()
        )

    def clear(self) -> None:
        """
        Remove every registered agent.
        """

        self._agents.clear()

    def count(self) -> int:
        """
        Number of registered agents.
        """

        return len(self._agents)

    def register_many(
        self,
        agents: Dict[str, BaseAgent],
    ) -> None:
        """
        Register multiple agents.
        """

        self._agents.update(
            agents
        )

    def as_dict(
        self,
    ) -> Dict[str, BaseAgent]:
        """
        Return registry dictionary.
        """

        return dict(
            self._agents
        )