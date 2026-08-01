"""
tests/test_ai_chat_service.py
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from services.ai_chat_service import AIChatService


@pytest.fixture
def chat_service(tmp_path):

    service = AIChatService()

    service.chat_dir = str(tmp_path)

    return service


def test_build_prompt(chat_service):

    history = [
        {
            "user": "Hello",
            "assistant": "Hi",
        }
    ]

    prompt = chat_service.build_prompt(
        transcript="Video Transcript",
        history=history,
        question="What is AI?",
    )

    assert "Video Transcript" in prompt
    assert "Hello" in prompt
    assert "Hi" in prompt
    assert "What is AI?" in prompt
    assert "CURRENT QUESTION" in prompt


@patch(
    "services.ai_chat_service.ProviderFactory.get_provider"
)
def test_ask_success(
    mock_get_provider,
    chat_service,
):

    provider = MagicMock()

    provider.generate.return_value = (
        "AI Response"
    )

    mock_get_provider.return_value = provider

    result = chat_service.ask(
        transcript="Transcript",
        history=[],
        question="Question",
        provider_name="Ollama",
        model_name="llama3",
    )

    assert result == "AI Response"

    provider.generate.assert_called_once()


@patch(
    "services.ai_chat_service.ProviderFactory.get_provider"
)
def test_ask_stream(
    mock_get_provider,
    chat_service,
):

    provider = MagicMock()

    provider.generate_stream.return_value = iter(
        [
            "Hello",
            " World",
        ]
    )

    mock_get_provider.return_value = provider

    stream = chat_service.ask_stream(
        transcript="Transcript",
        history=[],
        question="Question",
        provider_name="Ollama",
        model_name="llama3",
    )

    assert list(stream) == [
        "Hello",
        " World",
    ]


def test_save_chat(chat_service):

    history = [
        {
            "user": "User",
            "assistant": "Assistant",
        }
    ]

    path = chat_service.save_chat(
        "chat.json",
        history,
    )

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    assert data == history


def test_chat_directory_created(chat_service):

    import os

    assert os.path.exists(
        chat_service.chat_dir
    )


def test_build_prompt_empty_history(chat_service):

    prompt = chat_service.build_prompt(
        transcript="Transcript",
        history=[],
        question="Question?",
    )

    assert "Transcript" in prompt
    assert "Question?" in prompt
    assert "CHAT HISTORY" in prompt


@patch(
    "services.ai_chat_service.ProviderFactory.get_provider"
)
def test_ask_calls_provider_with_correct_arguments(
    mock_get_provider,
    chat_service,
):

    provider = MagicMock()

    provider.generate.return_value = "Answer"

    mock_get_provider.return_value = provider

    chat_service.ask(
        transcript="Transcript",
        history=[],
        question="Explain",
        provider_name="Ollama",
        model_name="qwen",
    )

    _, kwargs = provider.generate.call_args

    assert kwargs["model"] == "qwen"

    assert "Transcript" in kwargs["prompt"]

    assert "Explain" in kwargs["prompt"]


@patch(
    "services.ai_chat_service.ProviderFactory.get_provider"
)
def test_ask_stream_calls_provider(
    mock_get_provider,
    chat_service,
):

    provider = MagicMock()

    provider.generate_stream.return_value = iter(
        ["A"]
    )

    mock_get_provider.return_value = provider

    list(
        chat_service.ask_stream(
            transcript="Transcript",
            history=[],
            question="Explain",
            provider_name="Ollama",
            model_name="qwen",
        )
    )

    provider.generate_stream.assert_called_once()