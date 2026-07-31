from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Abstract base class for all AI providers.
    """

    @abstractmethod
    def generate(self, prompt: str, model: str) -> str:
        """
        Generate a response from the AI model.
        """
        pass

    def generate_stream(self, prompt: str, model: str):
        """
        Optional streaming support.

        Providers that do not implement streaming
        automatically fall back to normal generation.
        """
        yield self.generate(prompt, model)

    @abstractmethod
    def health_check(self) -> bool:
        """
        Check whether the provider is available.
        """
        pass