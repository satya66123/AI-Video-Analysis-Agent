import os
import uuid
import hashlib
import json
from pathlib import Path

import cv2


class VideoService:

    UPLOAD_FOLDER = "uploads"
    VIDEO_METADATA_FOLDER = Path("metadata/video")

    @classmethod
    def ensure_metadata_folder(cls):

        cls.VIDEO_METADATA_FOLDER.mkdir(
            parents=True,
            exist_ok=True,
        )

    @classmethod
    def create_metadata(
            cls,
            video_path: str,
    ):

        path = Path(video_path)

        cap = cv2.VideoCapture(video_path)

        fps = cap.get(
            cv2.CAP_PROP_FPS
        )

        frames = cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )

        width = int(
            cap.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            cap.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        duration = (
            frames / fps
            if fps
            else 0
        )

        cap.release()

        return {

            "filename": path.name,

            "duration": f"{duration:.2f} sec",

            "fps": round(fps, 2),

            "resolution": f"{width} x {height}",

            "format": path.suffix,

            "size": f"{path.stat().st_size / (1024 * 1024):.2f} MB",

        }

    @classmethod
    def save_metadata(
            cls,
            filename: str,
            metadata: dict,
    ):

        cls.ensure_metadata_folder()

        path = (
                cls.VIDEO_METADATA_FOLDER
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
                cls.VIDEO_METADATA_FOLDER
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

        ##################################################
        # Save Video Metadata
        ##################################################

        metadata = cls.create_metadata(
            filepath
        )

        cls.save_metadata(
            filepath,
            metadata,
        )

        return {
            "filepath": filepath,
            "filename": filename,
            "original_filename": uploaded_file.name,
            "size": uploaded_file.size,
        }

    @classmethod
    def delete_metadata(
            cls,
            filename: str,
    ):

        path = (
                cls.VIDEO_METADATA_FOLDER
                / f"{Path(filename).stem}.json"
        )

        if path.exists():
            path.unlink()

            return True

        return False

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