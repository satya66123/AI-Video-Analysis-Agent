"""
config/constants.py
"""

WORKFLOW_STAGES = [
    "Upload",
    "Audio",
    "Transcript",
    "Analysis",
    "Report",
    "Export",
    "Chat",
]

WORKFLOW_PROGRESS = {
    "Upload": 10,
    "Audio": 25,
    "Transcript": 40,
    "Analysis": 60,
    "Report": 75,
    "Export": 90,
    "Chat": 100,
}

SUCCESS = "SUCCESS"
FAILED = "FAILED"
RUNNING = "RUNNING"
IDLE = "IDLE"

DEFAULT_THEME = "Dark"

REPORT_FORMATS = [
    "PDF",
    "DOCX",
    "TXT",
    "HTML",
    "Markdown",
]

EXPORT_FORMATS = [
    "JSON",
    "CSV",
    "PDF",
    "DOCX",
]