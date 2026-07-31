from providers.ollama_provider import OllamaProvider
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider


class ProviderFactory:

    @staticmethod
    def get_provider(provider_name):

        providers = {
            "Ollama": OllamaProvider,
            "OpenAI": OpenAIProvider,
            "Anthropic": AnthropicProvider
        }

        provider = providers.get(provider_name)

        if provider is None:
            raise ValueError(f"Unsupported provider: {provider_name}")

        return provider()