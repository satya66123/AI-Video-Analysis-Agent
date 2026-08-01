# Project Structure

![Structure](https://img.shields.io/badge/Project-Structure-blue)
![Architecture](https://img.shields.io/badge/Architecture-Agent--Service--Provider-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)

This document describes the directory structure of the AI Video Analysis Agent project.

---

# Root Directory

```
AI-Video-Analysis-Agent/
│
├── app_agent.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── agents/
├── services/
├── providers/
├── workflows/
├── ui/
├── utils/
├── tests/
├── docs/
│
├── uploads/
├── audio/
├── metadata/
├── transcripts/
├── analysis/
├── chat_history/
├── reports/
├── exports/
│
└── assets/
```

---

# Folder Description

## app_agent.py

Main entry point of the application.

Responsible for:

- Streamlit initialization
- Navigation
- Workflow execution
- UI rendering

---

## agents/

Contains workflow agents.

Example:

```
agents/

base_agent.py
upload_agent.py
metadata_agent.py
audio_agent.py
transcript_agent.py
analysis_agent.py
chat_agent.py
report_agent.py
export_agent.py
```

Responsibilities

- Execute workflow
- Update workflow context
- Call services

---

## services/

Contains business logic.

Example

```
services/

video_agent_service.py
metadata_agent_service.py
audio_agent_service.py
speech_agent_service.py
ai_analysis_agent_service.py
ai_chat_agent_service.py
report_agent_service.py
export_agent_service.py
```

Responsibilities

- Business logic
- File operations
- AI integration
- Report generation

---

## providers/

Contains AI provider implementations.

Example

```
providers/

base_provider.py
provider_factory.py
ollama_provider.py
openai_provider.py
anthropic_provider.py
```

Responsibilities

- AI provider abstraction
- Model communication
- Response generation

---

## workflows/

Contains workflow execution logic.

Example

```
workflows/

workflow_context.py
workflow_manager.py
```

Responsibilities

- Execute agents
- Share workflow context
- Manage execution flow

---

## ui/

Contains Streamlit user interface pages.

Example

```
ui/

upload_page_agent.py
metadata_page_agent.py
audio_page_agent.py
transcript_page_agent.py
analysis_page_agent.py
chat_page_agent.py
report_page_agent.py
history_page_agent.py
settings_page_agent.py
```

Responsibilities

- User interface
- Forms
- Navigation
- Progress display

---

## utils/

Utility modules.

Example

```
utils/

audio_splitter.py
file_validator.py
metadata_utils.py
report_utils.py
```

Responsibilities

- Helper functions
- Validation
- Common utilities

---

## uploads/

Stores uploaded videos.

Example

```
uploads/

video1.mp4
meeting.mov
demo.mkv
```

---

## audio/

Stores extracted audio files.

Example

```
audio/

video1.wav
meeting.wav
```

---

## metadata/

Stores metadata files.

Example

```
metadata/

video1.json
meeting.json
```

---

## transcripts/

Stores generated transcripts.

Example

```
transcripts/

video1.txt
meeting.txt
```

---

## analysis/

Stores AI-generated analysis.

Example

```
analysis/

video_summary.md
meeting_analysis.md
```

---

## chat_history/

Stores AI chat conversations.

Example

```
chat_history/

video_chat.json
meeting_chat.json
```

---

## reports/

Stores generated reports.

Example

```
reports/

video_report.md
meeting_report.md
```

---

## exports/

Stores exported reports.

Example

```
exports/

pdf/
html/
markdown/
txt/
json/
```

---

## tests/

Contains automated tests.

Example

```
tests/

test_upload_agent.py
test_metadata_agent.py
test_audio_agent.py
test_transcript_agent.py
test_analysis_agent.py
test_chat_agent.py
test_report_agent.py
test_export_agent.py

test_video_agent_service.py
test_metadata_agent_service.py
test_audio_agent_service.py
test_speech_agent_service.py
test_ai_analysis_agent_service.py
test_ai_chat_agent_service.py
test_report_agent_service.py
test_export_agent_service.py
```

Responsibilities

- Unit Tests
- Integration Tests
- Service Tests
- Agent Tests

---

## docs/

Project documentation.

Example

```
docs/

API_DOCUMENTATION.md
ARCHITECTURE.md
CHANGELOG.md
CODE_OF_CONDUCT.md
CONFIGURATION.md
CONTRIBUTING.md
DOCUMENTATION.md
EXPORT_GUIDE.md
FAQ.md
FEATURES.md
IMPLEMENTATION_STEPS.md
INSTALLATION.md
INTERVIEW_ANSWERS.md
INTERVIEW_QUESTIONS.md
PROJECT_NOTES.md
PROJECT_PLANNER.md
PROJECT_STRUCTURE.md
ROADMAP.md
SECURITY.md
TESTING.md
USER_GUIDE.md
```

---

## assets/

Project assets.

Example

```
assets/

logo.png
banner.png
screenshots/
icons/
```

---

# Architecture Overview

```
User
   │
   ▼
Streamlit UI
   │
   ▼
Workflow
   │
   ▼
Agents
   │
   ▼
Services
   │
   ▼
Providers
   │
   ▼
Local Storage
```

---

# Summary

The AI Video Analysis Agent follows a clean and modular directory structure based on the **Agent → Service → Provider** architecture. Responsibilities are clearly separated across folders, making the project easy to understand, maintain, test, and extend with new features.