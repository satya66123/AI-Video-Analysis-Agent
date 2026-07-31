import os
from datetime import datetime

from providers.provider_factory import ProviderFactory


class AIChatService:
    """
    AI Chat Service

    Chat with video transcripts using any supported AI provider.
    """

    def __init__(self):
        self.chat_dir = "chat_history"
        os.makedirs(self.chat_dir, exist_ok=True)

    def build_prompt(self, transcript: str, history: list, question: str):
        """
        Build prompt with transcript and conversation history.
        """

        prompt = f"""
You are an AI Video Assistant.

Answer questions ONLY using the transcript below.

If the transcript does not contain the answer,
say:

"I couldn't find that information in the transcript."

-----------------------
VIDEO TRANSCRIPT
-----------------------

{transcript}

-----------------------
CHAT HISTORY
-----------------------
"""

        for chat in history:
            prompt += f"""
User: {chat['user']}
Assistant: {chat['assistant']}
"""

        prompt += f"""

-----------------------
CURRENT QUESTION
-----------------------

User: {question}

Assistant:
"""

        return prompt

    def ask(
            self,
            transcript,
            history,
            question,
            provider_name,
            model_name,
    ):
        provider = ProviderFactory.get_provider(provider_name)

        prompt = self.build_prompt(
            transcript,
            history,
            question,
        )

        response = provider.generate(
            prompt=prompt,
            model=model_name,
        )

        return response

    def save_chat(self, filename, history):
        path = os.path.join(self.chat_dir, filename)

        import json

        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

        return path

    def ask_stream(
            self,
            transcript,
            history,
            question,
            provider_name,
            model_name,
    ):
        provider = ProviderFactory.get_provider(provider_name)

        prompt = self.build_prompt(
            transcript,
            history,
            question,
        )

        return provider.generate_stream(
            prompt=prompt,
            model=model_name,
        )
