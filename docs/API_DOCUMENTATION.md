# API Documentation

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-531%20Passed-success)
![Pytest](https://img.shields.io/badge/Pytest-Passing-success?logo=pytest)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

> AI Video Analysis Agent API Documentation

---

# Application

**Entry Point**

```bash
streamlit run app_agent.py
```

---

# Application Flow

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

# Agents

| Agent | Responsibility |
|--------|----------------|
| UploadAgent | Upload and validate videos |
| MetadataAgent | Extract video/audio metadata |
| AudioAgent | Extract audio from video |
| TranscriptAgent | Generate transcript using Whisper |
| AnalysisAgent | Perform AI analysis |
| ChatAgent | Chat with transcript |
| ReportAgent | Generate analysis report |
| ExportAgent | Export reports |

---

# Services

| Service | Responsibility |
|----------|----------------|
| VideoService | Video upload, duplicate detection, hashing |
| MetadataService | Video and audio metadata |
| AudioService | Audio extraction and metadata |
| SpeechService | Whisper transcription |
| AIAnalysisService | AI analysis generation |
| AIChatService | AI chat management |
| ReportService | Report generation |
| ExportService | Export reports |

---

# Providers

| Provider | Purpose |
|----------|---------|
| OllamaProvider | Local LLM support |
| OpenAIProvider | OpenAI models |
| AnthropicProvider | Claude models |
| ProviderFactory | Returns configured provider |

---

# Utilities

- AudioSplitter
- FileValidator
- ModelManager
- ThemeManager
- Helper Functions

---

# Workflow Context

Common context values

```
uploaded_file
video
video_metadata
audio
audio_metadata
transcript
transcript_metadata
analysis
analysis_metadata
chat_history
report
exports
provider_name
model_name
status
```

---

# Storage Structure

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

# Supported Formats

### Video

- MP4
- AVI
- MOV
- MKV
- WEBM

### Audio

- MP3
- WAV

### Export

- PDF
- HTML
- Markdown
- TXT
- JSON

---

# Main Modules

```
app_agent.py
agents/
services/
providers/
ui/
utils/
workflows/
tests/
```

---

# Error Handling

The application handles:

- Invalid uploads
- Missing files
- Empty transcripts
- Provider errors
- Export failures
- File system exceptions

---

# Testing

```
Framework : Pytest
Status    : 531 Passed
Failures  : 0
```

Run tests:

```bash
pytest
```

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
- ReportLab
- FFmpeg

---

# GitHub

Repository

```
https://github.com/satya66123/AI-Video-Analysis-Agent
```

Issues

```
https://github.com/satya66123/AI-Video-Analysis-Agent/issues
```

Pull Requests

```
https://github.com/satya66123/AI-Video-Analysis-Agent/pulls
```

Releases

```
https://github.com/satya66123/AI-Video-Analysis-Agent/releases
```

---

© 2026 AI Video Analysis Agent