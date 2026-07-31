# 🏛 AI Video Analyzer - Software Architecture

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
- Architecture Overview
- Design Principles
- System Layers
- Request Flow
- AI Processing Pipeline
- Provider Architecture
- Export Architecture
- Testing Architecture
- Advantages
- Future Enhancements

---

# 🎯 Introduction

AI Video Analyzer is designed using a modular, layered architecture that separates presentation, business logic, AI provider communication, and data processing. This approach improves maintainability, scalability, and testability while allowing new features and AI providers to be added with minimal changes.

---

# 🏗 Architecture Overview

```text
                   +----------------------+
                   |     Streamlit UI     |
                   +----------+-----------+
                              |
                              ▼
                   +----------------------+
                   |      Components      |
                   +----------+-----------+
                              |
                              ▼
                   +----------------------+
                   |       Services       |
                   +----------+-----------+
                              |
                              ▼
                   +----------------------+
                   |      Providers       |
                   +----------+-----------+
                              |
                              ▼
                   +----------------------+
                   |     AI Models/API    |
                   +----------------------+
```

---

# 🏛 Design Principles

The architecture follows these software engineering principles:

- Single Responsibility Principle (SRP)
- Separation of Concerns (SoC)
- Modular Design
- Reusable Components
- Provider Abstraction
- Dependency Isolation
- Maintainable Codebase
- Test-Driven Development Support

---

# 📚 System Layers

## 1. Presentation Layer

Responsible for the user interface.

Examples:

- Streamlit Pages
- Sidebar
- Navigation
- Forms
- Buttons
- Progress Bars
- Data Tables

---

## 2. Component Layer

Reusable UI modules.

Examples:

- Header
- Footer
- Video Player
- Transcript Viewer
- Metadata Viewer
- Export Panel
- Chat Interface

---

## 3. Service Layer

Contains the application's business logic.

Major services include:

- VideoService
- AudioService
- SpeechService
- AIAnalysisService
- ExportService
- MetadataService
- ChatHistoryService

Responsibilities:

- Coordinate workflows
- Process files
- Validate data
- Handle errors
- Communicate with providers

---

## 4. Provider Layer

Acts as an abstraction between the application and AI providers.

Supported Providers:

- Ollama
- OpenAI
- Anthropic

Advantages:

- Easy provider switching
- Shared interface
- Reduced duplicate code
- Easier testing

---

## 5. Data Layer

Stores generated project files.

Folders include:

- uploads/
- audio/
- transcripts/
- analysis/
- reports/
- exports/
- chat_history/

---

# 🔄 Request Flow

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
Components
 │
 ▼
Services
 │
 ▼
Providers
 │
 ▼
AI Model
 │
 ▼
Response
 │
 ▼
Services
 │
 ▼
UI Display
```

---

# 🤖 AI Processing Pipeline

```text
Video Upload
      │
      ▼
Validation
      │
      ▼
Audio Extraction
      │
      ▼
Speech Recognition
      │
      ▼
Transcript Storage
      │
      ▼
Prompt Generation
      │
      ▼
AI Provider
      │
      ▼
Analysis Output
      │
      ▼
Export
```

---

# 🔌 Provider Architecture

```text
BaseProvider
     │
     ├───────────────┐
     │               │
     ▼               ▼
OllamaProvider   OpenAIProvider
                     │
                     ▼
             AnthropicProvider
```

Every provider implements a common interface, allowing the application to switch providers without modifying the service layer.

---

# 📤 Export Architecture

Supported export formats:

- TXT
- Markdown
- HTML
- PDF

Workflow:

```text
Analysis
    │
    ▼
Export Service
    │
    ├── TXT
    ├── MD
    ├── HTML
    └── PDF
```

---

# 🧪 Testing Architecture

Testing is organized around application modules.

```text
tests/
│
├── test_components.py
├── test_services.py
├── test_providers.py
├── test_utils.py
├── test_config.py
└── ...
```

The project uses:

- Pytest
- Fixtures
- Mock Objects
- GitHub Actions
- Continuous Integration

---

# ✅ Benefits of This Architecture

| Benefit | Description |
|----------|-------------|
| Modular | Easy to extend |
| Scalable | Supports future growth |
| Maintainable | Clear separation of concerns |
| Testable | High unit test coverage |
| Flexible | Multiple AI providers |
| Reusable | Shared components and services |
| Reliable | CI/CD validation |

---

# 🚀 Future Enhancements

The architecture is designed to accommodate future features such as:

- Plugin System
- Cloud Storage Integration
- Batch Video Processing
- OCR Pipeline
- Speaker Diarization
- Subtitle Generation
- Multi-language Translation
- REST API
- Authentication & User Management

---

# 📚 Related Documentation

- 01_INSTALLATION.md
- 02_FEATURES.md
- 03_PROJECT_STRUCTURE.md
- 05_SYSTEM_DESIGN.md
- 09_TESTING.md
- README.md

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub Repository

https://github.com/satya66123/AI-Video-Analyzer

---

**Version:** v1.0.0

⭐ If you find this project useful, consider giving it a GitHub Star and contributing through Issues or Pull Requests.