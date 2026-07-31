# 🚀 AI Video Analyzer - Installation Guide

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/Streamlit-1.46+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

<img src="https://img.shields.io/badge/Ollama-Supported-black?style=for-the-badge"/>

<img src="https://img.shields.io/badge/OpenAI-Supported-10A37F?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Anthropic-Supported-5A4FCF?style=for-the-badge"/>

<img src="https://github.com/satya66123/AI-Video-Analyzer/actions/workflows/python-tests.yml/badge.svg"/>

<img src="https://img.shields.io/badge/Pytest-Passing-success?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge"/>

</p>

---

# 📖 Table of Contents

- Introduction
- System Requirements
- Prerequisites
- Clone Repository
- Project Structure
- Virtual Environment
- Install Dependencies
- Configure Environment
- Install Ollama
- Download AI Models
- Running the Application
- Running Tests
- GitHub Actions
- Troubleshooting
- Related Documentation

---

# 🎯 Introduction

Welcome to the **AI Video Analyzer** installation guide.

AI Video Analyzer is a modular **Streamlit** application that extracts audio from videos, generates transcripts using Whisper, performs AI-powered analysis, allows conversational interaction with transcripts, and exports results into multiple formats.

The application follows a layered architecture using reusable components, service classes, provider abstraction, and automated testing.

---

# 💻 System Requirements

| Component | Minimum | Recommended |
|-----------|----------|-------------|
| Python | 3.11 | Latest 3.11.x |
| RAM | 8 GB | 16 GB |
| CPU | 4 Cores | 8+ Cores |
| Storage | 5 GB | 20 GB SSD |
| Internet | Optional | Required for cloud providers |

---

# 📦 Prerequisites

Install the following software before starting.

| Software | Required |
|----------|----------|
| Git | ✅ |
| Python 3.11+ | ✅ |
| pip | ✅ |
| FFmpeg | ✅ |
| Ollama | Optional |
| VS Code / PyCharm | Recommended |

Verify installation:

```bash
python --version
pip --version
git --version
ffmpeg -version
```

---

# 📥 Clone Repository

Clone the repository from GitHub.

```bash
git clone https://github.com/satya66123/AI-Video-Analyzer.git
```

Navigate to the project directory.

```bash
cd AI-Video-Analyzer
```

---

# 📂 Project Structure

```
AI-Video-Analyzer/
│
├── analysis/
├── audio/
├── chat_history/
├── components/
├── config/
├── docs/
├── exports/
├── pages/
├── prompts/
├── providers/
├── reports/
├── services/
├── tests/
├── transcripts/
├── uploads/
├── utils/
│
├── app.py
├── requirements.txt
├── requirements_test.txt
├── pytest.ini
└── README.md
```

---

# 🐍 Create Virtual Environment

## Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

---

## Linux

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

## macOS

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

# 📚 Install Dependencies

Install application dependencies.

```bash
pip install -r requirements.txt
```

Install testing dependencies.

```bash
pip install -r requirements_test.txt
```

Verify installation.

```bash
pip list
```

---

# ⚙ Configure Environment

Create a `.env` file in the project root if you intend to use cloud AI providers.

Example:

```env
OPENAI_API_KEY=your_api_key
ANTHROPIC_API_KEY=your_api_key
```

> **Note:** Ollama users do not require API keys.

---

# 🤖 Install Ollama

Download Ollama from:

https://ollama.com/download

Verify installation.

```bash
ollama --version
```

Start the Ollama server.

```bash
ollama serve
```

---

# 📥 Download Supported Models

Examples:

```bash
ollama pull llama3.1
```

```bash
ollama pull qwen2.5:1.5b
```

```bash
ollama pull gemma3:4b
```

```bash
ollama pull mistral
```

---

# ▶ Running the Application

Launch the Streamlit application.

```bash
streamlit run app.py
```

Open your browser:

```
http://localhost:8501
```

---

# 🧪 Running Tests

Run all tests.

```bash
pytest
```

Verbose mode.

```bash
pytest -v
```

Coverage report.

```bash
pytest --cov=. --cov-report=html
```

---

# ⚙ Continuous Integration

The project includes GitHub Actions for automated testing.

The workflow automatically:

- Installs dependencies
- Runs the complete Pytest suite
- Generates coverage reports
- Validates every push and pull request

Workflow location:

```
.github/workflows/python-tests.yml
```

---

# 🛠 Troubleshooting

## Missing Dependency

```bash
pip install -r requirements.txt
```

---

## FFmpeg Not Found

Verify installation.

```bash
ffmpeg -version
```

---

## Ollama Connection Error

Start the Ollama server.

```bash
ollama serve
```

---

## Test Failures

Install test dependencies.

```bash
pip install -r requirements_test.txt
```

---

# 📚 Related Documentation

- FEATURES.md
- PROJECT_STRUCTURE.md
- ARCHITECTURE.md
- SYSTEM_DESIGN.md
- TESTING.md
- USER_GUIDE.md

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub Repository:

https://github.com/satya66123/AI-Video-Analyzer

---

## ⭐ Support the Project

If you find this project helpful, consider giving it a **GitHub Star** and sharing feedback through Issues or Pull Requests.

---

**Version:** v1.0.0