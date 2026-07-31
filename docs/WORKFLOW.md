# 🔄 AI Video Analyzer - Workflow Guide

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/Streamlit-1.46+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

<img src="https://img.shields.io/badge/Whisper-Speech%20Recognition-blue?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge"/>

<img src="https://img.shields.io/badge/GitHub%20Actions-Passing-success?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge"/>

</p>

---

# Table of Contents

- Introduction
- Workflow Overview
- Video Processing Workflow
- AI Analysis Workflow
- Chat Workflow
- Export Workflow
- Complete System Flow
- Error Recovery
- Workflow Benefits

---

# Introduction

This document explains how AI Video Analyzer processes a video from upload to final export. Understanding these workflows helps developers extend the application and helps users understand how each module interacts.

---

# Complete Workflow Overview

```
User
 │
 ▼
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
Speech Recognition
 │
 ▼
Transcript Generation
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

# Video Upload Workflow

## Step 1 — User Upload

The user uploads a supported video file.

Supported formats:

- MP4
- AVI
- MOV
- MKV
- WEBM

---

## Step 2 — Validation

The application verifies:

- File exists
- Supported extension
- Maximum size
- Readability
- Duplicate detection (if implemented)

```
Video

↓

Validation

↓

Accepted
```

---

# Metadata Workflow

After validation, metadata is collected.

Examples:

- File Name
- File Size
- Duration
- Resolution
- FPS
- Codec

```
Video

↓

Metadata Extraction

↓

Metadata Report
```

---

# Audio Processing Workflow

The uploaded video is converted into an audio stream.

```
Video

↓

Extract Audio

↓

Save Audio

↓

Audio Metadata
```

Responsibilities:

- Extract audio
- Save audio
- Verify extraction
- Read audio information

---

# Speech Recognition Workflow

The extracted audio is processed using Whisper.

```
Audio

↓

Whisper Model

↓

Speech Recognition

↓

Transcript
```

Output:

- Transcript text
- Processing status
- Saved transcript file

---

# AI Analysis Workflow

The transcript becomes the input for AI processing.

```
Transcript

↓

Prompt Builder

↓

Selected Provider

↓

Selected Model

↓

Generated Analysis
```

Available analysis types include:

- Summary
- Key Points
- Keywords
- Topics
- Meeting Notes
- Study Notes
- Sentiment Analysis

---

# AI Chat Workflow

The transcript provides context for interactive conversations.

```
User Question

↓

Transcript Context

↓

AI Provider

↓

Response

↓

Chat History
```

Benefits:

- Context-aware answers
- Conversation history
- Interactive learning

---

# Report Generation Workflow

Generated content is organized into reports.

```
Transcript

+

Metadata

+

AI Analysis

↓

Reports
```

Available reports:

- Transcript Report
- Metadata Report
- AI Analysis Report
- Chat Report

---

# Export Workflow

Reports can be exported into multiple formats.

```
Generated Report

↓

Export Service

├── TXT
├── Markdown
├── HTML
└── PDF
```

---

# Complete Processing Pipeline

```
Upload

↓

Validate

↓

Metadata

↓

Extract Audio

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

# Error Recovery Workflow

The application should recover gracefully whenever possible.

Examples:

```
Upload Error

↓

Display Message

↓

Retry Upload
```

```
Provider Error

↓

Switch Provider

↓

Retry Analysis
```

```
Export Failure

↓

Display Error

↓

Retry Export
```

---

# Workflow Advantages

- Modular processing
- Easy debugging
- Independent services
- Reusable components
- Provider flexibility
- Scalable architecture
- Reliable processing pipeline

---

# Best Practices

✔ Validate inputs before processing.

✔ Keep intermediate files organized.

✔ Save transcripts before AI analysis.

✔ Handle provider failures gracefully.

✔ Export only verified results.

✔ Log important processing events.

---

# Related Documentation

- INSTALLATION.md
- FEATURES.md
- PROJECT_STRUCTURE.md
- ARCHITECTURE.md
- SYSTEM_DESIGN.md
- USER_GUIDE.md
- API_DOCUMENTATION.md
- PROVIDER_GUIDE.md
- TESTING.md
- README.md

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub Repository

https://github.com/satya66123/AI-Video-Analyzer

---

## License

This project is licensed under the **MIT License**.

---

**Version:** v1.0.0

⭐ Thank you for using **AI Video Analyzer**.