import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    APP_NAME = "AI Video Analyzer"

    APP_VERSION = "1.0.0"

    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    DEFAULT_PROVIDER = os.getenv(
        "DEFAULT_PROVIDER",
        "Ollama"
    )

    DEFAULT_MODEL = os.getenv(
        "DEFAULT_MODEL",
        "qwen2.5:1.5b"
    )