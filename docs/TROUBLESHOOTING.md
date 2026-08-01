# Troubleshooting Guide

![Troubleshooting](https://img.shields.io/badge/Troubleshooting-Guide-orange)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)
![Support](https://img.shields.io/badge/Support-Available-success)

This guide provides solutions to common issues encountered while using the AI Video Analysis Agent.

---

# Installation Issues

## Python Not Found

### Problem

```
'python' is not recognized as an internal or external command.
```

### Solution

- Install Python 3.11 or later.
- Add Python to your system PATH.
- Verify installation:

```bash
python --version
```

---

## Missing Dependencies

### Problem

```
ModuleNotFoundError
```

### Solution

Install project dependencies.

```bash
pip install -r requirements.txt
```

---

## Streamlit Not Installed

### Problem

```
ModuleNotFoundError: streamlit
```

### Solution

```bash
pip install streamlit
```

---

# FFmpeg Issues

## FFmpeg Not Found

### Problem

```
ffmpeg not found
```

### Solution

Install FFmpeg and verify:

```bash
ffmpeg -version
```

Add FFmpeg to the system PATH if necessary.

---

# Video Upload Issues

## Invalid Video Format

### Problem

Video cannot be uploaded.

### Solution

Supported formats:

- MP4
- AVI
- MOV
- MKV
- WEBM

---

## Duplicate Video

### Problem

The application reports a duplicate upload.

### Solution

Rename the file or upload a different video. Duplicate detection uses file hashing.

---

# Audio Issues

## Audio Extraction Failed

### Problem

Audio could not be extracted.

### Solution

- Verify FFmpeg installation.
- Confirm the video file is valid.
- Try another video.

---

# Whisper Issues

## Whisper Model Download Error

### Problem

Whisper model cannot be loaded.

### Solution

Check your internet connection for the initial model download and ensure sufficient disk space.

---

## Empty Transcript

### Problem

No transcript is generated.

### Solution

- Verify the video contains speech.
- Check audio quality.
- Try another Whisper model.

---

## Long Audio Processing

### Problem

Transcription is slow.

### Solution

- Use a smaller Whisper model.
- Reduce audio duration.
- Increase system memory if available.

---

# AI Provider Issues

## Ollama Not Running

### Problem

Cannot connect to Ollama.

### Solution

Start the Ollama service.

Verify installation:

```bash
ollama list
```

---

## OpenAI Authentication Error

### Problem

Invalid API key.

### Solution

Verify:

```text
OPENAI_API_KEY
```

is configured correctly.

---

## Anthropic Authentication Error

### Problem

Authentication failed.

### Solution

Verify:

```text
ANTHROPIC_API_KEY
```

is configured correctly.

---

## Provider Not Found

### Problem

Selected provider is unavailable.

### Solution

- Verify provider configuration.
- Check Provider Factory registration.
- Confirm required dependencies are installed.

---

# AI Analysis Issues

## Analysis Failed

### Problem

No AI response returned.

### Solution

- Verify provider connection.
- Confirm selected model exists.
- Check transcript availability.

---

# Chat Issues

## AI Chat Not Responding

### Problem

Chat returns no answer.

### Solution

- Generate a transcript first.
- Verify AI provider.
- Confirm model availability.

---

# Export Issues

## PDF Export Failed

### Problem

PDF generation failed.

### Solution

- Verify ReportLab installation.
- Check write permissions.
- Ensure the report was generated successfully.

---

## Export Folder Missing

### Problem

Exported files are not found.

### Solution

Create the folder if necessary:

```
exports/
```

---

# File Permission Issues

### Problem

Permission denied.

### Solution

- Close files opened by other applications.
- Run the application with appropriate permissions.
- Verify folder write access.

---

# Testing Issues

## Test Failure

### Problem

One or more tests fail.

### Solution

Run:

```bash
pytest
```

Review the error output and verify project dependencies.

---

## Mock Errors

### Problem

Mock-related test failures.

### Solution

- Verify mock paths.
- Check import statements.
- Ensure patched objects match the source code.

---

# Performance Issues

## Slow Processing

### Solution

- Use a smaller Whisper model.
- Close unnecessary applications.
- Process shorter videos.
- Use local SSD storage.

---

## High Memory Usage

### Solution

- Process smaller videos.
- Reduce chunk size.
- Close background applications.

---

# Common Error Messages

| Error | Solution |
|--------|----------|
| ModuleNotFoundError | Install missing dependency |
| FileNotFoundError | Verify file path |
| PermissionError | Check file permissions |
| ValueError | Validate user input |
| RuntimeError | Review logs for processing failures |
| ConnectionError | Verify AI provider connection |

---

# Recommended Checks

Before reporting an issue:

- Verify Python installation.
- Verify FFmpeg installation.
- Install all dependencies.
- Check API keys.
- Confirm AI provider availability.
- Ensure uploaded files are valid.
- Review application logs.
- Run the automated test suite.

---

# Getting Help

If the issue persists:

1. Review the project documentation.
2. Check the FAQ.
3. Run the application with logs enabled.
4. Open an issue on the GitHub repository with:
   - Error message
   - Steps to reproduce
   - Operating system
   - Python version
   - Project version

---

# Summary

Most issues can be resolved by verifying dependencies, AI provider configuration, FFmpeg installation, file permissions, and supported input formats. The comprehensive test suite (**531 passing tests**) also provides a reliable baseline for validating project functionality.