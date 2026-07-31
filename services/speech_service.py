import os
import whisper

from utils.audio_splitter import AudioSplitter


class SpeechService:

    TRANSCRIPT_FOLDER = "transcripts"

    _model = None
    _model_name = None

    @classmethod
    def load_model(cls, model_name="base"):

        if cls._model is None or cls._model_name != model_name:

            print(f"Loading Whisper Model: {model_name}")

            cls._model = whisper.load_model(model_name)
            cls._model_name = model_name

        return cls._model

    @classmethod
    def transcribe(
        cls,
        audio_path,
        progress_bar=None,
        status_text=None,
        model_name="base",
        chunk_minutes=5
    ):

        os.makedirs(
            cls.TRANSCRIPT_FOLDER,
            exist_ok=True
        )

        if not os.path.exists(audio_path):
            raise FileNotFoundError(audio_path)

        if os.path.getsize(audio_path) == 0:
            raise ValueError("Audio file is empty.")

        filename = os.path.splitext(
            os.path.basename(audio_path)
        )[0]

        transcript_path = os.path.join(
            cls.TRANSCRIPT_FOLDER,
            f"{filename}.txt"
        )

        # Duplicate Detection
        if os.path.exists(transcript_path):

            if progress_bar:
                progress_bar.progress(100)

            if status_text:
                status_text.warning(
                    "⚠ Transcript already exists."
                )

            with open(
                transcript_path,
                "r",
                encoding="utf-8"
            ) as f:

                return f.read()

        chunk_paths = []

        try:

            if progress_bar:
                progress_bar.progress(5)

            if status_text:
                status_text.info(
                    "Loading Whisper Model..."
                )

            model = cls.load_model(model_name)

            if progress_bar:
                progress_bar.progress(10)

            if status_text:
                status_text.info(
                    "Splitting Audio..."
                )

            chunk_paths = AudioSplitter.split_audio(
                audio_path,
                chunk_minutes
            )

            total_chunks = len(chunk_paths)

            if total_chunks == 0:
                raise Exception("No audio chunks created.")

            transcript_parts = []

            for index, chunk in enumerate(chunk_paths):

                current = index + 1

                if status_text:
                    status_text.info(
                        f"Transcribing Chunk {current} of {total_chunks}"
                    )

                print(
                    f"Chunk {current}/{total_chunks}"
                )

                result = model.transcribe(
                    chunk,
                    fp16=False,
                    verbose=False,
                    condition_on_previous_text=False
                )

                text = result.get(
                    "text",
                    ""
                ).strip()

                if text:
                    transcript_parts.append(text)

                percent = int(
                    10 +
                    (current / total_chunks) * 85
                )

                if progress_bar:
                    progress_bar.progress(percent)

            transcript = "\n\n".join(
                transcript_parts
            ).strip()

            if transcript == "":

                if status_text:
                    status_text.warning(
                        "⚠ No speech detected."
                    )

                return None

            if status_text:
                status_text.info(
                    "Saving Transcript..."
                )

            with open(
                transcript_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(transcript)

            AudioSplitter.cleanup(
                chunk_paths
            )

            if progress_bar:
                progress_bar.progress(100)

            if status_text:
                status_text.success(
                    "✅ Transcription Completed Successfully"
                )

            return transcript

        except Exception as e:

            try:
                AudioSplitter.cleanup(
                    chunk_paths
                )
            except:
                pass

            if progress_bar:
                progress_bar.progress(0)

            if status_text:
                status_text.error(
                    f"❌ {e}"
                )

            print(e)

            return None