from unittest.mock import MagicMock, patch

import pytest

from providers.anthropic_provider import AnthropicProvider


class TestAnthropicProvider:

    @patch("providers.anthropic_provider.anthropic.Anthropic")
    @patch("providers.anthropic_provider.os.getenv")
    def test_init_success(
        self,
        mock_getenv,
        mock_anthropic,
    ):
        mock_getenv.return_value = "test-key"

        provider = AnthropicProvider()

        assert provider.api_key == "test-key"

        mock_anthropic.assert_called_once_with(
            api_key="test-key"
        )

    @patch("providers.anthropic_provider.os.getenv")
    def test_init_no_api_key(
        self,
        mock_getenv,
    ):
        mock_getenv.return_value = None

        with pytest.raises(ValueError) as exc:
            AnthropicProvider()

        assert (
            str(exc.value)
            == "ANTHROPIC_API_KEY environment variable not found."
        )

    @patch("providers.anthropic_provider.anthropic.Anthropic")
    @patch("providers.anthropic_provider.os.getenv")
    def test_get_models(
        self,
        mock_getenv,
        mock_anthropic,
    ):
        mock_getenv.return_value = "key"

        provider = AnthropicProvider()

        models = provider.get_models()

        assert models == [
            "claude-opus-4.1",
            "claude-sonnet-4",
            "claude-3.7-sonnet",
            "claude-3.5-sonnet",
            "claude-3.5-haiku",
        ]

    @patch("providers.anthropic_provider.anthropic.Anthropic")
    @patch("providers.anthropic_provider.os.getenv")
    def test_generate_success(
        self,
        mock_getenv,
        mock_anthropic,
    ):
        mock_getenv.return_value = "key"

        response = MagicMock()
        response.content = [
            MagicMock(text="Hello World")
        ]

        client = MagicMock()
        client.messages.create.return_value = response

        mock_anthropic.return_value = client

        provider = AnthropicProvider()

        result = provider.generate(
            prompt="Hello",
            model="claude-3.5-haiku",
        )

        assert result == "Hello World"

        client.messages.create.assert_called_once_with(
            model="claude-3.5-haiku",
            max_tokens=1024,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": "Hello",
                }
            ],
        )

    @patch("providers.anthropic_provider.anthropic.Anthropic")
    @patch("providers.anthropic_provider.os.getenv")
    def test_generate_exception(
        self,
        mock_getenv,
        mock_anthropic,
    ):
        mock_getenv.return_value = "key"

        client = MagicMock()
        client.messages.create.side_effect = Exception(
            "API Error"
        )

        mock_anthropic.return_value = client

        provider = AnthropicProvider()

        result = provider.generate(
            prompt="Hello",
            model="claude-3.5-haiku",
        )

        assert result == "Error: API Error"

    @patch("providers.anthropic_provider.anthropic.Anthropic")
    @patch("providers.anthropic_provider.os.getenv")
    def test_generate_stream_success(
        self,
        mock_getenv,
        mock_anthropic,
    ):
        mock_getenv.return_value = "key"

        provider = AnthropicProvider()

        with patch.object(
            provider,
            "generate",
            return_value="Stream Result",
        ):
            result = list(
                provider.generate_stream(
                    "Hello",
                    "claude-3.5-haiku",
                )
            )

        assert result == ["Stream Result"]

    @patch("providers.anthropic_provider.anthropic.Anthropic")
    @patch("providers.anthropic_provider.os.getenv")
    def test_generate_stream_exception(
        self,
        mock_getenv,
        mock_anthropic,
    ):
        mock_getenv.return_value = "key"

        provider = AnthropicProvider()

        with patch.object(
            provider,
            "generate",
            side_effect=Exception("Stream Error"),
        ):
            result = list(
                provider.generate_stream(
                    "Hello",
                    "claude-3.5-haiku",
                )
            )

        assert result == [
            "Error: Stream Error"
        ]

    @patch("providers.anthropic_provider.anthropic.Anthropic")
    @patch("providers.anthropic_provider.os.getenv")
    def test_health_check_success(
        self,
        mock_getenv,
        mock_anthropic,
    ):
        mock_getenv.return_value = "key"

        client = MagicMock()

        mock_anthropic.return_value = client

        provider = AnthropicProvider()

        assert provider.health_check() is True

        client.messages.create.assert_called_once_with(
            model="claude-3.5-haiku",
            max_tokens=10,
            messages=[
                {
                    "role": "user",
                    "content": "Hello",
                }
            ],
        )

    @patch("providers.anthropic_provider.anthropic.Anthropic")
    @patch("providers.anthropic_provider.os.getenv")
    def test_health_check_failure(
        self,
        mock_getenv,
        mock_anthropic,
    ):
        mock_getenv.return_value = "key"

        client = MagicMock()
        client.messages.create.side_effect = Exception()

        mock_anthropic.return_value = client

        provider = AnthropicProvider()

        assert provider.health_check() is False