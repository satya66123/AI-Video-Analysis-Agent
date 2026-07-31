from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from providers.provider_factory import ProviderFactory


class AIChatService:
    """
    AI Chat Service

    Responsible for:
    - Building prompts
    - Asking AI providers
    - Streaming responses
    - Managing chat history
    """

    CHAT_FOLDER = Path("chat_history")

    def __init__(self):

        self.CHAT_FOLDER.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def build_prompt(
            transcript: str,
        history: List[Dict],
        question: str,
    ) -> str:
        """
        Build prompt using transcript,
        previous conversation and question.
        """

        prompt = f"""
You are an AI Video Assistant.

Answer ONLY using the transcript below.

If the transcript does not contain the answer,
reply exactly:

"I couldn't find that information in the transcript."

--------------------------------------------------
VIDEO TRANSCRIPT
--------------------------------------------------

{transcript}

--------------------------------------------------
CHAT HISTORY
--------------------------------------------------
"""

        for item in history:

            prompt += f"""

User:
{item.get("user","")}

Assistant:
{item.get("assistant","")}
"""

        prompt += f"""

--------------------------------------------------
CURRENT QUESTION
--------------------------------------------------

User:
{question}

Assistant:
"""

        return prompt

    def ask(
        self,
        transcript: str,
        history: List[Dict],
        question: str,
        provider_name: str,
        model_name: str,
    ) -> str:

        provider = ProviderFactory.get_provider(
            provider_name
        )

        if provider is None:
            raise ValueError(
                f"Provider '{provider_name}' not found."
            )

        prompt = self.build_prompt(
            transcript,
            history,
            question,
        )

        return provider.generate(
            prompt=prompt,
            model=model_name,
        )

    def ask_stream(
        self,
        transcript: str,
        history: List[Dict],
        question: str,
        provider_name: str,
        model_name: str,
    ):

        provider = ProviderFactory.get_provider(
            provider_name
        )

        if provider is None:
            raise ValueError(
                f"Provider '{provider_name}' not found."
            )

        prompt = self.build_prompt(
            transcript,
            history,
            question,
        )

        return provider.generate_stream(
            prompt=prompt,
            model=model_name,
        )

    def save_chat(
        self,
        filename: str,
        history: List[Dict],
    ) -> Path:

        path = self.CHAT_FOLDER / filename

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return path

    def load_chat(
        self,
        filename: str,
    ) -> List[Dict]:

        path = self.CHAT_FOLDER / filename

        if not path.exists():
            return []

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)



    CHAT_FOLDER = Path("chat_history")

    @classmethod
    def list_chats(cls):
            cls.CHAT_FOLDER.mkdir(
                parents=True,
                exist_ok=True,
            )

            return sorted(
                cls.CHAT_FOLDER.glob("*.json")
            )

    def delete_chat(
        self,
        filename: str,
    ) -> bool:

        path = self.CHAT_FOLDER / filename

        if path.exists():
            path.unlink()
            return True

        return False

    def clear_chat(self) -> None:

        for file in self.CHAT_FOLDER.glob("*.json"):
            file.unlink()

    @staticmethod
    def create_message(
        user: str,
        assistant: str,
    ) -> Dict:

        return {
            "user": user,
            "assistant": assistant,
            "timestamp": datetime.now().isoformat(),
        }