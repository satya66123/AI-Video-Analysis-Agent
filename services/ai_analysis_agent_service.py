"""
ai_analysis_service.py

AI Analysis Service

Responsibilities
----------------
- Generate AI analysis
- Save analysis
- Browse saved analyses
- Load analysis
- Delete analysis
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, List

from providers.provider_factory import ProviderFactory


class AIAnalysisService:

    ANALYSIS_FOLDER = "analysis"

    @classmethod
    def analyze(
        cls,
        provider_name: str,
        model_name: str,
        transcript: str,
        prompt: str,
    ) -> Dict:

        os.makedirs(
            cls.ANALYSIS_FOLDER,
            exist_ok=True,
        )

        provider = ProviderFactory.get_provider(
            provider_name
        )

        if provider is None:
            raise Exception(
                f"Provider '{provider_name}' not found."
            )

        full_prompt = f"""
You are an expert AI Video Analyzer.

Analyze ONLY the transcript below.
Do not use prior knowledge.
Do not invent facts.
If information is missing, state that it is not available.

{prompt}

Transcript
------------------------
{transcript}
------------------------
"""

        response = provider.generate(
            prompt=full_prompt,
            model=model_name,
        )

        return {
            "content": response,
            "provider": provider_name,
            "model": model_name,
            "analysis_type": prompt,
            "generated_at": datetime.now().isoformat(),
        }

    @classmethod
    def save_analysis(
        cls,
        filename: str,
        analysis_type: str,
        content: str,
    ) -> str:

        os.makedirs(
            cls.ANALYSIS_FOLDER,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        safe_type = (
            analysis_type.replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        output_file = os.path.join(
            cls.ANALYSIS_FOLDER,
            f"{filename}_{safe_type}_{timestamp}.md",
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:

            f.write(content)

        return output_file

    @classmethod
    def list_analysis(
        cls,
    ) -> List[Dict]:

        os.makedirs(
            cls.ANALYSIS_FOLDER,
            exist_ok=True,
        )

        files = []

        for filename in os.listdir(
            cls.ANALYSIS_FOLDER
        ):

            if not (
                filename.endswith(".md")
                or filename.endswith(".txt")
                or filename.endswith(".json")
            ):
                continue

            path = os.path.join(
                cls.ANALYSIS_FOLDER,
                filename,
            )

            files.append(
                {
                    "name": filename,
                    "path": path,
                    "size": os.path.getsize(path),
                    "modified": os.path.getmtime(path),
                }
            )

        files.sort(
            key=lambda x: x["modified"],
            reverse=True,
        )

        return files

    @classmethod
    def load_analysis(
        cls,
        filename: str,
    ) -> str:

        path = os.path.join(
            cls.ANALYSIS_FOLDER,
            filename,
        )

        if not os.path.exists(path):
            raise FileNotFoundError(path)

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            return f.read()

    @classmethod
    def delete_analysis(
        cls,
        filename: str,
    ) -> bool:

        path = os.path.join(
            cls.ANALYSIS_FOLDER,
            filename,
        )

        if os.path.exists(path):

            os.remove(path)

            return True

        return False

    @classmethod
    def analysis_exists(
        cls,
        filename: str,
    ) -> bool:

        path = os.path.join(
            cls.ANALYSIS_FOLDER,
            filename,
        )

        return os.path.exists(path)