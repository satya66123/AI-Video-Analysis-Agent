import os
from unittest.mock import MagicMock, patch

from services.audio_service import AudioService


class TestAudioService:

    @patch("services.audio_service.os.makedirs")
    @patch("services.audio_service.os.path.exists")
    def test_extract_audio_duplicate(
        self,
        mock_exists,
        mock_makedirs,
    ):
        mock_exists.return_value = True

        progress = MagicMock()
        status = MagicMock()

        video_path = os.path.join(
            "uploads",
            "video.mp4",
        )

        result = AudioService.extract_audio(
            video_path=video_path,
            progress_bar=progress,
            status_text=status,
        )

        expected = os.path.join(
            "audio",
            "video.mp3",
        )

        assert result == expected

        progress.progress.assert_called_once_with(1.0)
        status.warning.assert_called_once_with(
            "⚠ Audio already extracted."
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
        mock_exists.return_value = False

        progress = MagicMock()
        status = MagicMock()

        video = MagicMock()
        mock_clip.return_value = video

        video_path = os.path.join(
            "uploads",
            "video.mp4",
        )

        result = AudioService.extract_audio(
            video_path=video_path,
            progress_bar=progress,
            status_text=status,
        )

        expected = os.path.join(
            "audio",
            "video.mp3",
        )

        assert result == expected

        mock_clip.assert_called_once_with(
            video_path
        )

        video.audio.write_audiofile.assert_called_once_with(
            expected,
            logger=None,
        )

        video.close.assert_called_once()

        progress.progress.assert_any_call(10)
        progress.progress.assert_any_call(40)
        progress.progress.assert_any_call(100)

        status.info.assert_any_call(
            "Opening video..."
        )
        status.info.assert_any_call(
            "Extracting audio..."
        )
        status.success.assert_called_once_with(
            "✅ Audio extracted successfully."
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
        mock_exists.return_value = False

        mock_clip.side_effect = Exception(
            "MoviePy Error"
        )

        status = MagicMock()

        video_path = os.path.join(
            "uploads",
            "video.mp4",
        )

        result = AudioService.extract_audio(
            video_path=video_path,
            status_text=status,
        )

        assert result is None

        status.error.assert_called_once_with(
            "MoviePy Error"
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