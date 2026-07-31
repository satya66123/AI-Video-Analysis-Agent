import os
from typing import Generator, List

import anthropic

from providers.base_provider import BaseProvider


class AnthropicProvider(BaseProvider):
    """
    Anthropic AI Provider
    """

    def __init__(self):

        self.api_key = os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not found."
            )

        self.client = anthropic.Anthropic(
            api_key=self.api_key
        )

    def get_models(self) -> List[str]:
        """
        Return supported Anthropic models.
        """

        return [
            "claude-opus-4.1",
            "claude-sonnet-4",
            "claude-3.7-sonnet",
            "claude-3.5-sonnet",
            "claude-3.5-haiku"
        ]

    def generate(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> str:
        """
        Generate a response using Anthropic.
        """

        try:

            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.content[0].text

        except Exception as e:

            return f"Error: {str(e)}"

    def generate_stream(
        self,
        prompt: str,
        model: str
    ) -> Generator[str, None, None]:
        """
        Streaming response.

        Currently falls back to normal generation.
        Replace this with Anthropic native streaming
        if streaming is required in the future.
        """

        try:

            response = self.generate(
                prompt=prompt,
                model=model
            )

            yield response

        except Exception as e:

            yield f"Error: {str(e)}"

    def health_check(self) -> bool:
        """
        Verify Anthropic connectivity.
        """

        try:

            self.client.messages.create(
                model="claude-3.5-haiku",
                max_tokens=10,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello"
                    }
                ]
            )

            return True

        except Exception:

            return False