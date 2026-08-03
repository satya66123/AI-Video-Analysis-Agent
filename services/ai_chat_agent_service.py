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
    def generate_chat_id(
            video_name: str,
    ) -> str:

        video_name = Path(video_name).stem

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        return f"{video_name}_{timestamp}"

    def create_chat(
            self,
            video_name: str,
    ):

        chat_id = self.generate_chat_id(
            video_name
        )

        self.save_chat(
            f"{chat_id}.json",
            [],
            status="Open",
        )

        return chat_id

    def list_video_chats(
            self,
            video_name: str,
    ):

        video_name = Path(video_name).stem

        chats = []

        for file in self.CHAT_FOLDER.glob("*.json"):

            if file.stem.startswith(
                    f"{video_name}_"
            ):
                chats.append(file)

        chats.sort(
            reverse=True,
        )

        return chats

    def chat_exists(
            self,
            chat_id: str,
    ):

        return (
                self.CHAT_FOLDER
                / f"{chat_id}.json"
        ).exists()

    def load_chat_by_id(
            self,
            chat_id: str,
    ):

        path = self.CHAT_FOLDER / f"{chat_id}.json"

        if not path.exists():
            return []

        with open(
                path,
                "r",
                encoding="utf-8",
        ) as file:

            data = json.load(file)

        if isinstance(
                data,
                list,
        ):
            return data

        return data.get(
            "history",
            [],
        )

    def save_chat_by_id(
            self,
            chat_id: str,
            history,
            status: str = "Open",
    ):

        return self.save_chat(
            f"{chat_id}.json",
            history,
            status,
        )

    def append_message(
            self,
            history,
            user,
            assistant,
    ):

        history.append(

            self.create_message(
                user,
                assistant,
            )

        )

        return history

    @staticmethod
    def build_prompt(
            transcript: str,
            history: List[Dict],
            question: str,
    ) -> str:

        question_lower = question.strip().lower()

        casual_messages = {

            "hi",
            "hello",
            "hey",
            "hii",
            "helo",
            "good morning",
            "good afternoon",
            "good evening",
            "good night",
            "bye",
            "good bye",
            "goodbye",
            "see you",
            "see you later",
            "thanks",
            "thank you",
            "thankyou",
            "ok",
            "okay",
            "how are you",
            "who are you",
            "what can you do",
            "nice",
            "great",
            "awesome",
        }

        ####################################################
        # Casual Conversation
        ####################################################

        if question_lower in casual_messages:
            return f"""
    You are a friendly AI Video Analysis Assistant.

    The user is having a normal conversation with you.

    DO NOT use or mention the video transcript.

    Respond naturally, politely and conversationally.

    User:
    {question}

    Assistant:
    """

        ####################################################
        # Video Question
        ####################################################

        prompt = f"""
    You are an AI Video Analysis Assistant.

    Your primary responsibility is answering questions about the uploaded video.

    Rules:

    1. Answer using ONLY the transcript below.
    2. If the answer exists in the transcript, answer clearly.
    3. If the answer is NOT available in the transcript, reply exactly:

    "I couldn't find that information in the transcript."

    4. Do not invent information.
    5. Do not guess.
    6. Do not answer from general knowledge.
    7. Ignore previous world knowledge unless the user is having a casual conversation.

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
    {item.get("user", "")}

    Assistant:
    {item.get("assistant", "")}
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
            status: str = "Open",
    ) -> Path:

        path = self.CHAT_FOLDER / filename

        chat_data = {

            "chat_id": Path(filename).stem,

            "video": Path(filename).stem,

            "status": status,

            "created_at": datetime.now().isoformat(),

            "history": history,

        }

        if status == "Closed":

            chat_data["closed_at"] = datetime.now().isoformat()

        else:

            chat_data["closed_at"] = None

        with open(
                path,
                "w",
                encoding="utf-8",
        ) as file:

            json.dump(
                chat_data,
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

            data = json.load(file)

        if isinstance(
                data,
                list,
        ):
            return data

        return data.get(
            "history",
            [],
        )





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