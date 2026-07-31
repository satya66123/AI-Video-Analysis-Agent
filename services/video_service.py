import os
import uuid
import hashlib


class VideoService:

    UPLOAD_FOLDER = "uploads"

    @classmethod
    def save_video(
        cls,
        uploaded_file,
        progress_bar=None,
        status_text=None
    ):

        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)

        extension = os.path.splitext(uploaded_file.name)[1]
        filename = f"{uuid.uuid4()}{extension}"

        filepath = os.path.join(
            cls.UPLOAD_FOLDER,
            filename
        )

        uploaded_file.seek(0)

        total_size = uploaded_file.size
        bytes_written = 0
        chunk_size = 1024 * 1024  # 1 MB

        with open(filepath, "wb") as f:

            while True:

                chunk = uploaded_file.read(chunk_size)

                if not chunk:
                    break

                f.write(chunk)

                bytes_written += len(chunk)

                if progress_bar:

                    progress = min(
                        bytes_written / total_size,
                        1.0
                    )

                    progress_bar.progress(progress)

                    if status_text:

                        percentage = int(progress * 100)

                        uploaded_mb = bytes_written / (1024 * 1024)
                        total_mb = total_size / (1024 * 1024)

                        status_text.info(
                            f"Uploading... {percentage}% "
                            f"({uploaded_mb:.2f} MB / {total_mb:.2f} MB)"
                        )

        uploaded_file.seek(0)

        if progress_bar:
            progress_bar.progress(1.0)

        if status_text:
            status_text.success(
                "✅ Upload Complete (100%)"
            )

        return filepath

    @classmethod
    def list_videos(cls):

        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)

        return sorted(os.listdir(cls.UPLOAD_FOLDER))

    @classmethod
    def delete_video(cls, filename):

        filepath = os.path.join(
            cls.UPLOAD_FOLDER,
            filename
        )

        if os.path.exists(filepath):

            os.remove(filepath)

            return True

        return False

    @classmethod
    def calculate_file_hash(cls, file):

        sha256 = hashlib.sha256()

        file.seek(0)

        while True:

            chunk = file.read(1024 * 1024)

            if not chunk:
                break

            sha256.update(chunk)

        file.seek(0)

        return sha256.hexdigest()

    @classmethod
    def calculate_saved_file_hash(cls, filepath):

        sha256 = hashlib.sha256()

        with open(filepath, "rb") as f:

            while True:

                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    @classmethod
    def is_duplicate(cls, uploaded_file):

        uploaded_hash = cls.calculate_file_hash(
            uploaded_file
        )

        videos = cls.list_videos()

        for video in videos:

            filepath = os.path.join(
                cls.UPLOAD_FOLDER,
                video
            )

            saved_hash = cls.calculate_saved_file_hash(
                filepath
            )

            if uploaded_hash == saved_hash:
                return True

        return False