# 👤 AI Video Analyzer - User Guide

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
- Getting Started
- Dashboard
- Uploading Videos
- Transcript Generation
- AI Analysis
- AI Chat
- Reports
- Export Center
- Settings
- Keyboard Tips
- Best Practices
- Frequently Asked Questions

---

# Introduction

Welcome to **AI Video Analyzer**.

This guide explains every major feature of the application and provides step-by-step instructions for processing videos, generating transcripts, interacting with AI, and exporting results.

---

# Getting Started

Launch the application:

```bash
streamlit run app.py
```

Open your browser:

```
http://localhost:8501
```

The sidebar provides access to all application modules.

---

# Dashboard

The dashboard is the central hub of the application.

It provides quick access to:

- Upload Video
- Transcript Viewer
- AI Analysis
- AI Chat
- Reports
- Export Center
- Settings

> 📷 **Screenshot Placeholder**
>
> `assets/screenshots/dashboard.png`

---

# Uploading Videos

## Step 1

Open **Upload Video**.

## Step 2

Click **Browse**.

## Step 3

Select a supported video.

Supported formats:

- MP4
- AVI
- MOV
- MKV
- WEBM

## Step 4

Wait for upload completion.

The application validates:

- File format
- File size
- Video integrity

---

# Transcript Generation

After uploading:

1. Audio is extracted.
2. Whisper converts speech to text.
3. Transcript is saved.
4. Transcript becomes available for AI analysis.

> 📷 **Screenshot Placeholder**
>
> `assets/screenshots/transcript.png`

---

# AI Analysis

Select one of the available analysis options.

Examples:

- Summary
- Key Points
- Keywords
- Topics
- Meeting Notes
- Study Notes
- Sentiment Analysis

Choose:

- AI Provider
- AI Model
- Temperature (if available)

Click **Generate Analysis**.

---

# AI Chat

The AI Chat feature allows you to ask questions about the generated transcript.

Example questions:

- Summarize this meeting.
- What decisions were made?
- List all action items.
- Explain the technical discussion.
- Identify important dates.

The conversation history is stored for later reference.

> 📷 **Screenshot Placeholder**
>
> `assets/screenshots/chat.png`

---

# Reports

Generate structured reports from processed content.

Available reports include:

- Transcript Report
- Metadata Report
- AI Analysis Report
- Chat History Report

Reports can be reviewed before export.

---

# Export Center

Export generated content in multiple formats.

| Format | Supported |
|----------|-----------|
| TXT | ✅ |
| Markdown | ✅ |
| HTML | ✅ |
| PDF | ✅ |

Select the desired format and click **Export**.

---

# Settings

Configure application behavior.

Available options may include:

- AI Provider Selection
- Model Selection
- Theme Preferences
- Export Directory
- Processing Options

---

# Keyboard Tips

| Shortcut | Action |
|----------|--------|
| Ctrl + O | Open File |
| Ctrl + S | Save Export |
| Ctrl + C | Copy Selected Text |
| Ctrl + F | Search Transcript |

---

# Best Practices

✔ Use clear audio for accurate transcription.

✔ Keep FFmpeg installed and accessible.

✔ Verify AI provider availability before generating analysis.

✔ Regularly update dependencies.

✔ Store API keys securely using environment variables.

---

# Frequently Asked Questions

### Which video formats are supported?

MP4, AVI, MOV, MKV, and WEBM.

---

### Which AI providers are supported?

- Ollama
- OpenAI
- Anthropic

---

### Can I export reports?

Yes. Supported formats include TXT, Markdown, HTML, and PDF.

---

### Where are transcripts stored?

Inside the `transcripts/` directory.

---

### Can I continue previous AI chats?

Yes, if chat history is enabled and preserved.

---

# Related Documentation

- INSTALLATION.md
- FEATURES.md
- PROJECT_STRUCTURE.md
- ARCHITECTURE.md
- SYSTEM_DESIGN.md
- TESTING.md
- README.md

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub Repository:

https://github.com/satya66123/AI-Video-Analyzer

---

**Version:** v1.0.0

⭐ Thank you for using AI Video Analyzer!