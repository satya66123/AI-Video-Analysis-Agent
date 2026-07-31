"""
speech_service.py

Speech Service

Responsibilities
----------------
- Load Whisper model
- Split long audio into chunks
- Transcribe audio
- Save transcripts
- Detect duplicate transcripts
- Manage transcript files
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

import whisper

from utils.audio_splitter import AudioSplitter


class SpeechService:

    TRANSCRIPT_FOLDER = "transcripts"

    _model = None
    _model_name = None

    @classmethod
    def load_model(
        cls,
        model_name: str = "base",
    ):

        if (
            cls._model is None
            or cls._model_name != model_name
        ):

            print(
                f"Loading Whisper Model: {model_name}"
            )

            cls._model = whisper.load_model(
                model_name
            )

            cls._model_name = model_name

        return cls._model

    @classmethod
    def transcribe(
        cls,
        audio_path: str,
        progress_bar=None,
        status_text=None,
        model_name: str = "base",
        chunk_minutes: int = 5,
    ) -> Optional[Dict]:

        os.makedirs(
            cls.TRANSCRIPT_FOLDER,
            exist_ok=True,
        )

        if not os.path.exists(audio_path):
            raise FileNotFoundError(audio_path)

        if os.path.getsize(audio_path) == 0:
            raise ValueError(
                "Audio file is empty."
            )

        filename = os.path.splitext(
            os.path.basename(audio_path)
        )[0]

        transcript_path = os.path.join(
            cls.TRANSCRIPT_FOLDER,
            f"{filename}.txt",
        )

        # Duplicate detection
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
                encoding="utf-8",
            ) as f:

                transcript = f.read()

            return {
                "text": transcript,
                "path": transcript_path,
                "model": model_name,
                "chunks": 0,
                "word_count": len(
                    transcript.split()
                ),
                "character_count": len(
                    transcript
                ),
            }

        chunk_paths = []

        try:

            if progress_bar:
                progress_bar.progress(5)

            if status_text:
                status_text.info(
                    "Loading Whisper Model..."
                )

            model = cls.load_model(
                model_name
            )

            if progress_bar:
                progress_bar.progress(10)

            if status_text:
                status_text.info(
                    "Splitting Audio..."
                )

            chunk_paths = AudioSplitter.split_audio(
                audio_path,
                chunk_minutes,
            )

            total_chunks = len(
                chunk_paths
            )

            if total_chunks == 0:
                raise RuntimeError(
                    "No audio chunks created."
                )

            transcript_parts = []

            for index, chunk in enumerate(
                chunk_paths
            ):

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
                    condition_on_previous_text=False,
                )

                text = result.get(
                    "text",
                    "",
                ).strip()

                if text:
                    transcript_parts.append(
                        text
                    )

                percent = int(
                    10
                    + (
                        current
                        / total_chunks
                    )
                    * 85
                )

                if progress_bar:
                    progress_bar.progress(
                        percent
                    )

            transcript = "\n\n".join(
                transcript_parts
            ).strip()

            if not transcript:

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
                encoding="utf-8",
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

            return {
                "text": transcript,
                "path": transcript_path,
                "model": model_name,
                "chunks": total_chunks,
                "word_count": len(
                    transcript.split()
                ),
                "character_count": len(
                    transcript
                ),
            }

        except Exception as e:

            try:
                AudioSplitter.cleanup(
                    chunk_paths
                )
            except Exception:
                pass

            if progress_bar:
                progress_bar.progress(0)

            if status_text:
                status_text.error(
                    f"❌ {e}"
                )

            print(e)

            return None

    @classmethod
    def list_transcripts(
        cls,
    ) -> List[Dict]:

        os.makedirs(
            cls.TRANSCRIPT_FOLDER,
            exist_ok=True,
        )

        files = []

        for filename in os.listdir(
            cls.TRANSCRIPT_FOLDER
        ):

            if not filename.endswith(
                ".txt"
            ):
                continue

            path = os.path.join(
                cls.TRANSCRIPT_FOLDER,
                filename,
            )

            files.append(
                {
                    "name": filename,
                    "path": path,
                    "size": os.path.getsize(
                        path
                    ),
                    "modified": os.path.getmtime(
                        path
                    ),
                }
            )

        files.sort(
            key=lambda x: x["modified"],
            reverse=True,
        )

        return files

    @classmethod
    def load_transcript(
        cls,
        filename: str,
    ) -> str:

        path = os.path.join(
            cls.TRANSCRIPT_FOLDER,
            filename,
        )

        if not os.path.exists(path):
            raise FileNotFoundError(
                path
            )

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            return f.read()

    @classmethod
    def delete_transcript(
        cls,
        filename: str,
    ) -> bool:

        path = os.path.join(
            cls.TRANSCRIPT_FOLDER,
            filename,
        )

        if os.path.exists(path):

            os.remove(path)

            return True

        return False

    @classmethod
    def transcript_exists(
        cls,
        filename: str,
    ) -> bool:

        path = os.path.join(
            cls.TRANSCRIPT_FOLDER,
            filename,
        )

        return os.path.exists(path)