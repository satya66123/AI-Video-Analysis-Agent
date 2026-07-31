from unittest.mock import MagicMock, patch

import pytest

from providers.openai_provider import OpenAIProvider


class TestOpenAIProvider:

    @patch("providers.openai_provider.OpenAI")
    @patch("providers.openai_provider.os.getenv")
    def test_init_success(
        self,
        mock_getenv,
        mock_openai,
    ):
        mock_getenv.return_value = "test-key"

        provider = OpenAIProvider()

        assert provider.api_key == "test-key"

        mock_openai.assert_called_once_with(
            api_key="test-key"
        )

    @patch("providers.openai_provider.os.getenv")
    def test_init_missing_api_key(
        self,
        mock_getenv,
    ):
        mock_getenv.return_value = None

        with pytest.raises(ValueError) as exc:
            OpenAIProvider()

        assert (
            str(exc.value)
            == "OPENAI_API_KEY environment variable not found."
        )

    @patch("providers.openai_provider.OpenAI")
    @patch("providers.openai_provider.os.getenv")
    def test_get_models_success(
        self,
        mock_getenv,
        mock_openai,
    ):
        mock_getenv.return_value = "key"

        model1 = MagicMock(id="gpt-4o")
        model2 = MagicMock(id="gpt-5")

        models = MagicMock()
        models.data = [model1, model2]

        client = MagicMock()
        client.models.list.return_value = models

        mock_openai.return_value = client

        provider = OpenAIProvider()

        assert provider.get_models() == [
            "gpt-4o",
            "gpt-5",
        ]

    @patch("providers.openai_provider.OpenAI")
    @patch("providers.openai_provider.os.getenv")
    def test_get_models_exception(
        self,
        mock_getenv,
        mock_openai,
    ):
        mock_getenv.return_value = "key"

        client = MagicMock()
        client.models.list.side_effect = Exception()

        mock_openai.return_value = client

        provider = OpenAIProvider()

        assert provider.get_models() == []

    @patch("providers.openai_provider.OpenAI")
    @patch("providers.openai_provider.os.getenv")
    def test_generate_success(
        self,
        mock_getenv,
        mock_openai,
    ):
        mock_getenv.return_value = "key"

        response = MagicMock()
        response.output_text = "Hello World"

        client = MagicMock()
        client.responses.create.return_value = response

        mock_openai.return_value = client

        provider = OpenAIProvider()

        result = provider.generate(
            "Hello",
            "gpt-5",
        )

        assert result == "Hello World"

        client.responses.create.assert_called_once_with(
            model="gpt-5",
            input="Hello",
        )

    @patch("providers.openai_provider.OpenAI")
    @patch("providers.openai_provider.os.getenv")
    def test_generate_exception(
        self,
        mock_getenv,
        mock_openai,
    ):
        mock_getenv.return_value = "key"

        client = MagicMock()
        client.responses.create.side_effect = Exception(
            "API Error"
        )

        mock_openai.return_value = client

        provider = OpenAIProvider()

        result = provider.generate(
            "Hello",
            "gpt-5",
        )

        assert result == "Error: API Error"

    @patch("providers.openai_provider.OpenAI")
    @patch("providers.openai_provider.os.getenv")
    def test_generate_stream_success(
        self,
        mock_getenv,
        mock_openai,
    ):
        mock_getenv.return_value = "key"

        provider = OpenAIProvider()

        with patch.object(
            provider,
            "generate",
            return_value="Streaming",
        ):
            result = list(
                provider.generate_stream(
                    "Hello",
                    "gpt-5",
                )
            )

        assert result == ["Streaming"]

    @patch("providers.openai_provider.OpenAI")
    @patch("providers.openai_provider.os.getenv")
    def test_generate_stream_exception(
        self,
        mock_getenv,
        mock_openai,
    ):
        mock_getenv.return_value = "key"

        provider = OpenAIProvider()

        with patch.object(
            provider,
            "generate",
            side_effect=Exception("Stream Error"),
        ):
            result = list(
                provider.generate_stream(
                    "Hello",
                    "gpt-5",
                )
            )

        assert result == [
            "Error: Stream Error"
        ]

    @patch("providers.openai_provider.OpenAI")
    @patch("providers.openai_provider.os.getenv")
    def test_health_check_success(
        self,
        mock_getenv,
        mock_openai,
    ):
        mock_getenv.return_value = "key"

        client = MagicMock()

        mock_openai.return_value = client

        provider = OpenAIProvider()

        assert provider.health_check() is True

        client.models.list.assert_called_once()

    @patch("providers.openai_provider.OpenAI")
    @patch("providers.openai_provider.os.getenv")
    def test_health_check_failure(
        self,
        mock_getenv,
        mock_openai,
    ):
        mock_getenv.return_value = "key"

        client = MagicMock()
        client.models.list.side_effect = Exception()

        mock_openai.return_value = client

        provider = OpenAIProvider()

        assert provider.health_check() is False