# ⚙️ AI Video Analyzer - Configuration Guide

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/Configuration-Project%20Settings-blue?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Ollama-Supported-black?style=for-the-badge"/>

<img src="https://img.shields.io/badge/OpenAI-Supported-10A37F?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Anthropic-Supported-5A4FCF?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Environment-.env-success?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge"/>

</p>

---

# Table of Contents

- Introduction
- Configuration Overview
- Project Settings
- Environment Variables
- AI Provider Configuration
- Directory Configuration
- Application Settings
- Logging Configuration
- Security Recommendations
- Best Practices
- Troubleshooting

---

# Introduction

The Configuration Module centralizes all application settings used by AI Video Analyzer.

Keeping configuration separate from business logic improves maintainability, simplifies deployment, and makes future updates easier.

---

# Configuration Overview

```
Application

↓

Configuration

├── Environment Variables

├── Provider Settings

├── Directories

├── Constants

└── Application Options
```

---

# Configuration Files

Typical configuration files include:

```
config/

├── settings.py

├── constants.py

├── models.py

├── providers.py

└── themes.py
```

Project root:

```
.env

requirements.txt

requirements_test.txt

pytest.ini
```

---

# Environment Variables

Sensitive information should be stored in a `.env` file.

Example:

```env
OPENAI_API_KEY=your_openai_api_key

ANTHROPIC_API_KEY=your_anthropic_api_key
```

> Never commit API keys to version control.

---

# AI Provider Configuration

Supported providers:

| Provider | API Key Required |
|-----------|------------------|
| Ollama | ❌ |
| OpenAI | ✅ |
| Anthropic | ✅ |

Example workflow:

```
User

↓

Select Provider

↓

Load Configuration

↓

Initialize Provider

↓

Generate Response
```

---

# Directory Configuration

The application organizes files into dedicated directories.

```
uploads/

audio/

transcripts/

analysis/

reports/

exports/

chat_history/

assets/

docs/
```

Benefits:

- Organized storage
- Easier maintenance
- Simpler backups
- Faster debugging

---

# Application Settings

Typical configurable values include:

| Setting | Description |
|----------|-------------|
| Application Name | Display title |
| Version | Current release |
| Upload Directory | Video storage |
| Export Directory | Generated files |
| Maximum Upload Size | File limit |
| Supported Formats | Allowed video types |
| Default Provider | Selected AI provider |
| Default Model | Preferred AI model |

---

# Logging Configuration

Recommended log levels:

```
DEBUG

INFO

WARNING

ERROR

CRITICAL
```

Suggested log information:

- Application startup
- Video upload
- Audio extraction
- Transcript generation
- AI analysis
- Export completion
- Errors

---

# Configuration Loading

```
Start Application

↓

Load Configuration

↓

Validate Settings

↓

Initialize Providers

↓

Initialize Services

↓

Ready
```

---

# Security Recommendations

Follow these best practices:

- Store secrets in `.env`
- Never expose API keys
- Validate uploaded files
- Restrict supported file types
- Use dedicated storage folders
- Keep dependencies updated

---

# Deployment Checklist

Before deployment, verify:

✅ Configuration files exist

✅ Environment variables are configured

✅ Required directories are present

✅ Dependencies are installed

✅ AI providers are available

✅ FFmpeg is installed

✅ Ollama is running (if used)

---

# Best Practices

✔ Keep configuration centralized.

✔ Avoid hard-coded values.

✔ Use environment variables for secrets.

✔ Validate configuration during startup.

✔ Document every configurable option.

✔ Maintain separate development and production configurations if needed.

---

# Troubleshooting

### Missing API Key

Verify the `.env` file and restart the application.

---

### Invalid Configuration

Check for missing or incorrect values in the configuration files.

---

### Provider Initialization Failed

Ensure the selected provider is correctly configured and available.

---

### Missing Directories

Create the required folders or allow the application to generate them automatically.

---

# Related Documentation

- INSTALLATION.md
- PROVIDER_GUIDE.md
- API_DOCUMENTATION.md
- WORKFLOW.md
- SECURITY.md
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

⭐ Proper configuration is the foundation of a secure, reliable, and maintainable AI Video Analyzer deployment.