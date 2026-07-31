from unittest.mock import MagicMock

import pytest

from agents.agent_pipeline import AgentPipeline


def test_pipeline_creation():
    pipeline = AgentPipeline()

    assert pipeline.count() == 0
    assert pipeline.list_pipelines() == []


def test_register_pipeline():
    pipeline = AgentPipeline()

    agent = MagicMock()

    pipeline.register(
        "test",
        [agent],
    )

    assert pipeline.exists("test")
    assert pipeline.count() == 1


def test_get_pipeline():
    pipeline = AgentPipeline()

    agent = MagicMock()

    pipeline.register(
        "test",
        [agent],
    )

    assert pipeline.get("test") == [agent]


def test_get_missing_pipeline():
    pipeline = AgentPipeline()

    with pytest.raises(KeyError):
        pipeline.get("missing")


def test_remove_pipeline():
    pipeline = AgentPipeline()

    pipeline.register(
        "test",
        [MagicMock()],
    )

    pipeline.remove("test")

    assert not pipeline.exists("test")


def test_clear_pipeline():
    pipeline = AgentPipeline()

    pipeline.register(
        "one",
        [MagicMock()],
    )

    pipeline.register(
        "two",
        [MagicMock()],
    )

    pipeline.clear()

    assert pipeline.count() == 0


def test_as_dict():
    pipeline = AgentPipeline()

    agent = MagicMock()

    pipeline.register(
        "test",
        [agent],
    )

    data = pipeline.as_dict()

    assert isinstance(data, dict)
    assert "test" in data
    assert data["test"] == [agent]