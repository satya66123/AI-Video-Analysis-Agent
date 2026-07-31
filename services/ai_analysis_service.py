import os
from datetime import datetime

from providers.provider_factory import ProviderFactory


class AIAnalysisService:

    ANALYSIS_FOLDER = "analysis"

    @classmethod
    def analyze(
        cls,
        provider_name,
        model_name,
        transcript,
        prompt
    ):

        os.makedirs(
            cls.ANALYSIS_FOLDER,
            exist_ok=True
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

        Transcript:
        --------------------
        {transcript}
        --------------------
        """

        response = provider.generate(
            prompt=full_prompt,
            model=model_name
        )

        return response

    @classmethod
    def save_analysis(
        cls,
        filename,
        analysis_type,
        content
    ):

        os.makedirs(
            cls.ANALYSIS_FOLDER,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_file = os.path.join(
            cls.ANALYSIS_FOLDER,
            f"{filename}_{analysis_type}_{timestamp}.md"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        return output_file