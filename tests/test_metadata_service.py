from unittest.mock import MagicMock, patch

from services.metadata_service import MetadataService


class TestMetadataService:

    @patch("services.metadata_service.cv2.VideoCapture")
    @patch("services.metadata_service.Path.stat")
    def test_get_video_metadata(
        self,
        mock_stat,
        mock_capture,
    ):
        stat = MagicMock()
        stat.st_size = 1048576

        mock_stat.return_value = stat

        cap = MagicMock()

        cap.get.side_effect = [
            30,
            300,
            1920,
            1080,
        ]

        mock_capture.return_value = cap

        result = MetadataService.get_video_metadata(
            "sample.mp4"
        )

        assert result["filename"] == "sample.mp4"
        assert result["duration"] == "10.00 sec"
        assert result["fps"] == 30
        assert result["resolution"] == "1920 x 1080"
        assert result["format"] == ".mp4"
        assert result["size"] == "1.00 MB"

        cap.release.assert_called_once()

    @patch("services.metadata_service.AudioFileClip")
    @patch("services.metadata_service.Path.stat")
    def test_get_audio_metadata(
        self,
        mock_stat,
        mock_clip,
    ):
        stat = MagicMock()
        stat.st_size = 2097152

        mock_stat.return_value = stat

        clip = MagicMock()

        clip.duration = 15.25
        clip.fps = 44100
        clip.nchannels = 2

        mock_clip.return_value = clip

        result = MetadataService.get_audio_metadata(
            "audio.mp3"
        )

        assert result["filename"] == "audio.mp3"
        assert result["duration"] == "15.25 sec"
        assert result["sample_rate"] == 44100
        assert result["channels"] == 2
        assert result["format"] == ".mp3"
        assert result["size"] == "2.00 MB"

        clip.close.assert_called_once()

    @patch("services.metadata_service.AudioFileClip")
    @patch("services.metadata_service.Path.stat")
    def test_get_audio_metadata_exception(
        self,
        mock_stat,
        mock_clip,
    ):
        stat = MagicMock()
        stat.st_size = 1048576

        mock_stat.return_value = stat

        mock_clip.side_effect = Exception()

        result = MetadataService.get_audio_metadata(
            "audio.mp3"
        )

        assert result == {
            "filename": "audio.mp3",
            "duration": "Unknown",
            "sample_rate": "Unknown",
            "channels": "Unknown",
            "format": ".mp3",
            "size": "1.00 MB",
        }