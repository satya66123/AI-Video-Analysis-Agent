# 🏗️ AI Video Analyzer - Project Structure

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

- Introduction
- Project Layout
- Directory Structure
- Folder Description
- Architecture Layers
- Data Flow
- Development Guidelines
- Related Documentation

---

# 🎯 Introduction

AI Video Analyzer follows a modular architecture designed for scalability, maintainability, and ease of testing.

Each module has a single responsibility, making it easier to develop, test, and extend.

---

# 📂 Project Layout

```
AI-Video-Analyzer/
│
├── .github/
│   └── workflows/
│
├── analysis/
├── assets/
├── audio/
├── chat_history/
├── components/
├── config/
├── docs/
├── exports/
├── pages/
├── prompts/
├── providers/
├── reports/
├── services/
├── tests/
├── transcripts/
├── uploads/
├── utils/
│
├── app.py
├── requirements.txt
├── requirements_test.txt
├── pytest.ini
├── LICENSE
└── README.md
```

---

# 📁 Directory Overview

| Folder | Purpose |
|----------|----------|
| analysis | Stores AI-generated analysis files |
| assets | Images, logos, icons and screenshots |
| audio | Extracted audio files |
| chat_history | AI chat history |
| components | Reusable Streamlit components |
| config | Application configuration |
| docs | Project documentation |
| exports | Exported TXT, HTML, PDF, Markdown files |
| pages | Streamlit pages |
| prompts | AI prompt templates |
| providers | AI provider implementations |
| reports | Generated reports |
| services | Business logic |
| tests | Pytest test suite |
| transcripts | Generated transcripts |
| uploads | Uploaded videos |
| utils | Utility/helper functions |

---

# 🏛 Layered Architecture

```
Presentation Layer
        │
        ▼
Component Layer
        │
        ▼
Service Layer
        │
        ▼
Provider Layer
        │
        ▼
External AI Models
```

---

# 🧩 Folder Responsibilities

## components/

Contains reusable Streamlit UI components.

Examples:

- Header
- Footer
- Sidebar
- AI Chat
- Metadata Viewer
- Transcript Viewer
- Export Panel

---

## pages/

Contains individual application pages.

Examples:

- Dashboard
- Upload Video
- Speech to Text
- AI Analysis
- Reports
- Settings

---

## services/

Implements the business logic.

Examples:

- AudioService
- SpeechService
- AIAnalysisService
- ExportService
- MetadataService
- VideoService

---

## providers/

Implements AI provider integrations.

Supported providers:

- Ollama
- OpenAI
- Anthropic

---

## prompts/

Stores reusable prompt templates.

Examples:

- Summary Prompt
- Keywords Prompt
- Topics Prompt
- Sentiment Prompt
- Meeting Notes Prompt
- Study Notes Prompt

---

## utils/

Contains shared utility modules.

Examples:

- Audio Splitter
- File Validator
- Transcript Utilities
- Metadata Helpers

---

## tests/

Contains automated Pytest test cases.

Coverage includes:

- Components
- Services
- Providers
- Utilities
- Configuration
- Prompt Templates

---

# 🔄 Data Flow

```
Upload Video
      │
      ▼
Video Validation
      │
      ▼
Audio Extraction
      │
      ▼
Speech Recognition
      │
      ▼
Transcript Generation
      │
      ▼
AI Analysis
      │
      ▼
Reports
      │
      ▼
Export
```

---

# 💼 Development Guidelines

✔ Keep UI code inside `components/`

✔ Keep business logic inside `services/`

✔ Keep AI communication inside `providers/`

✔ Keep prompts inside `prompts/`

✔ Keep helper functions inside `utils/`

✔ Add corresponding tests inside `tests/`

---

# 📊 Module Relationship

```
pages
 │
 ▼
components
 │
 ▼
services
 │
 ▼
providers
 │
 ▼
AI Models
```

---

# 📚 Related Documentation

- 01_INSTALLATION.md
- 02_FEATURES.md
- 04_ARCHITECTURE.md
- 05_SYSTEM_DESIGN.md
- 09_TESTING.md

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub Repository

https://github.com/satya66123/AI-Video-Analyzer

---

**AI Video Analyzer v1.0.0**

⭐ Star the repository if you found it useful.