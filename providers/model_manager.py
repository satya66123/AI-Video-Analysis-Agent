class ModelManager:

    OLLAMA_MODELS = [
        "qwen2.5:1.5b",      # Default model
        "llama3.1:latest",
        "qwen3:latest",
        "gemma3:4b",
        "gemma2:2b",
        "mistral:latest",
        "phi3:latest",
        "deepseek-coder:latest",
        "translategemma:12b"
    ]

    OPENAI_MODELS = [
        "gpt-5",             # Default model
        "gpt-5-mini",
        "gpt-5-nano",
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4o",
        "gpt-4o-mini"
    ]

    ANTHROPIC_MODELS = [
        "claude-opus-4.1",   # Default model
        "claude-sonnet-4",
        "claude-3.7-sonnet",
        "claude-3.5-sonnet",
        "claude-3.5-haiku"
    ]

    @classmethod
    def get_models(cls, provider):

        if provider == "Ollama":
            return cls.OLLAMA_MODELS

        elif provider == "OpenAI":
            return cls.OPENAI_MODELS

        elif provider == "Anthropic":
            return cls.ANTHROPIC_MODELS

        return []