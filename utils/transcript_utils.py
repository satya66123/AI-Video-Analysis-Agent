import os


class TranscriptUtils:

    TRANSCRIPT_FOLDER = "transcripts"

    @classmethod
    def list_transcripts(cls):

        os.makedirs(
            cls.TRANSCRIPT_FOLDER,
            exist_ok=True
        )

        return sorted(
            os.listdir(cls.TRANSCRIPT_FOLDER),
            key=lambda x: os.path.getmtime(
                os.path.join(cls.TRANSCRIPT_FOLDER, x)
            ),
            reverse=True
        )

    @classmethod
    def rename_transcript(
            cls,
            old_name,
            new_name
    ):

        if not new_name.endswith(".txt"):
            new_name += ".txt"

        old_path = os.path.join(
            cls.TRANSCRIPT_FOLDER,
            old_name
        )

        new_path = os.path.join(
            cls.TRANSCRIPT_FOLDER,
            new_name
        )

        if os.path.exists(new_path):
            return False

        os.rename(
            old_path,
            new_path
        )

        return True

    @classmethod
    def get_total_statistics(cls):

        transcripts = cls.list_transcripts()

        total_words = 0
        total_characters = 0
        total_lines = 0

        for transcript in transcripts:
            text = cls.read_transcript(transcript)

            total_words += len(text.split())
            total_characters += len(text)
            total_lines += len(text.splitlines())

        return {
            "files": len(transcripts),
            "words": total_words,
            "characters": total_characters,
            "lines": total_lines
        }

    @classmethod
    def read_transcript(cls, filename):

        path = os.path.join(
            cls.TRANSCRIPT_FOLDER,
            filename
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    @classmethod
    def delete_transcript(cls, filename):

        path = os.path.join(
            cls.TRANSCRIPT_FOLDER,
            filename
        )

        if os.path.exists(path):
            os.remove(path)
            return True

        return False

    @classmethod
    def delete_all_transcripts(cls):

        transcripts = cls.list_transcripts()

        for transcript in transcripts:
            os.remove(
                os.path.join(
                    cls.TRANSCRIPT_FOLDER,
                    transcript
                )
            )