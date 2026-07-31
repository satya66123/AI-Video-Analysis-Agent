import os
from typing import Generator, List

from openai import OpenAI

from providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    """
    OpenAI Provider
    """

    def __init__(self):

        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not found."
            )

        self.client = OpenAI(
            api_key=self.api_key
        )

    def get_models(self) -> List[str]:
        """
        Fetch available OpenAI models.
        """

        try:

            models = self.client.models.list()

            return sorted(
                [model.id for model in models.data]
            )

        except Exception:

            return []

    def generate(
        self,
        prompt: str,
        model: str
    ) -> str:
        """
        Generate a response using the OpenAI Responses API.
        """

        try:

            response = self.client.responses.create(
                model=model,
                input=prompt
            )

            return response.output_text

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
        Replace this with native OpenAI streaming
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
        Verify OpenAI connectivity.
        """

        try:

            self.client.models.list()

            return True

        except Exception:

            return False