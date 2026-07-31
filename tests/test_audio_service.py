import os
from unittest.mock import MagicMock, patch

from services.audio_agent_service import AudioService


class TestAudioService:

    @patch("services.audio_service.os.makedirs")
    @patch("services.audio_service.os.path.exists")
    def test_extract_audio_duplicate(
        self,
        mock_exists,
        mock_makedirs,
    ):




        video_path = os.path.join(
            "uploads",
            "video.mp4",
        )







    @patch("services.audio_service.VideoFileClip")
    @patch("services.audio_service.os.path.exists")
    @patch("services.audio_service.os.makedirs")
    def test_extract_audio_success(
        self,
        mock_makedirs,
        mock_exists,
        mock_clip,
    ):






        expected = os.path.join(
            "audio",
            "video.mp3",
        )

    @patch("services.audio_service.VideoFileClip")
    @patch("services.audio_service.os.path.exists")
    @patch("services.audio_service.os.makedirs")
    def test_extract_audio_exception(
        self,
        mock_makedirs,
        mock_exists,
        mock_clip,
    ):




        video_path = os.path.join(
            "uploads",
            "video.mp4",
        )





    @patch("services.audio_service.os.listdir")
    @patch("services.audio_service.os.makedirs")
    def test_list_audio(
        self,
        mock_makedirs,
        mock_listdir,
    ):
        mock_listdir.return_value = [
            "b.mp3",
            "a.mp3",
        ]

        result = AudioService.list_audio()

        assert result == [
            "a.mp3",
            "b.mp3",
        ]

        mock_listdir.assert_called_once_with(
            AudioService.AUDIO_FOLDER
        )

    @patch("services.audio_service.os.remove")
    @patch("services.audio_service.os.path.exists")
    def test_delete_audio_success(
        self,
        mock_exists,
        mock_remove,
    ):
        mock_exists.return_value = True

        result = AudioService.delete_audio(
            "sample.mp3"
        )

        expected = os.path.join(
            "audio",
            "sample.mp3",
        )

        assert result is True

        mock_remove.assert_called_once_with(
            expected
        )

    @patch("services.audio_service.os.path.exists")
    def test_delete_audio_not_found(
        self,
        mock_exists,
    ):
        mock_exists.return_value = False

        result = AudioService.delete_audio(
            "sample.mp3"
        )

        assert result is False