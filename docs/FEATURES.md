# ✨ AI Video Analyzer - Features

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/Streamlit-1.46+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

<img src="https://img.shields.io/badge/Ollama-Supported-black?style=for-the-badge"/>

<img src="https://img.shields.io/badge/OpenAI-Supported-10A37F?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Anthropic-Supported-5A4FCF?style=for-the-badge"/>

<img src="https://github.com/satya66123/AI-Video-Analyzer/actions/workflows/python-tests.yml/badge.svg"/>

<img src="https://img.shields.io/badge/Pytest-Passing-success?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge"/>

</p>

---

# 📖 Table of Contents

- Overview
- Core Features
- Video Processing
- Audio Processing
- Speech Recognition
- AI Analysis
- AI Chat
- Reports
- Export Formats
- AI Providers
- User Interface
- Testing
- Upcoming Features

---

# 🎯 Overview

AI Video Analyzer is an AI-powered application that transforms video content into structured, searchable, and actionable information.

The application combines audio extraction, speech recognition, transcript generation, AI analysis, and report exporting into a unified workflow.

---

# 🚀 Core Features

| Category | Description | Status |
|----------|-------------|--------|
| Video Upload | Upload local videos | ✅ |
| Audio Extraction | Extract audio from videos | ✅ |
| Speech Recognition | Whisper transcription | ✅ |
| Transcript Viewer | Read generated transcripts | ✅ |
| AI Analysis | Intelligent content analysis | ✅ |
| AI Chat | Chat with transcripts | ✅ |
| Reports | Generate structured reports | ✅ |
| Export | TXT, Markdown, HTML, PDF | ✅ |
| Testing | Automated Pytest suite | ✅ |
| GitHub Actions | Continuous Integration | ✅ |

---

# 🎥 Video Processing

## Supported Formats

| Format | Supported |
|---------|-----------|
| MP4 | ✅ |
| AVI | ✅ |
| MOV | ✅ |
| MKV | ✅ |
| WEBM | ✅ |

### Features

- Upload videos
- Video validation
- Video metadata extraction
- Duration calculation
- Resolution detection
- FPS detection
- File size display

---

# 🎵 Audio Processing

The application automatically extracts audio from uploaded videos.

### Features

- Audio extraction
- Audio playback
- Audio metadata
- Audio duration
- Audio splitting
- Temporary audio management

Supported audio workflow

```text
Video
   │
   ▼
Audio Extraction
   │
   ▼
Speech Recognition
```

---

# 📝 Speech Recognition

Powered by **OpenAI Whisper**.

### Features

- Speech-to-Text
- Transcript generation
- UTF-8 transcript storage
- Transcript viewer
- Transcript management

Workflow

```text
Audio
   │
   ▼
Whisper
   │
   ▼
Transcript
```

---

# 🤖 AI Analysis

The application can generate multiple AI-powered analyses from transcripts.

| Analysis | Status |
|-----------|--------|
| Summary | ✅ |
| Key Points | ✅ |
| Keywords | ✅ |
| Topics | ✅ |
| Action Items | ✅ |
| Meeting Notes | ✅ |
| Study Notes | ✅ |
| Sentiment Analysis | ✅ |

Workflow

```text
Transcript
     │
     ▼
Prompt
     │
     ▼
AI Provider
     │
     ▼
Generated Analysis
```

---

# 💬 AI Chat

Interact with the transcript using natural language.

### Features

- Context-aware conversations
- Chat history
- Conversation export
- Chat title generation
- Multiple AI providers

Example

```
User:
Summarize the first half of the transcript.

↓

Assistant:
Provides an AI-generated summary.
```

---

# 📊 Reports

Generate professional reports including:

- Transcript Report
- Metadata Report
- AI Analysis Report
- Chat History Report

---

# 📄 Export Formats

Supported export formats.

| Format | Supported |
|----------|-----------|
| TXT | ✅ |
| Markdown | ✅ |
| HTML | ✅ |
| PDF | ✅ |

---

# 🤖 Supported AI Providers

| Provider | Status |
|-----------|--------|
| Ollama | ✅ |
| OpenAI | ✅ |
| Anthropic | ✅ |

---

## Ollama Models

Examples

- Llama 3
- Llama 3.1
- Gemma
- Gemma 2
- Gemma 3
- Phi-3
- Mistral
- Qwen
- DeepSeek

---

# 🎨 User Interface

Developed using **Streamlit**.

### UI Features

- Sidebar Navigation
- Multi-page Layout
- Progress Indicators
- Status Messages
- Responsive Components
- Theme-friendly Design

---

# 🧪 Testing

Testing infrastructure includes:

- Pytest
- Mocking
- Fixtures
- GitHub Actions
- Automated Validation

Current Coverage

- Components
- Services
- Providers
- Utilities
- Configuration
- Prompt Templates

---

# 🔮 Upcoming Features

Planned improvements

- Speaker Identification
- Timestamped Highlights
- OCR Support
- Subtitle Generation
- Multi-language Translation
- Batch Video Processing
- Cloud Storage Integration
- YouTube Video Support
- RAG-based Transcript Search

---

# 📷 Screenshots

> Add screenshots for the following pages:

- Dashboard
- Video Upload
- Transcript Viewer
- AI Analysis
- AI Chat
- Reports
- Export Center

---

# 📚 Related Documentation

- 01_INSTALLATION.md
- 03_PROJECT_STRUCTURE.md
- 04_ARCHITECTURE.md
- 05_SYSTEM_DESIGN.md
- 09_TESTING.md
- README.md

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub Repository

https://github.com/satya66123/AI-Video-Analyzer

---

⭐ If you enjoy this project, consider giving it a GitHub Star.