import os
import json
from pathlib import Path

from moviepy.editor import VideoFileClip


class AudioService:

    AUDIO_FOLDER = "audio"
    AUDIO_METADATA_FOLDER = Path("metadata/audio")

    @classmethod
    def ensure_metadata_folder(cls):

        cls.AUDIO_METADATA_FOLDER.mkdir(
            parents=True,
            exist_ok=True,
        )

    @classmethod
    def save_metadata(
            cls,
            filename: str,
            metadata: dict,
    ):

        cls.ensure_metadata_folder()

        path = (
                cls.AUDIO_METADATA_FOLDER
                / f"{Path(filename).stem}.json"
        )

        with open(
                path,
                "w",
                encoding="utf-8",
        ) as file:
            json.dump(
                metadata,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return path

    @classmethod
    def load_metadata(
            cls,
            filename: str,
    ):

        cls.ensure_metadata_folder()

        path = (
                cls.AUDIO_METADATA_FOLDER
                / f"{Path(filename).stem}.json"
        )

        if not path.exists():
            raise FileNotFoundError(path)

        with open(
                path,
                "r",
                encoding="utf-8",
        ) as file:
            return json.load(file)

    @classmethod
    def list_metadata(cls):

        cls.ensure_metadata_folder()

        files = []

        for file in sorted(
                cls.AUDIO_METADATA_FOLDER.glob("*.json")
        ):
            files.append(
                {
                    "name": file.name,
                    "path": str(file),
                    "size": file.stat().st_size,
                    "modified": file.stat().st_mtime,
                }
            )

        return files

    @classmethod
    def delete_metadata(
            cls,
            filename: str,
    ):

        path = (
                cls.AUDIO_METADATA_FOLDER
                / f"{Path(filename).stem}.json"
        )

        if path.exists():
            path.unlink()

            return True

        return False

    @classmethod
    def metadata_exists(
            cls,
            filename: str,
    ):

        return (
                cls.AUDIO_METADATA_FOLDER
                / f"{Path(filename).stem}.json"
        ).exists()

    @classmethod
    def create_metadata(
            cls,
            audio_path: str,
    ) -> dict:

        path = Path(audio_path)

        try:

            clip = VideoFileClip(audio_path)

            metadata = {

                "filename": path.name,

                "duration": f"{clip.duration:.2f} sec",

                "sample_rate": getattr(
                    clip.audio,
                    "fps",
                    "Unknown",
                ),

                "channels": getattr(
                    clip.audio,
                    "nchannels",
                    "Unknown",
                ),

                "format": path.suffix,

                "size": f"{path.stat().st_size / (1024 * 1024):.2f} MB",

            }

            clip.close()

        except Exception:

            metadata = {

                "filename": path.name,

                "duration": "Unknown",

                "sample_rate": "Unknown",

                "channels": "Unknown",

                "format": path.suffix,

                "size": f"{path.stat().st_size / (1024 * 1024):.2f} MB",

            }

        return metadata

    @classmethod
    def extract_audio(
        cls,
        video_path,
        progress_bar=None,
        status_text=None
    ):

        os.makedirs(
            cls.AUDIO_FOLDER,
            exist_ok=True
        )

        filename = os.path.splitext(
            os.path.basename(video_path)
        )[0]

        audio_path = os.path.join(
            cls.AUDIO_FOLDER,
            f"{filename}.mp3"
        )

        # Duplicate Detection
        if os.path.exists(audio_path):

            if progress_bar:
                progress_bar.progress(1.0)

            if status_text:
                status_text.warning(
                    "⚠ Audio already extracted."
                )

            video = VideoFileClip(video_path)


            return audio_path


        try:

            if progress_bar:
                progress_bar.progress(10)

            if status_text:
                status_text.info(
                    "Opening video..."
                )

            video = VideoFileClip(video_path)

            if progress_bar:
                progress_bar.progress(40)

            if status_text:
                status_text.info(
                    "Extracting audio..."
                )

            video.audio.write_audiofile(
                audio_path,
                logger=None
            )

            ##################################################
            # Create & Save Metadata
            ##################################################

            metadata = cls.create_metadata(
                audio_path,
            )

            cls.save_metadata(
                audio_path,
                metadata,
            )

            video.close()

            if progress_bar:
                progress_bar.progress(100)

            if status_text:
                status_text.success(
                    "✅ Audio extracted successfully."
                )
                return audio_path

        except Exception as e:

            if status_text:
                status_text.error(str(e))

            return None

    @classmethod
    def list_audio(cls):

        os.makedirs(
            cls.AUDIO_FOLDER,
            exist_ok=True
        )

        return sorted(
            os.listdir(cls.AUDIO_FOLDER)
        )

    @classmethod
    def delete_audio(
        cls,
        filename
    ):

        filepath = os.path.join(
            cls.AUDIO_FOLDER,
            filename
        )

        if os.path.exists(filepath):

            os.remove(filepath)

            return True

        return False