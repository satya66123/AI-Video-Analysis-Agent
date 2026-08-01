# Provider Guide

![Providers](https://img.shields.io/badge/Providers-Guide-blue)
![Architecture](https://img.shields.io/badge/Architecture-Provider%20Layer-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)

This guide explains how AI providers are integrated into the AI Video Analysis Agent.

---

# Overview

The Provider layer abstracts different Large Language Model (LLM) providers behind a common interface. This allows the application to switch between providers without changing the business logic.

Currently supported providers:

- Ollama
- OpenAI
- Anthropic

---

# Provider Architecture

```
Streamlit UI
      │
      ▼
Agents
      │
      ▼
Services
      │
      ▼
ProviderFactory
      │
      ▼
Provider
      │
      ▼
AI Model
```

---

# Provider Components

```
providers/

base_provider.py
provider_factory.py
ollama_provider.py
openai_provider.py
anthropic_provider.py
```

---

# Base Provider

The Base Provider defines the common interface that every provider must implement.

Typical responsibilities:

- Generate AI responses
- Stream AI responses
- Handle provider-specific communication

---

# Provider Factory

The Provider Factory is responsible for returning the correct provider instance.

Example:

```
User selects provider
        │
        ▼
ProviderFactory
        │
        ▼
Returns Provider Instance
```

Benefits:

- Centralized provider management
- Easy provider switching
- Simplified application code

---

# Ollama Provider

Purpose:

Provides local AI model support using Ollama.

Features:

- Local inference
- Multiple models
- Offline support
- Streaming responses

Typical workflow:

```
Application
     │
     ▼
Ollama Provider
     │
     ▼
Ollama Server
     │
     ▼
AI Response
```

---

# OpenAI Provider

Purpose:

Connects the application to OpenAI models.

Features:

- Cloud-based AI
- Chat completion
- Streaming support

Requirements:

- OpenAI API Key

---

# Anthropic Provider

Purpose:

Connects the application to Anthropic models.

Features:

- Claude models
- Streaming responses
- Cloud AI

Requirements:

- Anthropic API Key

---

# Provider Selection

The user selects:

- Provider
- Model

The application automatically loads the selected provider through the Provider Factory.

Example:

```
Provider

Ollama

Model

llama3.1
```

---

# Provider Workflow

```
User Request
      │
      ▼
Chat / Analysis Service
      │
      ▼
ProviderFactory
      │
      ▼
Selected Provider
      │
      ▼
Generate Response
      │
      ▼
Return Result
```

---

# Features

Supported features include:

- AI Analysis
- AI Chat
- Prompt Processing
- Response Generation
- Streaming Responses
- Multi-model Support

---

# Adding a New Provider

To integrate another AI provider:

1. Create a new provider class.
2. Implement the Base Provider interface.
3. Register the provider in `provider_factory.py`.
4. Add provider configuration.
5. Test the provider integration.

---

# Benefits of Provider Abstraction

- Modular design
- Easy maintenance
- Easy provider replacement
- Consistent API
- Scalable architecture
- Reusable code

---

# Error Handling

Providers should handle:

- Invalid API keys
- Network failures
- Missing models
- Timeout errors
- Invalid responses

Errors are propagated back to the service layer for appropriate handling.

---

# Configuration

Typical provider configuration includes:

- Provider name
- Model name
- API key (if required)
- Temperature
- Maximum tokens

---

# Supported Operations

Providers support:

- Generate AI response
- Stream AI response
- Model selection
- Prompt execution

---

# Summary

The Provider layer enables the AI Video Analysis Agent to work with multiple AI backends through a unified interface. By separating provider-specific logic from the rest of the application, the project remains modular, extensible, and easy to maintain while allowing users to choose the AI provider and model that best fits their needs.