# 🤖 AI Video Analyzer - Provider Guide

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/Streamlit-1.46+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

<img src="https://img.shields.io/badge/Ollama-Supported-black?style=for-the-badge"/>

<img src="https://img.shields.io/badge/OpenAI-Supported-10A37F?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Anthropic-Supported-5A4FCF?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge"/>

</p>

---

# Table of Contents

- Introduction
- Provider Architecture
- Supported Providers
- Provider Factory
- Base Provider
- Ollama Provider
- OpenAI Provider
- Anthropic Provider
- Model Management
- Provider Selection
- Error Handling
- Adding a New Provider
- Best Practices

---

# Introduction

AI Video Analyzer supports multiple AI providers through a common abstraction layer.

Instead of writing provider-specific logic throughout the application, all AI communication is centralized inside the **providers** package. This design simplifies maintenance and allows new providers to be added with minimal code changes.

---

# Provider Architecture

```
                AIAnalysisService
                        │
                        ▼
                ProviderFactory
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
 OllamaProvider   OpenAIProvider   AnthropicProvider
        │               │                │
        ▼               ▼                ▼
 Local Models     OpenAI API      Anthropic API
```

---

# Supported Providers

| Provider | Type | Internet Required |
|-----------|------|------------------|
| Ollama | Local | ❌ |
| OpenAI | Cloud | ✅ |
| Anthropic | Cloud | ✅ |

---

# Base Provider

Every provider inherits from a common base interface.

Example:

```python
class BaseProvider:

    def generate(self, model, prompt):
        raise NotImplementedError
```

Benefits:

- Common API
- Consistent implementation
- Easy testing
- Provider interchangeability

---

# Provider Factory

The Provider Factory creates the requested provider at runtime.

Example flow:

```
User selects Provider

↓

ProviderFactory

↓

Creates Provider Object

↓

Returns Provider Instance
```

Example:

```python
provider = ProviderFactory.get_provider(provider_name)
```

Advantages:

- Centralized creation
- No duplicate initialization
- Cleaner application architecture

---

# Ollama Provider

The Ollama provider enables local AI inference without requiring external API keys.

### Responsibilities

- Connect to Ollama
- Detect installed models
- Generate responses
- Handle local inference errors

### Example Workflow

```
Prompt

↓

Ollama Provider

↓

Ollama Server

↓

Selected Model

↓

Generated Response
```

### Recommended Models

- llama3.1
- qwen2.5
- qwen3
- gemma3
- mistral
- phi3
- deepseek-coder

---

# OpenAI Provider

The OpenAI provider communicates with OpenAI models using an API key.

Responsibilities:

- Authentication
- Request creation
- Response parsing
- Error handling

Typical process:

```
Prompt

↓

OpenAI Provider

↓

OpenAI API

↓

Generated Response
```

---

# Anthropic Provider

The Anthropic provider integrates Claude models into the application.

Responsibilities:

- API communication
- Request validation
- Response formatting
- Exception handling

---

# Model Management

Models are selected dynamically based on the chosen provider.

Example:

```
Select Provider

↓

Load Available Models

↓

User Selects Model

↓

Generate Response
```

Recommended behavior:

- Display only compatible models.
- Validate model availability before generation.
- Handle unavailable models gracefully.

---

# Provider Selection

Users can switch providers from the application interface.

Example workflow:

```
Settings

↓

Select Provider

↓

Choose Model

↓

Generate Analysis
```

The service layer remains unchanged regardless of the selected provider.

---

# Error Handling

Common provider-related errors include:

| Error | Recommended Action |
|--------|--------------------|
| API Key Missing | Prompt user to configure `.env` |
| Model Not Found | Select another available model |
| Ollama Server Offline | Start `ollama serve` |
| Network Failure | Retry request |
| Rate Limit | Wait and retry |
| Timeout | Display informative message |

---

# Configuration

Cloud providers require environment variables.

Example:

```env
OPENAI_API_KEY=your_api_key

ANTHROPIC_API_KEY=your_api_key
```

Ollama does not require API credentials.

---

# Adding a New Provider

Steps:

1. Create a new provider class.

2. Inherit `BaseProvider`.

3. Implement required methods.

4. Register the provider in `ProviderFactory`.

5. Add unit tests.

6. Update documentation.

Example:

```
providers/

└── custom_provider.py
```

---

# Best Practices

✔ Use the provider abstraction instead of direct API calls.

✔ Keep provider classes focused on communication logic only.

✔ Validate provider availability before generating responses.

✔ Store secrets in environment variables.

✔ Write tests for every new provider implementation.

✔ Log provider-specific errors for easier debugging.

---

# Provider Comparison

| Feature | Ollama | OpenAI | Anthropic |
|----------|:------:|:------:|:---------:|
| Local Execution | ✅ | ❌ | ❌ |
| Internet Required | ❌ | ✅ | ✅ |
| API Key Required | ❌ | ✅ | ✅ |
| Offline Support | ✅ | ❌ | ❌ |
| Easy Setup | ✅ | ✅ | ✅ |

---

# Future Enhancements

Possible provider improvements:

- Streaming responses
- Automatic provider fallback
- Multi-provider orchestration
- Provider benchmarking
- Response caching
- Cost estimation
- Token usage dashboard
- Model recommendation system

---

# Related Documentation

- INSTALLATION.md
- API_DOCUMENTATION.md
- ARCHITECTURE.md
- SYSTEM_DESIGN.md
- CONFIGURATION.md
- TESTING.md
- README.md

---

# 👨‍💻 Author

**Nekkanti Satya Srinath**

GitHub Repository

https://github.com/satya66123/AI-Video-Analyzer

---

## License

This project is licensed under the **MIT License**.

---

**Version:** v1.0.0

⭐ Thank you for using **AI Video Analyzer**. Contributions and suggestions are always welcome.