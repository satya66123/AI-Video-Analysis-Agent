"""
config/paths.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

UPLOADS = ROOT / "uploads"
AUDIO = ROOT / "audio"
TRANSCRIPTS = ROOT / "transcripts"
REPORTS = ROOT / "reports"
EXPORTS = ROOT / "exports"
LOGS = ROOT / "logs"
TEMP = ROOT / "temp"
MODELS = ROOT / "models"

DIRECTORIES = [
    UPLOADS,
    AUDIO,
    TRANSCRIPTS,
    REPORTS,
    EXPORTS,
    LOGS,
    TEMP,
]

for directory in DIRECTORIES:
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )