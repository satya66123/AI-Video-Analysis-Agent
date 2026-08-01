# User Guide

![User Guide](https://img.shields.io/badge/User-Guide-blue)
![Version](https://img.shields.io/badge/Version-v1.0.0-success)
![Platform](https://img.shields.io/badge/Platform-Streamlit-red)

---

# Introduction

Welcome to the **AI Video Analysis Agent**.

This application automates video processing using Artificial Intelligence. It extracts audio, generates transcripts, performs AI-powered analysis, enables transcript-based chat, generates professional reports, and exports results in multiple formats.

---

# Features

The application includes:

- Video Upload
- Video Metadata Extraction
- Audio Extraction
- Speech-to-Text (Whisper)
- AI Analysis
- AI Chat
- Report Generation
- Export Reports
- History Management
- Multiple AI Provider Support

---

# Launching the Application

Run the application using:

```bash
streamlit run app_agent.py
```

The application opens automatically in your default web browser.

---

# Home Page

The home page provides access to all major modules through the sidebar navigation.

Available sections include:

- Upload
- Metadata
- Audio
- Transcript
- AI Analysis
- AI Chat
- Reports
- Export
- History
- Settings

---

# Uploading a Video

1. Open the **Upload** page.
2. Click **Browse**.
3. Select a supported video.
4. Wait for the upload to complete.

Supported formats:

- MP4
- AVI
- MOV
- MKV
- WEBM

The application automatically checks for duplicate videos before processing.

---

# Viewing Metadata

After uploading a video, metadata is extracted automatically.

Available information includes:

- File Name
- Duration
- Resolution
- FPS
- Format
- File Size

---

# Audio Extraction

The application extracts audio from the uploaded video automatically.

Extracted audio is stored for transcription and future processing.

---

# Generating a Transcript

1. Open the **Transcript** page.
2. Select a Whisper model.
3. Click **Generate Transcript**.
4. Wait until processing completes.

The generated transcript is saved automatically.

---

# Performing AI Analysis

1. Open the **AI Analysis** page.
2. Select:

- AI Provider
- AI Model

3. Enter an optional custom prompt.
4. Click **Analyze**.

The generated analysis is stored for reporting.

---

# AI Chat

The AI Chat page allows you to ask questions about the generated transcript.

Steps:

1. Open **AI Chat**.
2. Enter your question.
3. Click **Send**.
4. View the AI response.

Conversation history is saved automatically.

---

# Report Generation

Open the **Reports** page.

Click:

```
Generate Report
```

The report contains:

- Video Information
- Audio Information
- Transcript
- AI Analysis
- Chat History
- Processing Metadata

---

# Export Reports

Navigate to the **Export** page.

Choose one or more formats:

- PDF
- HTML
- Markdown
- TXT
- JSON

Click:

```
Export
```

The generated files are saved automatically.

---

# History

The History page allows you to manage previously generated data.

Available sections:

- Videos
- Audio
- Metadata
- Transcripts
- Analysis
- Chat History
- Reports
- Exports

Users can view, load, or delete stored files.

---

# AI Providers

Supported providers:

- Ollama
- OpenAI
- Anthropic

Select the desired provider and model before running AI analysis or chat.

---

# Folder Structure

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

# Tips

- Upload clear videos with good audio quality.
- Generate a transcript before using AI Analysis or AI Chat.
- Use local AI providers (Ollama) for offline processing.
- Export reports after analysis for sharing or documentation.
- Regularly review the History page to manage stored files.

---

# Troubleshooting

If you encounter issues:

- Verify Python and dependencies are installed.
- Ensure FFmpeg is available.
- Confirm AI providers are configured correctly.
- Check that the uploaded video is in a supported format.
- Refer to the **Troubleshooting Guide** for detailed solutions.

---

# Best Practices

- Process one video at a time for optimal performance.
- Keep dependencies updated.
- Organize exported reports by project.
- Run the test suite after major changes.
- Back up important reports and transcripts.

---

# Getting Help

If you need assistance:

- Review the project documentation.
- Check the FAQ.
- Read the Installation Guide.
- Open an issue on the GitHub repository if you encounter a bug.

---

# Summary

The AI Video Analysis Agent provides a complete workflow for AI-powered video processing. From video upload to transcript generation, AI analysis, chat, report creation, and export, the application is designed to be simple, modular, and efficient for users who need automated video understanding and documentation.