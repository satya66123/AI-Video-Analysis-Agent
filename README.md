# 🎥 AI Video Analysis Agent

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Application-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Version](https://img.shields.io/badge/Version-v1.0.0-success?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-531%20Passed-success?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-Agent--Service--Provider-blueviolet?style=for-the-badge)
![License](https://img.shields.io/github/license/satya66123/AI-Video-Analysis-Agent?style=for-the-badge)

</p>

---

## 📖 Overview

AI Video Analysis Agent is an AI-powered Streamlit application that automates the complete video analysis workflow.

The application can:

- Upload videos
- Extract metadata
- Extract audio
- Generate transcripts using Whisper
- Perform AI-powered transcript analysis
- Chat with video transcripts
- Generate professional reports
- Export reports in multiple formats

The project follows a clean **Agent → Service → Provider** architecture for modularity, maintainability, and scalability.

---

# ✨ Features

## 🎬 Video Processing

- Video Upload
- Duplicate Detection
- Video Validation
- Upload Progress
- Video Metadata Extraction

---

## 🎵 Audio Processing

- Audio Extraction
- Audio Metadata
- Audio Management

---

## 🎙 Speech Recognition

- OpenAI Whisper Integration
- Multiple Whisper Models
- Long Audio Chunking
- Transcript Generation
- Transcript Storage
- Duplicate Transcript Detection

---

## 🤖 Artificial Intelligence

- AI Transcript Analysis
- AI Chat
- Custom Prompts
- Multi-Provider Support

Supported Providers

- Ollama
- OpenAI
- Anthropic

---

## 📄 Report Generation

Generate professional reports containing:

- Video Information
- Audio Information
- Transcript
- AI Analysis
- Chat History
- Processing Metadata

---

## 📤 Export Formats

- PDF
- HTML
- Markdown
- TXT
- JSON

---

## 📚 History Management

Manage:

- Videos
- Audio
- Metadata
- Transcripts
- AI Analysis
- Chat History
- Reports
- Exported Files

---

# 🏗 Architecture

```
                Streamlit UI
                      │
                      ▼
               Workflow Manager
                      │
                      ▼
                  Agents
                      │
                      ▼
                  Services
                      │
                      ▼
              Provider Factory
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    Ollama        OpenAI      Anthropic
                      │
                      ▼
               Local File Storage
```

---

# 🔄 Workflow

```
Upload Video
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
AI Analysis
      │
      ▼
AI Chat
      │
      ▼
Report Generation
      │
      ▼
Export Reports
```

---

# 📂 Project Structure

```
AI-Video-Analysis-Agent/

app_agent.py

agents/
services/
providers/
workflows/
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
assets/
```

---

# 🛠 Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| UI | Streamlit |
| Speech Recognition | Whisper |
| AI Providers | Ollama, OpenAI, Anthropic |
| Video Processing | OpenCV |
| Audio Processing | FFmpeg |
| Reports | ReportLab |
| Testing | Pytest |
| Version Control | Git & GitHub |

---

## 📸 Application Screenshots

### Dashboard

![Dashboard](docs/screenshots-agents/dashboardPageAgent.png)

---

### Upload Agent

![Upload Agent](docs/screenshots-agents/uploadVideoAgent.png)

---

### Transcript Agent

![Transcript Agent](docs/screenshots-agents/transcriptAgentPage.png)

---

### AI Analysis Agent

![Analysis Agent](docs/screenshots-agents/analysisAgent.png)

---

### AI Chat Agent

![Chat Agent](docs/screenshots-agents/chatAgent.png)

---

### Report Agent

![Report Agent](docs/screenshots-agents/ReportAgent.png)

---

### Export Agent

![Export Agent](docs/screenshots-agents/exportAgent.png)

---

### History Agent

![History Agent](docs/screenshots-agents/historyAgent.png)

---

### Settings

![Settings](docs/screenshots-agents/settingsAgent.png)

---

### About

![About](docs/screenshots-agents/aboutAgent.png)

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/satya66123/AI-Video-Analysis-Agent.git
```

Go to the project folder

```bash
cd AI-Video-Analysis-Agent
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app_agent.py
```

---

# 🧪 Testing

Run all tests

```bash
pytest
```

Verbose mode

```bash
pytest -v
```

Current Results

```
531 Tests Passed
0 Failed
100% Successful
```

---

# 📖 Documentation

The project includes comprehensive documentation:

- API Documentation
- Architecture Guide
- Configuration Guide
- Workflow Guide
- User Guide
- Installation Guide
- Export Guide
- Features Guide
- FAQ
- Troubleshooting Guide
- Provider Guide
- System Design
- Testing Guide
- Project Planner
- Project Structure
- Project Notes
- Security Policy
- Release Notes
- Changelog
- Contributing Guide
- Code of Conduct

---

# 📊 Project Statistics

| Item | Value |
|------|-------|
| Version | v1.0.0 |
| Architecture | Agent → Service → Provider |
| AI Providers | 3 |
| Export Formats | 5 |
| Automated Tests | 531 |
| Test Success | 100% |
| Documentation | Complete |

---

# 🗺 Roadmap

### Version 1.1

- Performance improvements
- UI enhancements
- Bug fixes

### Version 1.2

- OCR Support
- Speaker Diarization
- Subtitle Generation
- Timeline Analysis

### Version 2.0

- REST API
- Docker Support
- Database Integration
- Authentication
- Cloud Deployment

---

# 🤝 Contributing

Contributions are welcome.

Please read:

- CONTRIBUTING.md
- CODE_OF_CONDUCT.md

before submitting pull requests.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub:

**https://github.com/satya66123**

Project Repository:

**https://github.com/satya66123/AI-Video-Analysis-Agent**

---

# ⭐ Support

If you find this project useful:

- ⭐ Star the repository
- 🍴 Fork the project
- 🐞 Report issues
- 💡 Suggest new features

---

<p align="center">

**AI Video Analysis Agent v1.0.0**

Built with ❤️ using Python, Streamlit, Whisper, and AI.

</p>