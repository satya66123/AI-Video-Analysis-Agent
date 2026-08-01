# Documentation

![Documentation](https://img.shields.io/badge/Documentation-Complete-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)
![Tests](https://img.shields.io/badge/Tests-531%20Passed-success)

Welcome to the **AI Video Analysis Agent** documentation.

This project is a Streamlit-based application that automates the complete video analysis workflow using artificial intelligence. It supports video upload, metadata extraction, audio extraction, speech transcription, AI-powered analysis, transcript-based chat, report generation, and exporting reports in multiple formats.

---

# Features

- Video Upload
- Duplicate Video Detection
- Video Metadata Extraction
- Audio Extraction
- Audio Metadata Generation
- Whisper Speech-to-Text
- AI Transcript Analysis
- AI Chat Assistant
- Professional Report Generation
- Export Reports (PDF, HTML, Markdown, TXT, JSON)
- History Management
- Multi-AI Provider Support
- Local JSON Storage

---

# Workflow

```
Upload Video
      │
      ▼
Metadata Extraction
      │
      ▼
Audio Extraction
      │
      ▼
Speech Transcription
      │
      ▼
AI Analysis
      │
      ▼
AI Chat
      │
      ▼
Report Generation
      │
      ▼
Export
```

---

# Run the Application

Install dependencies

```bash
pip install -r requirements.txt
```

Start the application

```bash
streamlit run app_agent.py
```

---

# Project Structure

```
app_agent.py
agents/
services/
providers/
ui/
utils/
workflows/
uploads/
audio/
metadata/
transcripts/
analysis/
chat_history/
reports/
exports/
tests/
docs/
```

---

# Supported AI Providers

- Ollama
- OpenAI
- Anthropic

---

# Supported Export Formats

- PDF
- HTML
- Markdown
- TXT
- JSON

---

# Technology Stack

- Python
- Streamlit
- Whisper
- Ollama
- OpenAI
- Anthropic
- OpenCV
- MoviePy
- FFmpeg
- ReportLab

---

# Testing

```
Framework : Pytest
Status    : 531 Passed
Failures  : 0
```

Run tests

```bash
pytest
```

---

# Documentation

Additional project documentation is available in the `docs/` directory.

- API_DOCUMENTATION.md
- ARCHITECTURE.md
- CONFIGURATION.md
- CONTRIBUTING.md
- CHANGELOG.md
- RELEASE_NOTES.md
- ROADMAP.md
- SECURITY.md
- USER_GUIDE.md
- TESTING.md

---

# Summary

AI Video Analysis Agent provides an end-to-end workflow for analyzing videos with AI. Its modular architecture, agent-based workflow, provider abstraction, and comprehensive testing make it suitable for learning, development, and real-world AI-powered video analysis applications.