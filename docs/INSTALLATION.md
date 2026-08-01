# Installation Guide

![Installation](https://img.shields.io/badge/Installation-Guide-blue)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)

This guide explains how to install and run the **AI Video Analysis Agent**.

---

# System Requirements

| Component | Requirement |
|-----------|-------------|
| Python | 3.11 or later |
| RAM | Minimum 8 GB |
| Storage | Minimum 5 GB Free |
| FFmpeg | Required |
| Git | Recommended |

---

# Step 1 — Clone the Repository

```bash
git clone https://github.com/satya66123/AI-Video-Analysis-Agent.git
```

Move into the project folder.

```bash
cd AI-Video-Analysis-Agent
```

---

# Step 2 — Create a Virtual Environment

```bash
python -m venv venv
```

---

# Step 3 — Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

# Step 4 — Install Project Dependencies

```bash
pip install -r requirements.txt
```

---

# Step 5 — Install FFmpeg

FFmpeg is required for audio extraction.

### Windows

Download FFmpeg and add it to your system PATH.

Verify installation:

```bash
ffmpeg -version
```

### Linux

```bash
sudo apt install ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

---

# Step 6 — Install Ollama (Optional)

If using local AI models:

Install Ollama from:

https://ollama.com

Pull a model:

```bash
ollama pull llama3.1
```

Verify installation:

```bash
ollama list
```

---

# Step 7 — Configure API Keys (Optional)

If using cloud AI providers, configure environment variables.

OpenAI

```text
OPENAI_API_KEY=your_api_key
```

Anthropic

```text
ANTHROPIC_API_KEY=your_api_key
```

---

# Step 8 — Run the Application

Start the Streamlit application.

```bash
streamlit run app_agent.py
```

The application will automatically open in your default web browser.

---

# Project Structure

```
AI-Video-Analysis-Agent/

app_agent.py

agents/

services/

providers/

ui/

utils/

workflows/

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

requirements.txt
```

---

# Verify Installation

Run the automated test suite.

```bash
pytest
```

Expected result:

```
531 Tests Passed
```

---

# Supported AI Providers

- Ollama
- OpenAI
- Anthropic

---

# Supported Video Formats

- MP4
- AVI
- MOV
- MKV
- WEBM

---

# Supported Export Formats

- PDF
- HTML
- Markdown
- TXT
- JSON

---

# Troubleshooting

### Python Not Found

Verify your Python installation.

```bash
python --version
```

---

### FFmpeg Not Found

Verify FFmpeg is installed and available in your system PATH.

```bash
ffmpeg -version
```

---

### Ollama Connection Error

Ensure the Ollama service is running.

```bash
ollama list
```

---

### Missing Dependencies

Reinstall project dependencies.

```bash
pip install -r requirements.txt
```

---

### Streamlit Not Found

Install Streamlit.

```bash
pip install streamlit
```

---

# Installation Complete

Your AI Video Analysis Agent is now ready to use.

Launch the application anytime with:

```bash
streamlit run app_agent.py
```

Enjoy building and analyzing videos with AI!