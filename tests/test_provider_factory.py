from unittest.mock import MagicMock, patch

import pytest

from providers.provider_factory import ProviderFactory


class TestProviderFactory:

    @patch("providers.provider_factory.OllamaProvider")
    def test_get_ollama_provider(
        self,
        mock_provider,
    ):
        instance = MagicMock()
        mock_provider.return_value = instance

        result = ProviderFactory.get_provider(
            "Ollama"
        )

        assert result is instance
        mock_provider.assert_called_once()

    @patch("providers.provider_factory.OpenAIProvider")
    def test_get_openai_provider(
        self,
        mock_provider,
    ):
        instance = MagicMock()
        mock_provider.return_value = instance

        result = ProviderFactory.get_provider(
            "OpenAI"
        )

        assert result is instance
        mock_provider.assert_called_once()

    @patch("providers.provider_factory.AnthropicProvider")
    def test_get_anthropic_provider(
        self,
        mock_provider,
    ):
        instance = MagicMock()
        mock_provider.return_value = instance

        result = ProviderFactory.get_provider(
            "Anthropic"
        )

        assert result is instance
        mock_provider.assert_called_once()

    def test_invalid_provider(self):
        with pytest.raises(ValueError) as exc:
            ProviderFactory.get_provider(
                "Invalid"
            )

        assert (
            str(exc.value)
            == "Unsupported provider: Invalid"
        )

    def test_none_provider(self):
        with pytest.raises(ValueError):
            ProviderFactory.get_provider(None)

    def test_empty_provider(self):
        with pytest.raises(ValueError):
            ProviderFactory.get_provider("")