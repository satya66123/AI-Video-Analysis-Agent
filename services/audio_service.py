import os

from moviepy.editor import VideoFileClip


class AudioService:

    AUDIO_FOLDER = "audio"

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