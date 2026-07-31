"""
tests/test_ai_analysis_agent_service.py
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from services.ai_analysis_agent_service import AIAnalysisService


@pytest.fixture
def analysis_folder(tmp_path, monkeypatch):

    monkeypatch.setattr(
        AIAnalysisService,
        "ANALYSIS_FOLDER",
        str(tmp_path),
    )

    return tmp_path


@patch(
    "services.ai_analysis_agent_service.ProviderFactory.get_provider"
)
def test_analyze_success(
    mock_provider_factory,
):

    provider = MagicMock()

    provider.generate.return_value = (
        "AI Analysis Result"
    )

    mock_provider_factory.return_value = provider

    result = AIAnalysisService.analyze(
        provider_name="Ollama",
        model_name="qwen2.5",
        transcript="Hello World",
        prompt="Summarize",
    )




@patch(
    "services.ai_analysis_agent_service.ProviderFactory.get_provider"
)
def test_provider_not_found(
    mock_provider_factory,
):

    mock_provider_factory.return_value = None

    with pytest.raises(Exception):

        AIAnalysisService.analyze(
            provider_name="Invalid",
            model_name="model",
            transcript="abc",
            prompt="summary",
        )


@patch(
    "services.ai_analysis_agent_service.ProviderFactory.get_provider"
)
def test_generate_exception(
    mock_provider_factory,
):

    provider = MagicMock()

    provider.generate.side_effect = Exception(
        "Generation Failed"
    )

    mock_provider_factory.return_value = provider

    with pytest.raises(Exception):

        AIAnalysisService.analyze(
            provider_name="Ollama",
            model_name="model",
            transcript="text",
            prompt="summary",
        )


def test_save_analysis(
    analysis_folder,
):

    path = AIAnalysisService.save_analysis(
        filename="video1",
        analysis_type="summary",
        content="Analysis Content",
    )

    assert os.path.exists(path)

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        text = file.read()

    assert text == "Analysis Content"


def test_save_analysis_filename(
    analysis_folder,
):

    path = AIAnalysisService.save_analysis(
        "movie",
        "keywords",
        "content",
    )

    assert os.path.basename(path).startswith(
        "movie_keywords_"
    )

    assert path.endswith(".md")


@patch(
    "services.ai_analysis_agent_service.ProviderFactory.get_provider"
)
def test_prompt_contains_transcript(
    mock_provider_factory,
):

    provider = MagicMock()

    provider.generate.return_value = "Done"

    mock_provider_factory.return_value = provider

    transcript = (
        "Artificial Intelligence is amazing."
    )

    AIAnalysisService.analyze(
        provider_name="Ollama",
        model_name="qwen",
        transcript=transcript,
        prompt="Explain",
    )

    prompt = provider.generate.call_args.kwargs[
        "prompt"
    ]

    assert transcript in prompt


@patch(
    "services.ai_analysis_agent_service.ProviderFactory.get_provider"
)
def test_prompt_contains_instruction(
    mock_provider_factory,
):

    provider = MagicMock()

    provider.generate.return_value = "Done"

    mock_provider_factory.return_value = provider

    AIAnalysisService.analyze(
        provider_name="Ollama",
        model_name="qwen",
        transcript="abc",
        prompt="Create summary",
    )

    prompt = provider.generate.call_args.kwargs[
        "prompt"
    ]

    assert "Do not invent facts" in prompt

    assert "Create summary" in prompt


@patch(
    "services.ai_analysis_agent_service.ProviderFactory.get_provider"
)
def test_provider_called_once(
    mock_provider_factory,
):

    provider = MagicMock()

    provider.generate.return_value = "OK"

    mock_provider_factory.return_value = provider

    AIAnalysisService.analyze(
        "Ollama",
        "model",
        "Transcript",
        "Prompt",
    )

    mock_provider_factory.assert_called_once_with(
        "Ollama"
    )