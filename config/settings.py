"""
config/settings.py
"""

from __future__ import annotations

import os
from pathlib import Path

# =============================================================================
# Base Paths
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# Application
# =============================================================================

APP_NAME = "AI Video Analysis Agent"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# =============================================================================
# Directories
# =============================================================================

UPLOAD_DIR = BASE_DIR / "uploads"
AUDIO_DIR = BASE_DIR / "audio"
TRANSCRIPT_DIR = BASE_DIR / "transcripts"
REPORT_DIR = BASE_DIR / "reports"
EXPORT_DIR = BASE_DIR / "exports"
CHAT_DIR = BASE_DIR / "chat_history"
ANALYSIS_DIR = BASE_DIR / "analysis"
LOG_DIR = BASE_DIR / "logs"
TEMP_DIR = BASE_DIR / "temp"

# =============================================================================
# Upload Settings
# =============================================================================

MAX_UPLOAD_SIZE = 1024 * 1024 * 1024  # 1 GB

SUPPORTED_VIDEO_FORMATS = [
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
]

# =============================================================================
# AI Defaults
# =============================================================================

DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "Ollama")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen2.5:1.5b")

DEFAULT_TEMPERATURE = float(
    os.getenv("DEFAULT_TEMPERATURE", "0.7")
)

DEFAULT_MAX_TOKENS = int(
    os.getenv("DEFAULT_MAX_TOKENS", "2048")
)

# =============================================================================
# Ollama
# =============================================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434",
)

# =============================================================================
# Whisper
# =============================================================================

WHISPER_MODEL = os.getenv(
    "WHISPER_MODEL",
    "base",
)

# =============================================================================
# MySQL
# =============================================================================

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DATABASE = os.getenv(
    "MYSQL_DATABASE",
    "video_analysis",
)
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

# =============================================================================
# Create Required Directories
# =============================================================================

DIRECTORIES = [
    UPLOAD_DIR,
    AUDIO_DIR,
    TRANSCRIPT_DIR,
    REPORT_DIR,
    EXPORT_DIR,
    CHAT_DIR,
    ANALYSIS_DIR,
    LOG_DIR,
    TEMP_DIR,
]

for directory in DIRECTORIES:
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )