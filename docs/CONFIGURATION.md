# Configuration Guide

![Configuration](https://img.shields.io/badge/Configuration-Guide-blue)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Configured-FF4B4B?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Stable-success)

> This document describes the configuration options for the AI Video Analysis Agent.

---

# Table of Contents

- Overview
- System Requirements
- Python Environment
- Project Configuration
- AI Provider Configuration
- Whisper Configuration
- Streamlit Configuration
- Storage Configuration
- Export Configuration
- Environment Variables
- Folder Structure
- Recommended Settings
- Troubleshooting

---

# Overview

The AI Video Analysis Agent uses local configuration files and environment variables to control application behavior.

Configuration areas include:

- Python environment
- Streamlit
- AI Providers
- Whisper
- Export settings
- Storage folders
- Logging

---

# System Requirements

| Component | Requirement |
|-----------|-------------|
| Python | 3.11+ |
| RAM | 8 GB Minimum |
| Recommended RAM | 16 GB |
| Disk Space | 5 GB+ |
| FFmpeg | Required |
| Git | Recommended |

---

# Python Environment

Create a virtual environment.

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Project Configuration

Main application

```
app_agent.py
```

Launch

```bash
streamlit run app_agent.py
```

---

# AI Provider Configuration

Supported Providers

- Ollama
- OpenAI
- Anthropic

Provider selection is available from the application interface.

---

# Ollama Configuration

Example models

```
llama3.1

qwen3

qwen2.5

mistral

gemma3

phi3
```

Ensure Ollama is installed and running before using local models.

---

# OpenAI Configuration

Set the API key as an environment variable.

Example

```
OPENAI_API_KEY=your_api_key
```

---

# Anthropic Configuration

Set the API key as an environment variable.

Example

```
ANTHROPIC_API_KEY=your_api_key
```

---

# Whisper Configuration

Default Model

```
base
```

Available models

```
tiny

base

small

medium

large
```

Model selection can be changed from the application.

---

# Streamlit Configuration

Run

```bash
streamlit run app_agent.py
```

Optional configuration

```
Dark Theme

Wide Layout

Sidebar Navigation
```

---

# Storage Configuration

Default folders

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

Folders are automatically created if they do not exist.

---

# Export Configuration

Supported formats

- PDF
- HTML
- Markdown
- TXT
- JSON

Export files are stored in

```
exports/
```

---

# Environment Variables

Optional environment variables

```
OPENAI_API_KEY

ANTHROPIC_API_KEY

OLLAMA_HOST
```

Example

```
OPENAI_API_KEY=xxxxxxxx

ANTHROPIC_API_KEY=xxxxxxxx

OLLAMA_HOST=http://localhost:11434
```

---

# Logging

Application logging includes

- Upload status
- Metadata generation
- Audio extraction
- Transcript generation
- AI analysis
- Chat execution
- Report generation
- Export operations

---

# Folder Structure

```
AI-Video-Analysis-Agent/

app_agent.py

agents/

services/

providers/

ui/

utils/

uploads/

audio/

metadata/

transcripts/

analysis/

chat_history/

reports/

exports/

tests/

docs/
```

---

# Recommended Settings

| Component | Recommended |
|-----------|-------------|
| Python | 3.11+ |
| Whisper Model | base |
| AI Provider | Ollama |
| Export Format | PDF + HTML |
| Storage | Local JSON |
| Streamlit | Wide Layout |

---

# Troubleshooting

### FFmpeg not found

Install FFmpeg and ensure it is available in your system PATH.

---

### Whisper model download fails

Check your internet connection and retry downloading the selected model.

---

### Ollama connection error

Verify that the Ollama service is running.

---

### OpenAI or Anthropic authentication error

Confirm that the corresponding API key is correctly configured.

---

### Export generation fails

Verify write permissions for the `exports/` directory and ensure sufficient disk space.

---

# Summary

The AI Video Analysis Agent is designed with minimal configuration requirements. Most directories are created automatically, AI providers can be selected through the application, and environment variables are only needed for cloud-based providers. Local execution with Ollama and Whisper provides a straightforward setup for offline AI-powered video analysis.