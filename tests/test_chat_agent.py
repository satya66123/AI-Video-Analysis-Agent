"""
tests/test_chat_agent.py
"""

from unittest.mock import MagicMock

import pytest

from agents.chat_agent import ChatAgent


def make_service():

    service = MagicMock()

    service.ask.return_value = (
        "This is the AI answer."
    )

    service.save_chat.return_value = (
        "chat_history/video_chat.json"
    )

    return service


def make_context():

    return {

        "transcript": "This is a transcript.",

        "question": "What is discussed?",

        "provider_name": "ollama",

        "model_name": "llama3.1",

        "video": "uploads/video.mp4",

        "chat_history": [],

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

    assert result["status"] == "chat_completed"

    assert result["current_agent"] == "ChatAgent"

    assert (
        result["chat_answer"]
        == "This is the AI answer."
    )

    assert (
        result["chat_file"]
        == "chat_history/video_chat.json"
    )

    assert len(
        result["chat_history"]
    ) == 1

    chat = result["chat_history"][0]

    assert chat["user"] == "What is discussed?"

    assert (
        chat["assistant"]
        == "This is the AI answer."
    )

    assert "timestamp" in chat



    service.ask.assert_called_once()

    _, kwargs = service.ask.call_args

    assert kwargs["transcript"] == "This is a transcript."
    assert kwargs["question"] == "What is discussed?"
    assert kwargs["provider_name"] == "ollama"
    assert kwargs["model_name"] == "llama3.1"

    service.ask.assert_called_once()

    _, kwargs = service.ask.call_args

    assert kwargs["transcript"] == "This is a transcript."
    assert kwargs["question"] == "What is discussed?"
    assert kwargs["provider_name"] == "ollama"
    assert kwargs["model_name"] == "llama3.1"


def test_execute_without_question():

    service = make_service()

    agent = ChatAgent(service)

    context = {

        "transcript": "Transcript",

    }

    result = agent.execute(context)

    assert result["status"] == "chat_skipped"

    assert result["current_agent"] == "ChatAgent"

    assert result["chat_answer"] is None

    assert result["chat_history"] == []

    service.ask.assert_not_called()

    service.save_chat.assert_not_called()


def test_execute_without_transcript():

    service = make_service()

    agent = ChatAgent(service)

    with pytest.raises(

        ValueError,

        match="Workflow context does not contain a transcript.",

    ):

        agent.execute({})


def test_execute_existing_chat_history():

    service = make_service()

    agent = ChatAgent(service)

    context = make_context()

    context["chat_history"] = [

        {

            "user": "Hello",

            "assistant": "Hi",

            "timestamp": "old",

        }

    ]

    result = agent.execute(context)

    assert len(
        result["chat_history"]
    ) == 2

    assert (
        result["chat_history"][0]["user"]
        == "Hello"
    )

    assert (
        result["chat_history"][1]["user"]
        == "What is discussed?"
    )


def test_execute_default_video_name():

    service = make_service()

    agent = ChatAgent(service)

    context = make_context()

    context.pop("video")

    agent.execute(context)

    service.save_chat.assert_called_once_with(

        "video_chat.json",

        context["chat_history"],

    )


def test_execute_calls_service_correctly():

    service = make_service()

    agent = ChatAgent(service)

    context = make_context()

    agent.execute(context)

    _, kwargs = service.ask.call_args

    assert kwargs["provider_name"] == "ollama"

    assert kwargs["model_name"] == "llama3.1"

    assert kwargs["question"] == "What is discussed?"

    assert kwargs["transcript"] == "This is a transcript."