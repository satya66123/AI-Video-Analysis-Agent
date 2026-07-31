import os
import importlib

import pytest


def reload_settings():
    """
    Reload config.settings after environment changes.
    """
    import config.settings
    importlib.reload(config.settings)
    return config.settings.Settings


def test_app_name():
    Settings = reload_settings()
    assert Settings.APP_NAME == "AI Video Analyzer"


def test_app_version():
    Settings = reload_settings()
    assert Settings.APP_VERSION == "1.0.0"


def test_default_ollama_url(monkeypatch):
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)

    Settings = reload_settings()

    assert (
        Settings.OLLAMA_BASE_URL
        == "http://localhost:11434"
    )


def test_custom_ollama_url(monkeypatch):
    monkeypatch.setenv(
        "OLLAMA_BASE_URL",
        "http://127.0.0.1:11434"
    )

    Settings = reload_settings()

    assert (
        Settings.OLLAMA_BASE_URL
        == "http://127.0.0.1:11434"
    )


def test_default_provider(monkeypatch):
    monkeypatch.delenv("DEFAULT_PROVIDER", raising=False)

    Settings = reload_settings()

    assert Settings.DEFAULT_PROVIDER == "Ollama"


def test_custom_provider(monkeypatch):
    monkeypatch.setenv(
        "DEFAULT_PROVIDER",
        "OpenAI"
    )

    Settings = reload_settings()

    assert Settings.DEFAULT_PROVIDER == "OpenAI"


def test_default_model(monkeypatch):
    monkeypatch.delenv("DEFAULT_MODEL", raising=False)

    Settings = reload_settings()

    assert Settings.DEFAULT_MODEL == "qwen2.5:1.5b"


def test_custom_model(monkeypatch):
    monkeypatch.setenv(
        "DEFAULT_MODEL",
        "llama3.1:8b"
    )

    Settings = reload_settings()

    assert Settings.DEFAULT_MODEL == "llama3.1:8b"


def test_all_required_attributes_exist():
    Settings = reload_settings()

    assert hasattr(Settings, "APP_NAME")
    assert hasattr(Settings, "APP_VERSION")
    assert hasattr(Settings, "OLLAMA_BASE_URL")
    assert hasattr(Settings, "DEFAULT_PROVIDER")
    assert hasattr(Settings, "DEFAULT_MODEL")