"""
tests/test_analysis_agent.py
"""

from unittest.mock import MagicMock

import pytest

from agents.analysis_agent import AnalysisAgent


def make_service():

    service = MagicMock()

    service.analyze.return_value = {
        "content": "This is the AI analysis.",
        "provider": "ollama",
        "model": "llama3.1",
        "generated_at": "2026-08-01T10:00:00",
    }

    service.save_analysis.return_value = (
        "analysis/video_general.md"
    )

    return service


def make_context():

    return {
        "transcript": "This is a transcript.",
        "provider_name": "ollama",
        "model_name": "llama3.1",
        "video": "uploads/video.mp4",
    }


def test_analysis_agent_creation():

    service = make_service()

    agent = AnalysisAgent(service)

    assert agent.name == "AnalysisAgent"

    assert agent.analysis_service is service


def test_execute_success():

    service = make_service()

    agent = AnalysisAgent(service)

    context = make_context()

    result = agent.execute(context)

    assert (
        result["analysis"]
        == "This is the AI analysis."
    )

    assert (
        result["analysis_file"]
        == "analysis/video_general.md"
    )

    assert (
        result["status"]
        == "analysis_completed"
    )

    assert (
        result["current_agent"]
        == "AnalysisAgent"
    )

    metadata = result["analysis_metadata"]

    assert metadata["provider"] == "ollama"

    assert metadata["model"] == "llama3.1"

    assert metadata["analysis_type"] == "general"

    assert (
        metadata["output_file"]
        == "analysis/video_general.md"
    )

    assert metadata["characters"] == len(
        "This is the AI analysis."
    )

    assert metadata["words"] == len(
        "This is the AI analysis.".split()
    )

    assert (
        metadata["generated_at"]
        == "2026-08-01T10:00:00"
    )

    service.analyze.assert_called_once_with(
        provider_name="ollama",
        model_name="llama3.1",
        transcript="This is a transcript.",
        prompt="Generate a comprehensive analysis of this transcript.",
    )

    service.save_analysis.assert_called_once_with(
        filename="video",
        analysis_type="general",
        content="This is the AI analysis.",
    )


def test_execute_custom_prompt_and_analysis_type():

    service = make_service()

    agent = AnalysisAgent(service)

    context = make_context()

    context["analysis_prompt"] = (
        "Summarize the meeting."
    )

    context["analysis_type"] = (
        "summary"
    )

    result = agent.execute(context)

    assert (
        result["analysis_metadata"]["analysis_type"]
        == "summary"
    )

    service.analyze.assert_called_once_with(
        provider_name="ollama",
        model_name="llama3.1",
        transcript="This is a transcript.",
        prompt="Summarize the meeting.",
    )

    service.save_analysis.assert_called_once_with(
        filename="video",
        analysis_type="summary",
        content="This is the AI analysis.",
    )


def test_execute_without_transcript():

    service = make_service()

    agent = AnalysisAgent(service)

    context = make_context()

    context.pop("transcript")

    with pytest.raises(
        ValueError,
        match="Workflow context does not contain a transcript.",
    ):

        agent.execute(context)


def test_execute_without_provider():

    service = make_service()

    agent = AnalysisAgent(service)

    context = make_context()

    context.pop("provider_name")

    with pytest.raises(
        ValueError,
        match="provider_name not found in workflow context.",
    ):

        agent.execute(context)


def test_execute_without_model():

    service = make_service()

    agent = AnalysisAgent(service)

    context = make_context()

    context.pop("model_name")

    with pytest.raises(
        ValueError,
        match="model_name not found in workflow context.",
    ):

        agent.execute(context)


def test_execute_analysis_returns_none():

    service = make_service()

    service.analyze.return_value = None

    agent = AnalysisAgent(service)

    with pytest.raises(
        RuntimeError,
        match="AI analysis returned no content.",
    ):

        agent.execute(
            make_context()
        )


def test_execute_without_video():

    service = make_service()

    agent = AnalysisAgent(service)

    context = make_context()

    context.pop("video")

    result = agent.execute(context)

    assert (
        result["analysis_file"]
        == "analysis/video_general.md"
    )

    service.save_analysis.assert_called_once_with(
        filename="analysis",
        analysis_type="general",
        content="This is the AI analysis.",
    )


def test_execute_custom_video_name():

    service = make_service()

    agent = AnalysisAgent(service)

    context = make_context()

    context["video"] = (
        "uploads/my_meeting.mp4"
    )

    result = agent.execute(context)

    assert (
        result["analysis_file"]
        == "analysis/video_general.md"
    )

    service.save_analysis.assert_called_once_with(
        filename="my_meeting",
        analysis_type="general",
        content="This is the AI analysis.",
    )