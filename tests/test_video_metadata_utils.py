import os
from unittest.mock import MagicMock, patch

import cv2

from utils.video_metadata import VideoMetadata


class TestVideoMetadataUtils:

    @patch("utils.video_metadata.cv2.VideoCapture")
    def test_get_metadata_capture_not_opened(
        self,
        mock_capture_class,
    ):
        capture = MagicMock()
        capture.isOpened.return_value = False

        mock_capture_class.return_value = capture

        result = VideoMetadata.get_metadata(
            "video.mp4"
        )

        assert result is None

    @patch("utils.video_metadata.os.path.getsize")
    @patch("utils.video_metadata.cv2.VideoCapture")
    def test_get_metadata_success(
        self,
        mock_capture_class,
        mock_getsize,
    ):
        capture = MagicMock()

        capture.isOpened.return_value = True

        values = {
            cv2.CAP_PROP_FRAME_WIDTH: 1920,
            cv2.CAP_PROP_FRAME_HEIGHT: 1080,
            cv2.CAP_PROP_FPS: 30.0,
            cv2.CAP_PROP_FRAME_COUNT: 300,
            cv2.CAP_PROP_FOURCC: (
                ord("X")
                | (ord("V") << 8)
                | (ord("I") << 16)
                | (ord("D") << 24)
            ),
        }

        capture.get.side_effect = (
            lambda prop: values[prop]
        )

        mock_capture_class.return_value = capture

        mock_getsize.return_value = 50 * 1024 * 1024

        result = VideoMetadata.get_metadata(
            "videos/sample.mp4"
        )

        assert result == {
            "filename": "sample.mp4",
            "width": 1920,
            "height": 1080,
            "resolution": "1920 x 1080",
            "fps": 30.0,
            "frames": 300,
            "duration": 10.0,
            "codec": "XVID",
            "file_size_mb": 50.0,
        }

        capture.release.assert_called_once()

    @patch("utils.video_metadata.os.path.getsize")
    @patch("utils.video_metadata.cv2.VideoCapture")
    def test_get_metadata_zero_fps(
        self,
        mock_capture_class,
        mock_getsize,
    ):
        capture = MagicMock()

        capture.isOpened.return_value = True

        values = {
            cv2.CAP_PROP_FRAME_WIDTH: 1280,
            cv2.CAP_PROP_FRAME_HEIGHT: 720,
            cv2.CAP_PROP_FPS: 0,
            cv2.CAP_PROP_FRAME_COUNT: 250,
            cv2.CAP_PROP_FOURCC: (
                ord("M")
                | (ord("P") << 8)
                | (ord("4") << 16)
                | (ord("V") << 24)
            ),
        }

        capture.get.side_effect = (
            lambda prop: values[prop]
        )

        mock_capture_class.return_value = capture

        mock_getsize.return_value = 10 * 1024 * 1024

        result = VideoMetadata.get_metadata(
            "video.mp4"
        )

        assert result["duration"] == 0
        assert result["fps"] == 0
        assert result["codec"] == "MP4V"

        capture.release.assert_called_once()

    @patch("utils.video_metadata.os.path.getsize")
    @patch("utils.video_metadata.cv2.VideoCapture")
    def test_get_metadata_rounding(
        self,
        mock_capture_class,
        mock_getsize,
    ):
        capture = MagicMock()

        capture.isOpened.return_value = True

        values = {
            cv2.CAP_PROP_FRAME_WIDTH: 640,
            cv2.CAP_PROP_FRAME_HEIGHT: 480,
            cv2.CAP_PROP_FPS: 29.976,
            cv2.CAP_PROP_FRAME_COUNT: 299,
            cv2.CAP_PROP_FOURCC: (
                ord("A")
                | (ord("V") << 8)
                | (ord("C") << 16)
                | (ord("1") << 24)
            ),
        }

        capture.get.side_effect = (
            lambda prop: values[prop]
        )

        mock_capture_class.return_value = capture

        mock_getsize.return_value = int(
            5.55 * 1024 * 1024
        )

        result = VideoMetadata.get_metadata(
            "movie.mp4"
        )

        assert result["fps"] == round(29.976, 2)
        assert result["duration"] == round(
            299 / 29.976,
            2,
        )
        assert result["file_size_mb"] == round(
            int(5.55 * 1024 * 1024) / (1024 * 1024),
            2,
        )

        capture.release.assert_called_once()