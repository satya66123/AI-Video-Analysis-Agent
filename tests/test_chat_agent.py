from unittest.mock import MagicMock

import pytest

from agents.chat_agent import ChatAgent


def make_service():
    service = MagicMock()
    service.ask.return_value = "This is the AI response."
    service.save_chat.return_value = "chat/video_chat.json"
    return service


def make_context():
    return {
        "transcript": "This is a transcript.",
        "question": "What is this video about?",
        "provider_name": "ollama",
        "model_name": "llama3.1",
        "video": "uploads/video.mp4",
    }


def test_chat_agent_creation():
    service = make_service()

    agent = ChatAgent(service)

    assert agent.name == "ChatAgent"
    assert agent.chat_service is service


def test_execute_success():
    service = make_service()

    agent = ChatAgent(service)

    context = make_context()

    result = agent.execute(context)

    assert result["chat_answer"] == "This is the AI response."
    assert result["chat_file"] == "chat/video_chat.json"
    assert result["status"] == "chat_completed"
    assert result["current_agent"] == "ChatAgent"

    history = result["chat_history"]

    assert len(history) == 1
    assert history[0]["user"] == "What is this video about?"
    assert history[0]["assistant"] == "This is the AI response."
    assert "timestamp" in history[0]

    service.ask.assert_called_once()

    _, kwargs = service.ask.call_args

    assert kwargs["transcript"] == "This is a transcript."
    assert kwargs["question"] == "What is this video about?"
    assert kwargs["provider_name"] == "ollama"
    assert kwargs["model_name"] == "llama3.1"

    # It is the same list object used by the agent.
    assert kwargs["history"] is history

    service.save_chat.assert_called_once_with(
        "video_chat.json",
        history,
    )


def test_execute_existing_history():
    service = make_service()

    agent = ChatAgent(service)

    history = [
        {
            "user": "Hi",
            "assistant": "Hello",
            "timestamp": "2025-01-01T00:00:00",
        }
    ]

    context = make_context()
    context["chat_history"] = history

    result = agent.execute(context)

    assert len(result["chat_history"]) == 2

    service.ask.assert_called_once_with(
        transcript="This is a transcript.",
        history=history,
        question="What is this video about?",
        provider_name="ollama",
        model_name="llama3.1",
    )


def test_execute_without_transcript():
    service = make_service()

    agent = ChatAgent(service)

    context = make_context()
    context.pop("transcript")

    with pytest.raises(
        ValueError,
        match="Workflow context does not contain a transcript.",
    ):
        agent.execute(context)


def test_execute_without_question():
    service = make_service()

    agent = ChatAgent(service)

    context = make_context()
    context.pop("question")

    with pytest.raises(
        ValueError,
        match="No question supplied.",
    ):
        agent.execute(context)


def test_execute_without_video():
    service = make_service()

    agent = ChatAgent(service)

    context = make_context()
    context.pop("video")

    result = agent.execute(context)

    assert result["chat_file"] == "chat/video_chat.json"

    service.save_chat.assert_called_once_with(
        "video_chat.json",
        result["chat_history"],
    )