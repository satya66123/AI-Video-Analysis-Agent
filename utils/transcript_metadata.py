import os
from datetime import datetime


class TranscriptMetadata:

    @staticmethod
    def get_metadata(file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        words = len(text.split())

        characters = len(text)

        lines = len(text.splitlines())

        reading_minutes = max(
            1,
            round(words / 200)
        )

        size_kb = round(
            os.path.getsize(file_path) / 1024,
            2
        )

        created = datetime.fromtimestamp(
            os.path.getctime(file_path)
        )

        return {

            "Words": words,

            "Characters": characters,

            "Lines": lines,

            "Reading Time": f"{reading_minutes} min",

            "Size": f"{size_kb} KB",

            "Created": created.strftime("%d-%m-%Y %H:%M")

        }