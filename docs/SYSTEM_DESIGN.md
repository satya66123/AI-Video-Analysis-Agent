# System Design

![System Design](https://img.shields.io/badge/System-Design-blue)
![Architecture](https://img.shields.io/badge/Architecture-Agent--Service--Provider-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)

---

# Overview

AI Video Analysis Agent is a modular Streamlit application designed to automate the complete video analysis workflow. The system follows an **Agent → Service → Provider** architecture, separating workflow execution, business logic, and AI provider integration.

---

# High-Level Architecture

```
                   User
                     │
                     ▼
             Streamlit Interface
                     │
                     ▼
              Workflow Manager
                     │
                     ▼
     ┌────────────────────────────────┐
     │            Agents              │
     └────────────────────────────────┘
                     │
                     ▼
     ┌────────────────────────────────┐
     │           Services             │
     └────────────────────────────────┘
                     │
                     ▼
     ┌────────────────────────────────┐
     │        Provider Factory        │
     └────────────────────────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Ollama      OpenAI    Anthropic
                     │
                     ▼
              Local File Storage
```

---

# System Workflow

```
Upload Video
      │
      ▼
Video Validation
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
Export Reports
```

---

# Layered Architecture

## Presentation Layer

Responsible for:

- Streamlit UI
- User interaction
- Navigation
- Progress display
- History pages

Folder:

```
ui/
```

---

## Workflow Layer

Responsible for:

- Agent execution
- Workflow sequencing
- Context management

Folder:

```
workflows/
```

---

## Agent Layer

Agents coordinate the workflow by invoking services and updating the workflow context.

Implemented agents:

- UploadAgent
- MetadataAgent
- AudioAgent
- TranscriptAgent
- AnalysisAgent
- ChatAgent
- ReportAgent
- ExportAgent

Folder:

```
agents/
```

---

## Service Layer

Contains the application's business logic.

Implemented services:

- VideoService
- MetadataService
- AudioService
- SpeechService
- AIAnalysisService
- AIChatService
- ReportService
- ExportService

Folder:

```
services/
```

---

## Provider Layer

Provides a common interface for AI providers.

Supported providers:

- Ollama
- OpenAI
- Anthropic

Components:

```
BaseProvider

↓

ProviderFactory

↓

Provider Implementation
```

Folder:

```
providers/
```

---

## Utility Layer

Contains reusable helper modules.

Examples:

- Audio Splitter
- File Validator
- Metadata Utilities
- Report Utilities

Folder:

```
utils/
```

---

# Workflow Context

The application uses a shared workflow context to exchange data between agents.

Example:

```
{
    video,
    video_metadata,
    audio,
    audio_metadata,
    transcript,
    transcript_metadata,
    analysis,
    report,
    exports,
    chat_history,
    status
}
```

---

# Data Flow

```
Video Upload
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

# Storage Design

The application uses local folder-based storage.

```
uploads/
audio/
metadata/
transcripts/
analysis/
chat_history/
reports/
exports/
```

---

# AI Processing

The AI pipeline performs:

1. Load transcript
2. Generate prompt
3. Select provider
4. Generate AI response
5. Store analysis
6. Generate report

---

# Report Pipeline

```
Video Metadata
        │
Audio Metadata
        │
Transcript
        │
AI Analysis
        │
Chat History
        │
        ▼
Complete Report
        │
        ▼
Export Module
```

---

# Export Pipeline

Supported formats:

- PDF
- HTML
- Markdown
- TXT
- JSON

```
Report
   │
   ▼
Export Service
   │
   ▼
Generate Files
   │
   ▼
exports/
```

---

# Error Handling

The system validates:

- Uploaded files
- Duplicate uploads
- Missing transcripts
- AI provider availability
- Export operations
- File operations

Errors are handled within the appropriate service and propagated to the workflow when necessary.

---

# Design Principles

The system is built using:

- Modular Design
- Separation of Concerns
- Single Responsibility Principle
- Reusability
- Extensibility
- Maintainability

---

# Advantages

- Modular architecture
- Easy maintenance
- Easy testing
- Multiple AI provider support
- Reusable services
- Scalable workflow
- Simple local storage
- Clear separation of responsibilities

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Frontend | Streamlit |
| Language | Python |
| Speech Recognition | Whisper |
| AI Providers | Ollama, OpenAI, Anthropic |
| Audio Processing | FFmpeg |
| Reporting | ReportLab |
| Testing | Pytest |
| Storage | Local Files & JSON |

---

# Summary

The AI Video Analysis Agent uses a clean **Agent → Service → Provider** architecture to separate workflow management, business logic, and AI integration. This layered design makes the application modular, maintainable, testable, and easy to extend with new AI providers, workflow agents, services, and export formats while supporting an end-to-end AI-powered video analysis pipeline.