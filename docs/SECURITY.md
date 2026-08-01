# Security Policy

![Security](https://img.shields.io/badge/Security-Policy-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)

## Supported Versions

| Version | Supported |
|----------|-----------|
| v1.0.x | ✅ Yes |

---

# Reporting a Security Issue

If you discover a security vulnerability in this project, please report it responsibly.

Please include:

- Description of the issue
- Steps to reproduce
- Potential impact
- Suggested mitigation (if available)

Please avoid publicly disclosing security vulnerabilities until they have been reviewed.

---

# Security Best Practices

When using this project:

- Keep Python updated.
- Keep project dependencies updated.
- Install packages only from trusted sources.
- Use supported AI provider SDK versions.
- Store API keys securely.
- Do not commit secrets to Git.
- Regularly update project dependencies.

---

# API Keys

If using cloud AI providers:

- OpenAI
- Anthropic

Store API keys using environment variables or a local `.env` file.

Never hard-code credentials into source code.

Example:

```text
OPENAI_API_KEY=your_api_key
ANTHROPIC_API_KEY=your_api_key
```

---

# Local Storage

The application stores generated files locally, including:

- Uploaded videos
- Audio files
- Metadata
- Transcripts
- AI analysis
- Chat history
- Reports
- Exported files

Ensure appropriate file permissions are configured for these directories.

---

# File Validation

The application validates uploaded files before processing to reduce the risk of invalid or unsupported inputs.

---

# Dependency Management

Recommended practices:

- Update dependencies regularly.
- Review dependency changes before upgrading.
- Remove unused packages.

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

# Third-Party Components

This project uses several third-party libraries, including:

- Streamlit
- Whisper
- FFmpeg
- OpenCV
- ReportLab
- Pytest

Refer to the respective projects for their security updates and advisories.

---

# Responsible Disclosure

Security reports will be reviewed and addressed as quickly as possible.

Please provide sufficient technical detail to reproduce the issue.

---

# Security Recommendations

- Protect API keys and credentials.
- Keep your operating system updated.
- Use the latest supported Python version.
- Run the application in a trusted environment.
- Verify AI provider configurations before deployment.

---

# Contact

For security-related questions or vulnerability reports, please use the GitHub repository's issue tracker or contact the project maintainer through GitHub.

---

Thank you for helping improve the security of AI Video Analysis Agent.