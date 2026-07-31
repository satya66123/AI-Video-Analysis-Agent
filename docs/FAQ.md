# ❓ AI Video Analyzer - Frequently Asked Questions (FAQ)

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/FAQ-Documentation-blue?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Version-v1.0.0-success?style=for-the-badge"/>

</p>

---

# Table of Contents

- General Questions
- Installation
- Video Processing
- Audio Processing
- Speech Recognition
- AI Providers
- Export
- Testing
- Troubleshooting

---

# General Questions

## What is AI Video Analyzer?

AI Video Analyzer is a Streamlit-based application that extracts audio from videos, generates transcripts using Whisper, performs AI-powered analysis, supports interactive AI chat, and exports results in multiple formats.

---

## Who is this project for?

- Students
- Developers
- Researchers
- Content Creators
- Educators
- Business Professionals

---

## Which operating systems are supported?

- Windows
- Linux
- macOS

---

# Installation

## Which Python version is required?

Python **3.11 or newer** is recommended.

---

## Do I need FFmpeg?

Yes.

FFmpeg is required for audio extraction from uploaded videos.

---

## Do I need Ollama?

Only if you want to use local AI models.

Cloud providers (OpenAI and Anthropic) do not require Ollama.

---

# Video Processing

## Which video formats are supported?

- MP4
- AVI
- MOV
- MKV
- WEBM

---

## Is there a maximum upload size?

The limit depends on your application configuration.

You can modify it inside the configuration settings if required.

---

## Can I process multiple videos?

Current version focuses on single-video processing.

Batch processing is planned for a future release.

---

# Audio Processing

## Where are extracted audio files stored?

```
audio/
```

---

## Can I reuse extracted audio?

Yes.

Previously extracted audio can be reused without repeating extraction.

---

# Speech Recognition

## Which speech recognition model is used?

OpenAI Whisper.

---

## Does transcription work offline?

Yes.

When Whisper is installed locally, transcription can be performed without an internet connection.

---

# AI Providers

## Which AI providers are supported?

- Ollama
- OpenAI
- Anthropic

---

## Which provider should I use?

| Provider | Best For |
|----------|----------|
| Ollama | Offline local inference |
| OpenAI | High-quality cloud responses |
| Anthropic | Claude-based analysis |

---

## Can I change providers?

Yes.

The provider can be changed from the application settings.

---

# Export

## Which export formats are supported?

- TXT
- Markdown
- HTML
- PDF

---

## Where are exported files stored?

```
exports/
```

---

# Testing

## Which testing framework is used?

Pytest.

---

## Does the project support GitHub Actions?

Yes.

The repository includes automated CI workflows.

---

# Troubleshooting

## The application cannot find FFmpeg.

Ensure FFmpeg is installed and available in your system PATH.

---

## Ollama is not responding.

Run:

```bash
ollama serve
```

---

## API key errors.

Verify your `.env` configuration.

---

## Export failed.

Check:

- Output directory
- File permissions
- Available disk space

---

# Still Need Help?

If you encounter an issue that is not covered here:

1. Review the documentation.
2. Check the Troubleshooting Guide.
3. Open a GitHub Issue.
4. Include logs and screenshots when reporting bugs.

---

# Related Documentation

- INSTALLATION.md
- USER_GUIDE.md
- CONFIGURATION.md
- TROUBLESHOOTING.md
- README.md

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub Repository

https://github.com/satya66123/AI-Video-Analyzer

---

**Version:** v1.0.0

**License:** MIT