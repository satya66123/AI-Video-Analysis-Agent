# Workflow Guide

![Workflow](https://img.shields.io/badge/Workflow-Guide-blue)
![Architecture](https://img.shields.io/badge/Architecture-Agent--Service--Provider-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)

---

# Overview

The AI Video Analysis Agent follows a sequential workflow where each stage processes data and passes the results to the next stage. The workflow is coordinated through a shared workflow context using the **Agent → Service → Provider** architecture.

---

# Complete Workflow

```
                User
                  │
                  ▼
          Upload Video
                  │
                  ▼
        UploadAgent
                  │
                  ▼
        VideoService
                  │
                  ▼
      Video Saved Successfully
                  │
                  ▼
      MetadataAgent
                  │
                  ▼
     MetadataService
                  │
                  ▼
      Video Metadata
                  │
                  ▼
       AudioAgent
                  │
                  ▼
       AudioService
                  │
                  ▼
      Audio Extracted
                  │
                  ▼
     TranscriptAgent
                  │
                  ▼
      SpeechService
                  │
                  ▼
     Whisper Transcript
                  │
                  ▼
      AnalysisAgent
                  │
                  ▼
    AIAnalysisService
                  │
                  ▼
 Provider Factory
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
   Ollama      OpenAI    Anthropic
                  │
                  ▼
        AI Analysis
                  │
                  ▼
        ChatAgent
                  │
                  ▼
      AIChatService
                  │
                  ▼
        AI Conversation
                  │
                  ▼
       ReportAgent
                  │
                  ▼
      ReportService
                  │
                  ▼
     Complete Report
                  │
                  ▼
       ExportAgent
                  │
                  ▼
      ExportService
                  │
                  ▼
    PDF / HTML / MD / TXT / JSON
```

---

# Step 1 — Video Upload

**Agent**

```
UploadAgent
```

**Service**

```
VideoService
```

Responsibilities:

- Validate video
- Detect duplicates
- Save uploaded file
- Generate upload metadata

Output:

```
uploads/
```

---

# Step 2 — Metadata Extraction

**Agent**

```
MetadataAgent
```

**Service**

```
MetadataService
```

Responsibilities:

- Read video information
- Generate metadata
- Store metadata

Output:

```
metadata/
```

---

# Step 3 — Audio Extraction

**Agent**

```
AudioAgent
```

**Service**

```
AudioService
```

Responsibilities:

- Extract audio
- Save WAV file
- Generate audio metadata

Output:

```
audio/
```

---

# Step 4 — Speech Recognition

**Agent**

```
TranscriptAgent
```

**Service**

```
SpeechService
```

Responsibilities:

- Load Whisper
- Split long audio
- Generate transcript
- Save transcript

Output:

```
transcripts/
```

---

# Step 5 — AI Analysis

**Agent**

```
AnalysisAgent
```

**Service**

```
AIAnalysisService
```

Responsibilities:

- Load transcript
- Build prompt
- Select AI provider
- Generate analysis
- Save analysis

Output:

```
analysis/
```

---

# Step 6 — AI Chat

**Agent**

```
ChatAgent
```

**Service**

```
AIChatService
```

Responsibilities:

- Ask questions
- Build conversation context
- Generate AI responses
- Save chat history

Output:

```
chat_history/
```

---

# Step 7 — Report Generation

**Agent**

```
ReportAgent
```

**Service**

```
ReportService
```

Responsibilities:

- Combine project data
- Generate report
- Create report metadata

Output:

```
reports/
```

---

# Step 8 — Export

**Agent**

```
ExportAgent
```

**Service**

```
ExportService
```

Supported Formats:

- PDF
- HTML
- Markdown
- TXT
- JSON

Output:

```
exports/
```

---

# Workflow Context

Each agent shares data through a common workflow context.

Example:

```python
{
    "video": "...",
    "video_metadata": {},
    "audio": "...",
    "audio_metadata": {},
    "transcript": "...",
    "transcript_metadata": {},
    "analysis": "...",
    "analysis_metadata": {},
    "chat_history": [],
    "report": "...",
    "exports": {},
    "status": "...",
    "current_agent": "..."
}
```

---

# AI Processing Workflow

```
Transcript
      │
      ▼
Build Prompt
      │
      ▼
Provider Factory
      │
      ▼
Selected Provider
      │
      ▼
AI Model
      │
      ▼
AI Response
```

---

# Report Workflow

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
```

---

# Export Workflow

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

# Workflow Storage

Generated files are stored in:

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

# Workflow Benefits

- Modular architecture
- Independent agents
- Reusable services
- Multiple AI providers
- Shared workflow context
- Easy testing
- Easy maintenance
- Simple extensibility

---

# Summary

The AI Video Analysis Agent executes a complete end-to-end workflow beginning with video upload and ending with report export. Each processing stage is handled by a dedicated agent that delegates business logic to services while using a shared workflow context to pass data between stages. This design results in a clean, scalable, and maintainable AI-powered video analysis pipeline.