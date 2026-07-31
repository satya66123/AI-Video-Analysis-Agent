import os
import cv2


class VideoMetadata:

    @staticmethod
    def get_metadata(video_path):

        capture = cv2.VideoCapture(video_path)

        if not capture.isOpened():
            return None

        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

        duration = 0
        if fps > 0:
            duration = frame_count / fps

        fourcc = int(capture.get(cv2.CAP_PROP_FOURCC))

        codec = "".join([
            chr((fourcc >> 8 * i) & 0xFF)
            for i in range(4)
        ])

        capture.release()

        return {
            "filename": os.path.basename(video_path),
            "width": width,
            "height": height,
            "resolution": f"{width} x {height}",
            "fps": round(fps, 2),
            "frames": frame_count,
            "duration": round(duration, 2),
            "codec": codec.strip(),
            "file_size_mb": round(
                os.path.getsize(video_path) / (1024 * 1024),
                2
            ),
        }