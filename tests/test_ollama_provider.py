import requests
from unittest.mock import MagicMock, patch

from providers.ollama_provider import OllamaProvider


class TestOllamaProvider:

    @patch("providers.ollama_provider.requests.get")
    def test_get_models_success(
        self,
        mock_get,
    ):
        response = MagicMock()
        response.json.return_value = {
            "models": ["llama3.1"]
        }

        mock_get.return_value = response

        provider = OllamaProvider()

        result = provider.get_models()

        assert result == {
            "models": ["llama3.1"]
        }

        mock_get.assert_called_once_with(
            "http://localhost:11434/api/tags",
            timeout=10,
        )

    @patch("providers.ollama_provider.requests.get")
    def test_get_models_exception(
        self,
        mock_get,
    ):
        mock_get.side_effect = requests.exceptions.RequestException

        provider = OllamaProvider()

        assert provider.get_models() == {}

    @patch("providers.ollama_provider.requests.post")
    def test_generate_success(
        self,
        mock_post,
    ):
        response = MagicMock()
        response.json.return_value = {
            "response": "Hello"
        }

        mock_post.return_value = response

        provider = OllamaProvider()

        result = provider.generate(
            "Hi",
            "llama3.1",
        )

        assert result == "Hello"

        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1",
                "prompt": "Hi",
                "stream": False,
            },
            timeout=300,
        )

    @patch("providers.ollama_provider.requests.post")
    def test_generate_timeout(
        self,
        mock_post,
    ):
        mock_post.side_effect = requests.exceptions.Timeout

        provider = OllamaProvider()

        result = provider.generate(
            "Hi",
            "llama3.1",
        )

        assert result == "Error: Request timed out."

    @patch("providers.ollama_provider.requests.post")
    def test_generate_connection_error(
        self,
        mock_post,
    ):
        mock_post.side_effect = requests.exceptions.ConnectionError

        provider = OllamaProvider()

        result = provider.generate(
            "Hi",
            "llama3.1",
        )

        assert result == "Error: Unable to connect to Ollama."

    @patch("providers.ollama_provider.requests.post")
    def test_generate_request_exception(
        self,
        mock_post,
    ):
        mock_post.side_effect = requests.exceptions.RequestException(
            "Failure"
        )

        provider = OllamaProvider()

        result = provider.generate(
            "Hi",
            "llama3.1",
        )

        assert result == "Error: Failure"

    @patch("providers.ollama_provider.requests.post")
    def test_generate_stream_success(
        self,
        mock_post,
    ):
        response = MagicMock()

        response.iter_lines.return_value = [
            b'{"response":"Hello"}',
            b'{"response":" World"}',
        ]

        mock_post.return_value = response

        provider = OllamaProvider()

        result = list(
            provider.generate_stream(
                "Hi",
                "llama3.1",
            )
        )

        assert result == [
            "Hello",
            " World",
        ]

    @patch("providers.ollama_provider.requests.post")
    def test_generate_stream_ignores_empty_lines(
        self,
        mock_post,
    ):
        response = MagicMock()

        response.iter_lines.return_value = [
            b"",
            b'{"response":"Hello"}',
            b"",
        ]

        mock_post.return_value = response

        provider = OllamaProvider()

        result = list(
            provider.generate_stream(
                "Hi",
                "llama3.1",
            )
        )

        assert result == [
            "Hello",
        ]

    @patch("providers.ollama_provider.requests.post")
    def test_generate_stream_timeout(
        self,
        mock_post,
    ):
        mock_post.side_effect = requests.exceptions.Timeout

        provider = OllamaProvider()

        result = list(
            provider.generate_stream(
                "Hi",
                "llama3.1",
            )
        )

        assert result == [
            "Error: Request timed out."
        ]

    @patch("providers.ollama_provider.requests.post")
    def test_generate_stream_connection_error(
        self,
        mock_post,
    ):
        mock_post.side_effect = requests.exceptions.ConnectionError

        provider = OllamaProvider()

        result = list(
            provider.generate_stream(
                "Hi",
                "llama3.1",
            )
        )

        assert result == [
            "Error: Unable to connect to Ollama."
        ]

    @patch("providers.ollama_provider.requests.post")
    def test_generate_stream_request_exception(
        self,
        mock_post,
    ):
        mock_post.side_effect = requests.exceptions.RequestException(
            "Failure"
        )

        provider = OllamaProvider()

        result = list(
            provider.generate_stream(
                "Hi",
                "llama3.1",
            )
        )

        assert result == [
            "Error: Failure"
        ]

    @patch("providers.ollama_provider.requests.get")
    def test_health_check_success(
        self,
        mock_get,
    ):
        response = MagicMock()

        mock_get.return_value = response

        provider = OllamaProvider()

        assert provider.health_check() is True

        mock_get.assert_called_once_with(
            "http://localhost:11434/api/tags",
            timeout=5,
        )

    @patch("providers.ollama_provider.requests.get")
    def test_health_check_failure(
        self,
        mock_get,
    ):
        mock_get.side_effect = requests.exceptions.RequestException

        provider = OllamaProvider()

        assert provider.health_check() is False