# 🛠️ AI Video Analyzer - Troubleshooting Guide

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/Troubleshooting-Solutions-red?style=for-the-badge"/>

<img src="https://img.shields.io/badge/PyTest-Tested-success?style=for-the-badge&logo=pytest"/>

<img src="https://img.shields.io/badge/GitHub-Actions-blue?style=for-the-badge&logo=github"/>

<img src="https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge"/>

</p>

---

# Table of Contents

- Introduction
- Installation Problems
- Application Startup Issues
- Video Processing Issues
- Audio Processing Issues
- Speech Recognition Issues
- AI Provider Issues
- Export Issues
- Testing Issues
- GitHub Actions Issues
- Frequently Encountered Errors
- Getting Support

---

# Introduction

This guide provides solutions for common problems encountered while installing, configuring, and using **AI Video Analyzer**.

Before reporting a bug, review the solutions below, as many issues can be resolved with a few simple checks.

---

# Installation Problems

## Python Not Found

### Error

```text
python is not recognized as an internal or external command
```

### Solution

- Install Python 3.11+
- Enable **Add Python to PATH**
- Restart the terminal

Verify:

```bash
python --version
```

---

## pip Not Found

### Error

```text
pip is not recognized
```

### Solution

```bash
python -m ensurepip

python -m pip install --upgrade pip
```

---

## Dependency Installation Failed

Install all dependencies again.

```bash
pip install -r requirements.txt
```

Install testing dependencies.

```bash
pip install -r requirements_test.txt
```

---

# Application Startup Issues

## Streamlit Not Found

```text
ModuleNotFoundError: streamlit
```

Install Streamlit.

```bash
pip install streamlit
```

---

## App Does Not Start

Run

```bash
streamlit run app.py
```

Check for:

- Missing dependencies
- Incorrect virtual environment
- Syntax errors

---

# Video Processing Issues

## Unsupported Video Format

Supported formats:

- MP4
- AVI
- MOV
- MKV
- WEBM

---

## Video Upload Failed

Possible causes:

- Unsupported extension
- Corrupted file
- File too large
- Permission denied

---

## Video Metadata Missing

Verify:

- Video is readable
- File is not corrupted
- Upload completed successfully

---

# Audio Processing Issues

## Audio Extraction Failed

Verify FFmpeg installation.

```bash
ffmpeg -version
```

---

## Audio File Not Generated

Possible reasons:

- Invalid video
- FFmpeg missing
- Permission denied

---

## Audio Duration Incorrect

Re-upload the original video and regenerate audio.

---

# Speech Recognition Issues

## Whisper Model Failed

Check:

- Whisper installation
- Audio validity
- Available system memory

---

## Empty Transcript

Possible causes:

- Silent audio
- Corrupted audio
- Unsupported encoding

---

## Poor Transcription Quality

Recommendations:

- Use clear audio
- Reduce background noise
- Avoid heavily compressed recordings

---

# AI Provider Issues

## Ollama Connection Failed

Verify:

```bash
ollama serve
```

Check available models.

```bash
ollama list
```

---

## Model Not Found

Download the required model.

Example:

```bash
ollama pull llama3.1
```

---

## OpenAI Authentication Error

Verify:

```
OPENAI_API_KEY
```

inside the `.env` file.

---

## Anthropic Authentication Error

Verify:

```
ANTHROPIC_API_KEY
```

---

# Export Issues

## PDF Export Failed

Possible causes:

- Missing dependencies
- Invalid output directory
- Permission issues

---

## HTML Export Failed

Verify:

- Write permissions
- Available disk space

---

## Empty Export

Generate transcript and AI analysis before exporting.

---

# Testing Issues

## Pytest Not Found

Install:

```bash
pip install pytest
```

---

## Tests Failing

Recommended steps:

- Activate virtual environment
- Install requirements
- Review error logs
- Verify mocked dependencies

---

## Import Errors

Run tests from the project root.

---

# GitHub Actions Issues

## Workflow Failed

Verify:

- requirements.txt
- requirements_test.txt
- Workflow YAML
- Python version

---

## Missing Dependency

Add the missing package to:

```
requirements.txt
```

or

```
requirements_test.txt
```

Commit the update and rerun the workflow.

---

## CI Passes Locally but Fails Online

Check:

- Python version mismatch
- Missing dependency
- Platform-specific paths
- File permissions

---

# Frequently Encountered Errors

| Error | Solution |
|--------|----------|
| ModuleNotFoundError | Install missing package |
| FileNotFoundError | Verify file path |
| PermissionError | Check directory permissions |
| TimeoutError | Retry operation |
| ConnectionError | Verify network/provider |
| ValueError | Validate user input |

---

# Diagnostic Checklist

Before reporting an issue, verify:

✅ Python installed

✅ Virtual environment activated

✅ Dependencies installed

✅ FFmpeg available

✅ Ollama running (if used)

✅ API keys configured

✅ Tests passing

✅ Latest project version

---

# Reporting Bugs

Include the following information:

- Operating System
- Python Version
- Error Message
- Stack Trace
- Steps to Reproduce
- Screenshots (if applicable)
- Log Files

---

# Getting Support

Helpful resources:

- Project Documentation
- GitHub Issues
- GitHub Discussions
- Project Wiki

---

# Related Documentation

- INSTALLATION.md
- USER_GUIDE.md
- CONFIGURATION.md
- TESTING.md
- SECURITY.md
- FAQ.md
- README.md

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub Repository

https://github.com/satya66123/AI-Video-Analyzer

---

## License

Released under the **MIT License**.

---

**Version:** v1.0.0

⭐ This troubleshooting guide is intended to help users quickly diagnose and resolve common issues while using AI Video Analyzer.