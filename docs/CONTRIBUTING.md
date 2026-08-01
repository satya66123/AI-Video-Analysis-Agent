# Contributing Guide

![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)
![Pull Requests](https://img.shields.io/badge/Pull%20Requests-Welcome-success)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-Required-success)

First off, thank you for your interest in contributing to the **AI Video Analysis Agent** project!

Whether you're fixing bugs, improving documentation, adding features, or optimizing performance, your contributions are appreciated.

---

# Table of Contents

- Getting Started
- Development Setup
- Project Structure
- Branch Strategy
- Coding Standards
- Testing
- Pull Requests
- Reporting Bugs
- Suggesting Features
- Documentation
- Community Guidelines

---

# Getting Started

1. Fork the repository.
2. Clone your fork.
3. Create a feature branch.
4. Make your changes.
5. Run all tests.
6. Commit your work.
7. Push to GitHub.
8. Open a Pull Request.

---

# Clone Repository

```bash
git clone https://github.com/satya66123/AI-Video-Analysis-Agent.git
```

Move into the project directory.

```bash
cd AI-Video-Analysis-Agent
```

---

# Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

```bash
streamlit run app_agent.py
```

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
```

---

# Branch Naming

Use descriptive branch names.

Examples

```
feature/add-export-format

feature/chat-improvements

bugfix/fix-history-page

bugfix/audio-extraction

docs/update-readme

test/add-export-tests

refactor/provider-factory
```

---

# Coding Standards

Please follow these guidelines.

- Follow PEP 8.
- Write readable code.
- Keep functions focused on a single responsibility.
- Use descriptive variable and function names.
- Add docstrings for public classes and methods.
- Keep business logic inside the Service layer.
- Keep workflow orchestration inside Agents.
- Avoid duplicate code.
- Use type hints where appropriate.

---

# Testing

Run the complete test suite before submitting changes.

```bash
pytest
```

Current project status

```
531 Tests Passed
```

New features should include:

- Unit tests
- Regression tests (if applicable)
- Updated documentation (if behavior changes)

---

# Commit Messages

Use clear and meaningful commit messages.

Examples

```
feat: add export history support

fix: resolve transcript loading issue

docs: update API documentation

test: add speech service tests

refactor: simplify report generation
```

---

# Pull Requests

Before opening a Pull Request, ensure that:

- The application runs successfully.
- All tests pass.
- No unnecessary files are included.
- Documentation is updated if needed.
- Code follows the project's coding standards.

Provide a clear description of:

- What changed
- Why it changed
- How it was tested

---

# Reporting Bugs

When reporting a bug, include:

- Operating System
- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages or logs
- Screenshots (if applicable)

---

# Feature Requests

Feature requests should include:

- Problem statement
- Proposed solution
- Expected benefits
- Possible implementation details (optional)

---

# Documentation Contributions

Documentation improvements are always welcome.

Examples include:

- Fixing typos
- Improving explanations
- Adding examples
- Updating screenshots
- Enhancing setup instructions

---

# Code Review

All contributions may be reviewed before merging.

Reviews typically focus on:

- Code quality
- Readability
- Performance
- Maintainability
- Test coverage
- Documentation

---

# Community Guidelines

Please:

- Be respectful.
- Provide constructive feedback.
- Help other contributors.
- Follow the Code of Conduct.
- Keep discussions professional.

---

# Need Help?

If you have questions about contributing:

- Open a GitHub Issue.
- Start a GitHub Discussion (if enabled).
- Review the project documentation in the `docs/` directory.

---

# Thank You

Thank you for contributing to the **AI Video Analysis Agent** project. Your time, effort, and ideas help improve the project for the entire community.

Happy coding! 🚀