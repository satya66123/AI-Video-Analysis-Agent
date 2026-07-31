import os

import pytest

from services.ai_analysis_service import AIAnalysisService


class DummyProvider:
    def __init__(self):
        self.calls = []

    def generate(self, *, prompt, model):
        self.calls.append(
            {
                "prompt": prompt,
                "model": model,
            }
        )
        return "Analysis Result"


@pytest.fixture
def analysis_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(
        AIAnalysisService,
        "ANALYSIS_FOLDER",
        str(tmp_path),
    )
    return tmp_path


def test_analyze_success(monkeypatch):
    provider = DummyProvider()

    monkeypatch.setattr(
        "providers.provider_factory.ProviderFactory.get_provider",
        lambda name: provider,
    )

    result = AIAnalysisService.analyze(
        provider_name="Ollama",
        model_name="llama3.1",
        transcript="Hello World",
        prompt="Summarize",
    )

    assert result == "Analysis Result"

    assert len(provider.calls) == 1
    assert provider.calls[0]["model"] == "llama3.1"
    assert "Hello World" in provider.calls[0]["prompt"]
    assert "Summarize" in provider.calls[0]["prompt"]


def test_analyze_provider_not_found(monkeypatch):
    monkeypatch.setattr(
        "providers.provider_factory.ProviderFactory.get_provider",
        lambda name: None,
    )

    with pytest.raises(Exception, match="Provider"):
        AIAnalysisService.analyze(
            "Ollama",
            "model",
            "text",
            "prompt",
        )


def test_save_analysis(analysis_dir):
    path = AIAnalysisService.save_analysis(
        filename="video1",
        analysis_type="summary",
        content="My analysis",
    )

    assert os.path.exists(path)

    assert os.path.basename(path).startswith(
        "video1_summary_"
    )

    assert path.endswith(".md")

    with open(path, encoding="utf-8") as f:
        assert f.read() == "My analysis"


def test_prompt_contains_transcript(monkeypatch):
    provider = DummyProvider()

    monkeypatch.setattr(
        "providers.provider_factory.ProviderFactory.get_provider",
        lambda name: provider,
    )

    AIAnalysisService.analyze(
        "Ollama",
        "model",
        "Transcript Text",
        "Explain",
    )

    prompt = provider.calls[0]["prompt"]

    assert "Transcript Text" in prompt


def test_prompt_contains_instruction(monkeypatch):
    provider = DummyProvider()

    monkeypatch.setattr(
        "providers.provider_factory.ProviderFactory.get_provider",
        lambda name: provider,
    )

    AIAnalysisService.analyze(
        "Ollama",
        "model",
        "abc",
        "Summarize",
    )

    prompt = provider.calls[0]["prompt"]

    assert "Do not invent facts" in prompt
    assert "Analyze ONLY the transcript" in prompt


def test_provider_called_once(monkeypatch):
    provider = DummyProvider()

    monkeypatch.setattr(
        "providers.provider_factory.ProviderFactory.get_provider",
        lambda name: provider,
    )

    AIAnalysisService.analyze(
        "Ollama",
        "model",
        "text",
        "prompt",
    )

    assert len(provider.calls) == 1