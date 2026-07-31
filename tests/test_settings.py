import importlib
import os

import config.settings as settings


def reload_settings():
    return importlib.reload(settings)


def test_app_name():
    s = reload_settings()
    assert s.APP_NAME == "AI Video Analysis Agent"


def test_app_version():
    s = reload_settings()
    assert s.APP_VERSION == "1.0.0"


def test_default_ollama_url(monkeypatch):
    monkeypatch.delenv("OLLAMA_URL", raising=False)

    s = reload_settings()

    assert s.OLLAMA_URL == "http://localhost:11434"


def test_custom_ollama_url(monkeypatch):
    monkeypatch.setenv("OLLAMA_URL", "http://127.0.0.1:9999")

    s = reload_settings()

    assert s.OLLAMA_URL == "http://127.0.0.1:9999"


def test_default_provider():
    s = reload_settings()
    assert s.DEFAULT_PROVIDER == "Ollama"


def test_default_model():
    s = reload_settings()
    assert s.DEFAULT_MODEL == "qwen2.5:1.5b"


def test_mysql_defaults(monkeypatch):
    monkeypatch.delenv("MYSQL_HOST", raising=False)
    monkeypatch.delenv("MYSQL_PORT", raising=False)
    monkeypatch.delenv("MYSQL_DATABASE", raising=False)
    monkeypatch.delenv("MYSQL_USER", raising=False)
    monkeypatch.delenv("MYSQL_PASSWORD", raising=False)

    s = reload_settings()

    assert s.MYSQL_HOST == "localhost"
    assert s.MYSQL_PORT == 3306
    assert s.MYSQL_DATABASE == "video_analysis"
    assert s.MYSQL_USER == "root"
    assert s.MYSQL_PASSWORD == ""


def test_custom_mysql(monkeypatch):
    monkeypatch.setenv("MYSQL_HOST", "db")
    monkeypatch.setenv("MYSQL_PORT", "3307")
    monkeypatch.setenv("MYSQL_DATABASE", "ai")
    monkeypatch.setenv("MYSQL_USER", "admin")
    monkeypatch.setenv("MYSQL_PASSWORD", "secret")

    s = reload_settings()

    assert s.MYSQL_HOST == "db"
    assert s.MYSQL_PORT == 3307
    assert s.MYSQL_DATABASE == "ai"
    assert s.MYSQL_USER == "admin"
    assert s.MYSQL_PASSWORD == "secret"


def test_all_required_attributes_exist():
    s = reload_settings()

    required = [
        "APP_NAME",
        "APP_VERSION",
        "BASE_DIR",
        "UPLOAD_DIR",
        "AUDIO_DIR",
        "TRANSCRIPT_DIR",
        "REPORT_DIR",
        "EXPORT_DIR",
        "LOG_DIR",
        "TEMP_DIR",
        "MAX_UPLOAD_SIZE",
        "SUPPORTED_VIDEO_FORMATS",
        "DEFAULT_PROVIDER",
        "DEFAULT_MODEL",
        "DEFAULT_TEMPERATURE",
        "DEFAULT_MAX_TOKENS",
        "MYSQL_HOST",
        "MYSQL_PORT",
        "MYSQL_DATABASE",
        "MYSQL_USER",
        "MYSQL_PASSWORD",
        "OLLAMA_URL",
        "WHISPER_MODEL",
    ]

    for attr in required:
        assert hasattr(s, attr)