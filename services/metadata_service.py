from pathlib import Path
import cv2
from moviepy.audio.io.AudioFileClip import AudioFileClip


class MetadataService:

    @staticmethod
    def get_video_metadata(video_path: str):
        path = Path(video_path)

        cap = cv2.VideoCapture(video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        duration = frames / fps if fps else 0

        cap.release()

        return {
            "filename": path.name,
            "duration": f"{duration:.2f} sec",
            "fps": round(fps, 2),
            "resolution": f"{width} x {height}",
            "format": path.suffix,
            "size": f"{path.stat().st_size / (1024 * 1024):.2f} MB",
        }

    @staticmethod
    def get_audio_metadata(audio_path: str):
        path = Path(audio_path)

        try:
            clip = AudioFileClip(str(path))

            metadata = {
                "filename": path.name,
                "duration": f"{clip.duration:.2f} sec",
                "sample_rate": getattr(clip, "fps", "Unknown"),
                "channels": getattr(clip, "nchannels", "Unknown"),
                "format": path.suffix,
                "size": f"{path.stat().st_size / (1024 * 1024):.2f} MB",
            }

            clip.close()

            return metadata

        except Exception:
            return {
                "filename": path.name,
                "duration": "Unknown",
                "sample_rate": "Unknown",
                "channels": "Unknown",
                "format": path.suffix,
                "size": f"{path.stat().st_size / (1024 * 1024):.2f} MB",
            }