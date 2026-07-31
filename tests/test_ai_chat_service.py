import os
from unittest.mock import MagicMock, mock_open, patch

from services.ai_chat_service import AIChatService


class TestAIChatService:

    @patch("services.ai_chat_service.os.makedirs")
    def test_init(
        self,
        mock_makedirs,
    ):
        service = AIChatService()

        assert service.chat_dir == "chat_history"

        mock_makedirs.assert_called_once_with(
            "chat_history",
            exist_ok=True,
        )

    @patch("services.ai_chat_service.os.makedirs")
    def test_build_prompt(
        self,
        mock_makedirs,
    ):
        service = AIChatService()

        history = [
            {
                "user": "Hello",
                "assistant": "Hi",
            },
            {
                "user": "Topic?",
                "assistant": "Python",
            },
        ]

        prompt = service.build_prompt(
            transcript="Video Transcript",
            history=history,
            question="Explain",
        )

        assert "Video Transcript" in prompt
        assert "Hello" in prompt
        assert "Hi" in prompt
        assert "Topic?" in prompt
        assert "Python" in prompt
        assert "Explain" in prompt
        assert "CURRENT QUESTION" in prompt

    @patch("services.ai_chat_service.ProviderFactory.get_provider")
    @patch("services.ai_chat_service.os.makedirs")
    def test_ask(
        self,
        mock_makedirs,
        mock_get_provider,
    ):
        provider = MagicMock()
        provider.generate.return_value = "AI Response"

        mock_get_provider.return_value = provider

        service = AIChatService()

        history = []

        result = service.ask(
            transcript="Transcript",
            history=history,
            question="Question",
            provider_name="Ollama",
            model_name="llama3.1",
        )

        assert result == "AI Response"

        mock_get_provider.assert_called_once_with(
            "Ollama"
        )

        args = provider.generate.call_args.kwargs

        assert args["model"] == "llama3.1"
        assert "Transcript" in args["prompt"]
        assert "Question" in args["prompt"]

    @patch("builtins.open", new_callable=mock_open)
    @patch("services.ai_chat_service.os.makedirs")
    def test_save_chat(
        self,
        mock_makedirs,
        mock_file,
    ):
        service = AIChatService()

        history = [
            {
                "user": "Hello",
                "assistant": "Hi",
            }
        ]

        path = service.save_chat(
            "chat.json",
            history,
        )

        expected = os.path.join(
            "chat_history",
            "chat.json",
        )

        assert path == expected

        mock_file.assert_called_once_with(
            expected,
            "w",
            encoding="utf-8",
        )

    @patch("services.ai_chat_service.ProviderFactory.get_provider")
    @patch("services.ai_chat_service.os.makedirs")
    def test_ask_stream(
        self,
        mock_makedirs,
        mock_get_provider,
    ):
        provider = MagicMock()

        provider.generate_stream.return_value = iter(
            [
                "Hello",
                " World",
            ]
        )

        mock_get_provider.return_value = provider

        service = AIChatService()

        result = list(
            service.ask_stream(
                transcript="Transcript",
                history=[],
                question="Question",
                provider_name="Ollama",
                model_name="llama3.1",
            )
        )

        assert result == [
            "Hello",
            " World",
        ]

        args = provider.generate_stream.call_args.kwargs

        assert args["model"] == "llama3.1"
        assert "Transcript" in args["prompt"]
        assert "Question" in args["prompt"]