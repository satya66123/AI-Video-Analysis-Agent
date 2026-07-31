import json
from typing import Dict, Generator

import requests

from providers.base_provider import BaseProvider


class OllamaProvider(BaseProvider):
    """
    Ollama AI Provider
    """

    BASE_URL = "http://localhost:11434"

    def get_models(self) -> Dict:

        try:
            response = requests.get(
                f"{self.BASE_URL}/api/tags",
                timeout=10
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException:
            return {}

    def generate(
        self,
        prompt: str,
        model: str
    ) -> str:

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/api/generate",
                json=payload,
                timeout=300
            )

            response.raise_for_status()

            return response.json().get("response", "")

        except requests.exceptions.Timeout:
            return "Error: Request timed out."

        except requests.exceptions.ConnectionError:
            return "Error: Unable to connect to Ollama."

        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

    def generate_stream(
        self,
        prompt: str,
        model: str
    ) -> Generator[str, None, None]:

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/api/generate",
                json=payload,
                stream=True,
                timeout=300
            )

            response.raise_for_status()

            for line in response.iter_lines():

                if not line:
                    continue

                data = json.loads(line)

                yield data.get("response", "")

        except requests.exceptions.Timeout:
            yield "Error: Request timed out."

        except requests.exceptions.ConnectionError:
            yield "Error: Unable to connect to Ollama."

        except requests.exceptions.RequestException as e:
            yield f"Error: {str(e)}"

    def health_check(self) -> bool:

        try:
            response = requests.get(
                f"{self.BASE_URL}/api/tags",
                timeout=5
            )

            response.raise_for_status()

            return True

        except requests.exceptions.RequestException:
            return False