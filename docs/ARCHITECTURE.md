# System Architecture

![Architecture](https://img.shields.io/badge/Architecture-Agent%20Based-blueviolet)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Stable-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)

> AI Video Analysis Agent follows a modular **Agent → Service → Provider** architecture. Each component has a single responsibility, making the application scalable, maintainable, and easy to extend.

---

# Architecture Overview

```
                    User
                      │
                      ▼
             Streamlit Frontend
                 (app_agent.py)
                      │
                      ▼
              Workflow Controller
                      │
                      ▼
       ┌─────────────────────────────┐
       │         AI Agents           │
       └─────────────────────────────┘
                      │
                      ▼
       ┌─────────────────────────────┐
       │      Business Services      │
       └─────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     AI Providers           Local Storage
```

---

# Application Layers

## Presentation Layer

Responsible for user interaction.

```
app_agent.py

UI Pages

Sidebar

Forms

Progress Bars

Status Messages
```

---

## Workflow Layer

Coordinates the execution flow between agents.

```
Workflow Context

Workflow Manager

Context Updates

Execution Order
```

---

## Agent Layer

Each agent performs a single workflow task.

```
UploadAgent

MetadataAgent

AudioAgent

TranscriptAgent

AnalysisAgent

ChatAgent

ReportAgent

ExportAgent
```

---

## Service Layer

Contains business logic.

```
VideoService

MetadataService

AudioService

SpeechService

AIAnalysisService

AIChatService

ReportService

ExportService
```

---

## Provider Layer

Provides AI model abstraction.

```
ProviderFactory

OllamaProvider

OpenAIProvider

AnthropicProvider
```

---

## Storage Layer

Stores generated files.

```
Uploads

Audio

Metadata

Transcripts

Analysis

Chat History

Reports

Exports
```

---

# Complete Workflow

```
Upload Video
      │
      ▼
Video Validation
      │
      ▼
Duplicate Detection
      │
      ▼
Save Video
      │
      ▼
Extract Metadata
      │
      ▼
Extract Audio
      │
      ▼
Generate Transcript
      │
      ▼
AI Analysis
      │
      ▼
AI Chat
      │
      ▼
Generate Report
      │
      ▼
Export Report
```

---

# Component Interaction

```
UI
 │
 ▼
Agent
 │
 ▼
Service
 │
 ▼
Provider
 │
 ▼
Model
 │
 ▼
Response
 │
 ▼
Storage
 │
 ▼
UI
```

---

# Folder Structure

```
AI-Video-Analysis-Agent/

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

# Data Flow

```
Video
 │
 ▼
Metadata
 │
 ▼
Audio
 │
 ▼
Transcript
 │
 ▼
AI Analysis
 │
 ▼
Chat
 │
 ▼
Report
 │
 ▼
Export
```

---

# Design Principles

- Modular Architecture
- Agent-Based Design
- Separation of Concerns
- Service-Oriented Logic
- Provider Abstraction
- Reusable Components
- Workflow Context Sharing
- JSON-Based Storage
- Easy Extensibility
- Maintainable Codebase

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

---

# Future Scalability

The architecture is designed to support:

- Additional AI providers
- New analysis agents
- Cloud storage integration
- Database backends
- REST API support
- Authentication
- Multi-user support
- Plugin architecture

---

# Summary

The AI Video Analysis Agent uses a clean layered architecture with **Agent → Service → Provider** separation. Business logic is isolated within services, workflow orchestration is handled by agents, AI interactions are abstracted through providers, and all generated artifacts are stored locally in an organized directory structure. This design enables scalability, maintainability, and straightforward extension for future features.