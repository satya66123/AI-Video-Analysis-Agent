# Frequently Asked Questions (FAQ)

![FAQ](https://img.shields.io/badge/FAQ-Guide-blue)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)
![Support](https://img.shields.io/badge/Support-Available-success)

This document answers the most frequently asked questions about the **AI Video Analysis Agent**.

---

# General

### What is AI Video Analysis Agent?

AI Video Analysis Agent is a Streamlit-based application that automatically processes videos by extracting metadata, generating transcripts, performing AI analysis, enabling AI chat, generating reports, and exporting results.

---

### What operating systems are supported?

The application supports:

- Windows
- Linux
- macOS

---

### Which Python version is recommended?

Python **3.11 or later** is recommended.

---

# Installation

### How do I install the project?

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app_agent.py
```

---

### Do I need FFmpeg?

Yes.

FFmpeg is required for audio extraction from videos.

---

### Do I need Whisper?

Yes.

Whisper is used for automatic speech-to-text transcription.

---

# AI Providers

### Which AI providers are supported?

- Ollama
- OpenAI
- Anthropic

---

### Can I use the application offline?

Yes.

Using **Ollama** and **Whisper**, the application can run locally without cloud AI services.

---

# Video Processing

### Which video formats are supported?

- MP4
- AVI
- MOV
- MKV
- WEBM

---

### Can duplicate videos be detected?

Yes.

The application checks uploaded videos to help prevent duplicate processing.

---

# Audio & Transcript

### How is audio extracted?

Audio is extracted automatically during the workflow after a video is uploaded.

---

### Which Whisper models are supported?

Common Whisper models include:

- tiny
- base
- small
- medium
- large

---

### Where are transcripts stored?

```
transcripts/
```

---

# AI Analysis

### What can AI analyze?

The AI can analyze transcript content to produce summaries, insights, key information, and other report content based on the selected prompt and provider.

---

### Can I use different AI models?

Yes.

The available models depend on the configured AI provider.

---

# AI Chat

### Can I ask questions about the video?

Yes.

The chat feature answers questions using the generated transcript as context.

---

### Is chat history saved?

Yes.

Chat history is stored locally.

---

# Reports

### What information is included in reports?

Reports may include:

- Video Information
- Audio Information
- Transcript
- AI Analysis
- Chat History
- Processing Metadata

---

### Which export formats are supported?

- PDF
- HTML
- Markdown
- TXT
- JSON

---

### Where are exported reports stored?

```
exports/
```

---

# Storage

### Where are uploaded videos stored?

```
uploads/
```

---

### Where are audio files stored?

```
audio/
```

---

### Where is metadata stored?

```
metadata/
```

---

### Where are AI analyses stored?

```
analysis/
```

---

### Where are reports stored?

```
reports/
```

---

# Testing

### Which testing framework is used?

Pytest.

---

### How many tests are included?

Current release:

```
531 Tests Passed
```

Run tests:

```bash
pytest
```

---

# Troubleshooting

### The application cannot detect FFmpeg.

Ensure FFmpeg is installed and added to your system PATH.

---

### Whisper transcription fails.

Verify that:

- FFmpeg is installed.
- The audio file is valid.
- The selected Whisper model is available.

---

### AI provider is unavailable.

Check:

- Ollama service is running.
- API keys are configured correctly (for cloud providers).
- Internet connection (if using cloud providers).

---

### Export failed.

Verify that:

- The report was generated successfully.
- The `exports/` directory is writable.
- Sufficient disk space is available.

---

# Documentation

Additional documentation is available in the `docs/` folder:

- API_DOCUMENTATION.md
- ARCHITECTURE.md
- CONFIGURATION.md
- CONTRIBUTING.md
- CHANGELOG.md
- EXPORT_GUIDE.md
- TESTING.md
- USER_GUIDE.md
- ROADMAP.md
- SECURITY.md

---

# Need More Help?

If your question is not answered here:

- Review the project documentation.
- Open a GitHub Issue.
- Check the project README for setup instructions.

---

**Thank you for using AI Video Analysis Agent!**