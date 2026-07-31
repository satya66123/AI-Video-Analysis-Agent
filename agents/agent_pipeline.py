"""
agent_pipeline.py

Agent Pipeline

Responsibilities
----------------
- Define reusable execution pipelines
- Store ordered agent sequences
- Provide pipeline lookup
- Allow custom pipelines

Execution is handled by WorkflowAgent/WorkflowEngine.
"""

from __future__ import annotations

from typing import Dict, List

from .base_agent import BaseAgent
from .agent_registry import AgentRegistry


class AgentPipeline:
    """
    Defines reusable execution pipelines.
    """

    def __init__(self):

        self._pipelines: Dict[str, List[BaseAgent]] = {}

    def register(
        self,
        name: str,
        agents: List[BaseAgent],
    ) -> None:
        """
        Register a pipeline.
        """

        self._pipelines[name] = agents

    def get(
        self,
        name: str,
    ) -> List[BaseAgent]:
        """
        Get a registered pipeline.

        Raises
        ------
        KeyError
            If the pipeline does not exist.
        """

        if name not in self._pipelines:
            raise KeyError(
                f"Pipeline '{name}' is not registered."
            )

        return self._pipelines[name]

    def remove(
        self,
        name: str,
    ) -> None:
        """
        Remove a pipeline.
        """

        self._pipelines.pop(name, None)

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a pipeline exists.
        """

        return name in self._pipelines

    def list_pipelines(
        self,
    ) -> List[str]:
        """
        Return all pipeline names.
        """

        return sorted(
            self._pipelines.keys()
        )

    def clear(self) -> None:
        """
        Remove all pipelines.
        """

        self._pipelines.clear()

    def count(self) -> int:
        """
        Return total number of pipelines.
        """

        return len(self._pipelines)

    def register_default_pipelines(
        self,
        registry: AgentRegistry,
    ) -> None:
        """
        Register built-in pipelines.
        """

        self.register(
            "standard",
            [
                registry.get("upload"),
                registry.get("audio"),
                registry.get("transcript"),
                registry.get("analysis"),
                registry.get("report"),
                registry.get("export"),
            ],
        )

        self.register(
            "analysis",
            [
                registry.get("analysis"),
            ],
        )

        self.register(
            "report",
            [
                registry.get("report"),
                registry.get("export"),
            ],
        )

        self.register(
            "chat",
            [
                registry.get("chat"),
            ],
        )

    def as_dict(
        self,
    ) -> Dict[str, List[BaseAgent]]:
        """
        Return all registered pipelines.
        """

        return dict(self._pipelines)