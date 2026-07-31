# 🧪 AI Video Analyzer - Testing Guide

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/PyTest-Tested-success?style=for-the-badge&logo=pytest"/>

<img src="https://img.shields.io/badge/GitHub%20Actions-CI-blue?style=for-the-badge&logo=githubactions"/>

<img src="https://img.shields.io/badge/Coverage-Unit%20Tests-green?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge"/>

</p>

---

# Table of Contents

- Introduction
- Testing Strategy
- Test Structure
- Running Tests
- Test Coverage
- Fixtures
- Mocking
- Continuous Integration
- Writing New Tests
- Best Practices
- Troubleshooting

---

# Introduction

AI Video Analyzer uses **Pytest** for automated testing to ensure reliability, maintainability, and code quality.

The project includes unit tests covering services, providers, utilities, components, prompts, and configuration modules.

---

# Testing Goals

The testing framework is designed to:

- Verify application behavior
- Detect regressions
- Validate business logic
- Ensure provider compatibility
- Improve maintainability
- Support continuous integration

---

# Testing Stack

| Tool | Purpose |
|-------|----------|
| Pytest | Unit Testing |
| unittest.mock | Mock Objects |
| pytest Fixtures | Test Setup |
| GitHub Actions | Continuous Integration |

---

# Test Directory Structure

```
tests/

├── conftest.py
├── test_requirements.py
├── test_app.py
├── test_audio_service.py
├── test_video_service.py
├── test_speech_service.py
├── test_export_service.py
├── test_ai_analysis_service.py
├── test_metadata_service.py
├── test_provider_factory.py
├── test_ollama_provider.py
├── test_openai_provider.py
├── test_anthropic_provider.py
├── test_file_validator.py
├── test_transcript_utils.py
├── ...
```

> Continue adding test files following the same naming convention as new modules are introduced.

---

# Running Tests

Run all tests:

```bash
pytest
```

Verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_audio_service.py
```

Run a specific test case:

```bash
pytest tests/test_audio_service.py::test_extract_audio
```

Generate a coverage report:

```bash
pytest --cov=. --cov-report=html
```

---

# Test Coverage

The following modules should be covered by automated tests.

| Module | Tested |
|----------|:------:|
| Components | ✅ |
| Services | ✅ |
| Providers | ✅ |
| Utilities | ✅ |
| Configuration | ✅ |
| Prompt Templates | ✅ |
| Export Logic | ✅ |
| Validation Logic | ✅ |

---

# Fixtures

Fixtures reduce duplicate setup code.

Example:

```python
@pytest.fixture
def sample_video():
    return "sample.mp4"
```

Advantages:

- Reusability
- Cleaner tests
- Consistent setup
- Easier maintenance

---

# Mocking

External dependencies should be mocked to isolate application logic.

Examples:

- AI Providers
- Whisper Models
- File System
- Network Requests
- Export Operations

Example:

```python
from unittest.mock import patch

@patch("services.audio_service.extract_audio")
def test_audio(mock_extract):
    mock_extract.return_value = True
```

---

# Continuous Integration

GitHub Actions automatically validates the project.

Workflow:

```
Push Code

↓

Install Dependencies

↓

Run Pytest

↓

Generate Results

↓

Pass / Fail
```

Benefits:

- Automated verification
- Early bug detection
- Consistent testing
- Reliable releases

---

# Writing New Tests

When adding a new module:

1. Create a matching test file inside `tests/`.
2. Use descriptive test names.
3. Test both successful and failure scenarios.
4. Mock external dependencies where appropriate.
5. Ensure tests are independent and repeatable.

Example naming convention:

```
module.py

↓

test_module.py
```

---

# Best Practices

✔ Write one test for one behavior.

✔ Keep tests independent.

✔ Use fixtures for reusable setup.

✔ Mock external services.

✔ Test expected failures.

✔ Avoid hard-coded paths.

✔ Keep test names descriptive.

✔ Run tests before every commit.

---

# Common Test Scenarios

Recommended scenarios include:

- Valid input
- Invalid input
- Missing files
- Empty responses
- Exception handling
- Provider failures
- Export failures
- Configuration errors
- Boundary conditions

---

# Troubleshooting

### Module Not Found

Install project dependencies:

```bash
pip install -r requirements.txt
```

---

### Import Errors

Verify that the virtual environment is activated.

---

### Failed Assertions

Check expected values and update assertions if application behavior has changed.

---

### Mock Failures

Confirm the correct import path is being patched.

---

### GitHub Actions Failure

Verify:

- Dependencies are listed in `requirements.txt`
- Test dependencies are listed in `requirements_test.txt`
- Workflow file is up to date
- Tests pass locally before pushing

---

# Related Documentation

- INSTALLATION.md
- PROJECT_STRUCTURE.md
- API_DOCUMENTATION.md
- PROVIDER_GUIDE.md
- TROUBLESHOOTING.md
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

⭐ High-quality software starts with reliable testing. Contributions to improve the test suite are always appreciated.