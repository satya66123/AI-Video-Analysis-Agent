import os
from unittest.mock import MagicMock, patch

import pytest

from services.audio_service import AudioService


class DummyAudio:
    def write_audiofile(self, path, logger=None):
        pass


class DummyVideo:
    def __init__(self):
        self.audio = DummyAudio()
        self.duration = 120.5

    def close(self):
        pass


@pytest.fixture
def audio_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(
        AudioService,
        "AUDIO_FOLDER",
        str(tmp_path),
    )
    return tmp_path


class TestAudioService:

    @patch("services.audio_service.VideoFileClip")
    @patch("services.audio_service.os.path.exists")
    @patch("services.audio_service.os.makedirs")
    def test_extract_audio_duplicate(
        self,
        mock_makedirs,
        mock_exists,
        mock_video,
        audio_dir,
    ):
        mock_exists.return_value = True
        mock_video.return_value = DummyVideo()

        progress = MagicMock()
        status = MagicMock()

        result = AudioService.extract_audio("video.mp4", progress, status)

        print(type(result))
        from pathlib import Path

        assert Path(result).name == "video.mp3"




        progress.progress.assert_called_with(1.0)
        status.warning.assert_called_once()

    @patch("services.audio_service.VideoFileClip")
    @patch("services.audio_service.os.path.exists")
    def test_extract_audio_success(
        self,
        mock_exists,
        mock_video,
        audio_dir,
    ):
        mock_exists.return_value = False
        mock_video.return_value = DummyVideo()

        progress = MagicMock()
        status = MagicMock()

        result = AudioService.extract_audio(
            "video.mp4",
            progress,
            status,
        )

        from pathlib import Path

        assert Path(result).name == "video.mp3"


        progress.progress.assert_any_call(10)
        progress.progress.assert_any_call(40)
        progress.progress.assert_any_call(100)

        status.success.assert_called_once()

    @patch("services.audio_service.VideoFileClip")
    @patch("services.audio_service.os.path.exists")
    def test_extract_audio_exception(
        self,
        mock_exists,
        mock_video,
        audio_dir,
    ):
        mock_exists.return_value = False
        mock_video.side_effect = Exception("boom")

        status = MagicMock()

        result = AudioService.extract_audio(
            "video.mp4",
            None,
            status,
        )

        assert result is None
        status.error.assert_called_once()

    def test_list_audio(
        self,
        audio_dir,
    ):
        (audio_dir / "a.mp3").write_text("")
        (audio_dir / "b.mp3").write_text("")

        result = AudioService.list_audio()

        assert result == ["a.mp3", "b.mp3"]

    def test_delete_audio_success(
        self,
        audio_dir,
    ):
        file = audio_dir / "a.mp3"
        file.write_text("x")

        assert AudioService.delete_audio("a.mp3") is True
        assert not file.exists()

    def test_delete_audio_missing(
        self,
        audio_dir,
    ):
        assert AudioService.delete_audio("missing.mp3") is False