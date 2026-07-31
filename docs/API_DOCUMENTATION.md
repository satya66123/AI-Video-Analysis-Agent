# 🔌 AI Video Analyzer - API Documentation

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/Streamlit-1.46+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

<img src="https://img.shields.io/badge/Ollama-Supported-black?style=for-the-badge"/>

<img src="https://img.shields.io/badge/OpenAI-Supported-10A37F?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Anthropic-Supported-5A4FCF?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge"/>

</p>

---

# Table of Contents

- Introduction
- Architecture
- Providers
- Services
- Utilities
- Components
- Configuration
- Data Flow
- Error Handling
- Developer Notes

---

# Introduction

This document describes the internal API used throughout **AI Video Analyzer**.

Unlike a REST API, the project uses a modular Python architecture where services communicate through reusable classes and provider interfaces.

---

# Internal Architecture

```
app.py
   │
   ▼
Pages
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
AI Models
```

---

# Provider API

Every provider follows the same interface.

```python
provider.generate(
    model=model_name,
    prompt=prompt
)
```

---

## Supported Providers

| Provider | Purpose |
|-----------|----------|
| Ollama | Local AI Models |
| OpenAI | Cloud LLM |
| Anthropic | Claude Models |

---

## Base Provider

Responsible for defining the common interface.

Example

```python
class BaseProvider:

    def generate(self, model, prompt):
        pass
```

---

## Ollama Provider

Responsibilities

- Connect to Ollama
- List models
- Generate responses
- Handle errors

---

## OpenAI Provider

Responsibilities

- API communication
- Authentication
- Completion generation
- Exception handling

---

## Anthropic Provider

Responsibilities

- Claude API integration
- Prompt execution
- Response parsing

---

# Service Layer

Business logic is implemented inside services.

---

## VideoService

Responsibilities

- Save uploads
- Validate files
- Read metadata

Typical methods

```
save_video()

validate_video()

get_metadata()
```

---

## AudioService

Responsibilities

- Audio extraction
- Audio conversion
- Audio validation

Methods

```
extract_audio()

get_audio_info()
```

---

## SpeechService

Responsibilities

- Whisper loading
- Speech recognition
- Transcript generation

Methods

```
load_model()

transcribe()

save_transcript()
```

---

## AIAnalysisService

Responsibilities

- Prompt preparation
- Provider selection
- AI communication
- Result formatting

Methods

```
generate_summary()

generate_keywords()

generate_topics()

generate_analysis()
```

---

## ExportService

Responsibilities

Generate

- TXT
- Markdown
- HTML
- PDF

Methods

```
export_txt()

export_md()

export_html()

export_pdf()
```

---

## MetadataService

Responsibilities

- Read metadata
- Format metadata
- Display metadata

---

# Utility Modules

Utility modules provide reusable helper functions.

Examples

```
FileValidator

TranscriptUtils

AudioUtils

ExportUtils

Logger

ConfigManager
```

---

# Components

Reusable Streamlit UI components.

Examples

```
Sidebar

Header

Footer

TranscriptViewer

ChatComponent

ExportPanel

MetadataViewer
```

---

# Configuration

Configuration is centralized.

Examples

```
APP_NAME

VERSION

SUPPORTED_FORMATS

MAX_FILE_SIZE

UPLOAD_DIRECTORY

EXPORT_DIRECTORY
```

---

# Data Flow

```
Video

↓

Validation

↓

Audio Extraction

↓

Speech Recognition

↓

Transcript

↓

AI Analysis

↓

Reports

↓

Export
```

---

# Exception Handling

The application should gracefully handle:

- Invalid file types

- Unsupported video formats

- AI provider errors

- Missing API keys

- Missing models

- Network failures

- Export failures

---

# Logging

Recommended logging includes

```
INFO

WARNING

ERROR

DEBUG
```

Store logs for troubleshooting and debugging during development.

---

# Extension Guide

Adding a new AI provider:

1. Create provider class.

2. Inherit BaseProvider.

3. Implement generate().

4. Register in ProviderFactory.

5. Add tests.

---

# Best Practices

✔ Keep business logic inside services.

✔ Keep providers lightweight.

✔ Write unit tests for new modules.

✔ Reuse utility functions.

✔ Avoid duplicated logic.

✔ Handle exceptions consistently.

---

# Future API Enhancements

Potential additions include:

- REST API

- FastAPI integration

- Authentication

- JWT Support

- WebSocket Streaming

- Plugin API

- Batch Processing API

- Cloud Deployment

---

# Related Documentation

- INSTALLATION.md

- FEATURES.md

- PROJECT_STRUCTURE.md

- ARCHITECTURE.md

- SYSTEM_DESIGN.md

- PROVIDER_GUIDE.md

- TESTING.md

- README.md

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub Repository

https://github.com/satya66123/AI-Video-Analyzer

---

**Version:** v1.0.0

**License:** MIT

⭐ Contributions, feature requests, and feedback are always welcome.