import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from services.ai_analysis_service import AIAnalysisService


class TestAIAnalysisService:

    @patch("services.ai_analysis_service.os.makedirs")
    @patch("services.ai_analysis_service.ProviderFactory.get_provider")
    def test_analyze_success(
        self,
        mock_get_provider,
        mock_makedirs,
    ):
        provider = MagicMock()
        provider.generate.return_value = "Analysis Result"

        mock_get_provider.return_value = provider

        result = AIAnalysisService.analyze(
            provider_name="Ollama",
            model_name="llama3.1",
            transcript="Video transcript",
            prompt="Summarize",
        )

        assert result == "Analysis Result"

        mock_makedirs.assert_called_once_with(
            AIAnalysisService.ANALYSIS_FOLDER,
            exist_ok=True,
        )

        mock_get_provider.assert_called_once_with(
            "Ollama"
        )

        args = provider.generate.call_args.kwargs

        assert args["model"] == "llama3.1"
        assert "Video transcript" in args["prompt"]
        assert "Summarize" in args["prompt"]

    @patch("services.ai_analysis_service.os.makedirs")
    @patch("services.ai_analysis_service.ProviderFactory.get_provider")
    def test_analyze_provider_not_found(
        self,
        mock_get_provider,
        mock_makedirs,
    ):
        mock_get_provider.return_value = None

        with pytest.raises(Exception) as exc:
            AIAnalysisService.analyze(
                provider_name="Unknown",
                model_name="model",
                transcript="text",
                prompt="prompt",
            )

        assert (
            str(exc.value)
            == "Provider 'Unknown' not found."
        )

    @patch("services.ai_analysis_service.datetime")
    @patch("services.ai_analysis_service.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_analysis(
        self,
        mock_file,
        mock_makedirs,
        mock_datetime,
    ):
        mock_datetime.now.return_value.strftime.return_value = (
            "20260101_120000"
        )

        result = AIAnalysisService.save_analysis(
            filename="video1",
            analysis_type="summary",
            content="Analysis text",
        )

        expected = os.path.join(
            AIAnalysisService.ANALYSIS_FOLDER,
            "video1_summary_20260101_120000.md",
        )

        assert result == expected

        mock_makedirs.assert_called_once_with(
            AIAnalysisService.ANALYSIS_FOLDER,
            exist_ok=True,
        )

        mock_file.assert_called_once_with(
            expected,
            "w",
            encoding="utf-8",
        )

        mock_file().write.assert_called_once_with(
            "Analysis text"
        )