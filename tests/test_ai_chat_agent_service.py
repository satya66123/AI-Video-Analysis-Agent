"""
tests/test_ai_chat_agent_service.py
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from services.ai_chat_agent_service import AIChatService



@pytest.fixture
def chat_service(tmp_path):

    AIChatService.CHAT_FOLDER = tmp_path

    AIChatService.CHAT_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    service = AIChatService()

    return service


def test_build_prompt():

    history = [
        {
            "user": "Hello",
            "assistant": "Hi"
        }
    ]

    prompt = AIChatService.build_prompt(
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
    "services.ai_chat_agent_service.ProviderFactory.get_provider"
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
        model_name="qwen",
    )

    assert result == "AI Response"

    provider.generate.assert_called_once()


@patch(
    "services.ai_chat_agent_service.ProviderFactory.get_provider"
)
def test_ask_invalid_provider(
    mock_get_provider,
    chat_service,
):

    mock_get_provider.return_value = None

    with pytest.raises(ValueError):

        chat_service.ask(
            transcript="Transcript",
            history=[],
            question="Question",
            provider_name="Invalid",
            model_name="model",
        )


@patch(
    "services.ai_chat_agent_service.ProviderFactory.get_provider"
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
        model_name="qwen",
    )

    assert list(stream) == [
        "Hello",
        " World",
    ]


def test_save_chat(chat_service):

    history = [
        {
            "user": "Hi",
            "assistant": "Hello",
        }
    ]

    path = chat_service.save_chat(
        "chat.json",
        history,
    )

    assert path.exists()

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    assert data == history


def test_load_chat(chat_service):

    history = [
        {
            "user": "User",
            "assistant": "Bot",
        }
    ]

    chat_service.save_chat(
        "sample.json",
        history,
    )

    loaded = chat_service.load_chat(
        "sample.json"
    )

    assert loaded == history


def test_load_missing_chat(
    chat_service,
):

    assert (
        chat_service.load_chat(
            "missing.json"
        )
        == []
    )


def test_list_chats(chat_service):

    chat_service.save_chat(
        "a.json",
        [],
    )

    chat_service.save_chat(
        "b.json",
        [],
    )

    chats = AIChatService.list_chats()

    assert len(chats) == 2

    assert chats[0].name == "a.json"

    assert chats[1].name == "b.json"


def test_delete_chat(
    chat_service,
):

    chat_service.save_chat(
        "delete.json",
        [],
    )

    assert chat_service.delete_chat(
        "delete.json"
    )

    assert not (
        chat_service.CHAT_FOLDER
        / "delete.json"
    ).exists()


def test_delete_missing_chat(
    chat_service,
):

    assert (
        chat_service.delete_chat(
            "missing.json"
        )
        is False
    )


def test_clear_chat(
    chat_service,
):

    chat_service.save_chat(
        "one.json",
        [],
    )

    chat_service.save_chat(
        "two.json",
        [],
    )

    chat_service.clear_chat()

    assert (
        len(
            list(
                chat_service.CHAT_FOLDER.glob(
                    "*.json"
                )
            )
        )
        == 0
    )


def test_create_message():

    message = AIChatService.create_message(
        "User",
        "Assistant",
    )

    assert message["user"] == "User"

    assert (
        message["assistant"]
        == "Assistant"
    )

    assert "timestamp" in message
