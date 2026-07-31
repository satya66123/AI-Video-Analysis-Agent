"""
tests/test_audio_agent_service.py
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from services.audio_agent_service import AudioService


class DummyProgressBar:

    def __init__(self):
        self.values = []

    def progress(self, value):
        self.values.append(value)


class DummyStatus:

    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(("info", message))

    def warning(self, message):
        self.messages.append(("warning", message))

    def success(self, message):
        self.messages.append(("success", message))

    def error(self, message):
        self.messages.append(("error", message))


@pytest.fixture
def audio_dir(tmp_path, monkeypatch):

    monkeypatch.setattr(
        AudioService,
        "AUDIO_FOLDER",
        str(tmp_path),
    )

    return tmp_path


@pytest.fixture
def mock_video():

    video = MagicMock()

    video.duration = 120

    video.audio = MagicMock()

    return video


@patch("services.audio_agent_service.VideoFileClip")
def test_extract_audio_success(
    mock_clip,
    audio_dir,
    mock_video,
):

    mock_clip.return_value = mock_video

    progress = DummyProgressBar()

    status = DummyStatus()

    result = AudioService.extract_audio(
        "sample.mp4",
        progress,
        status,
    )




@patch("services.audio_agent_service.VideoFileClip")
def test_duplicate_audio(
    mock_clip,
    audio_dir,
    mock_video,
):

    mock_clip.return_value = mock_video

    duplicate = os.path.join(
        audio_dir,
        "sample.mp3",
    )

    open(
        duplicate,
        "wb",
    ).close()

    progress = DummyProgressBar()

    status = DummyStatus()

    result = AudioService.extract_audio(
        "sample.mp4",
        progress,
        status,
    )




@patch("services.audio_agent_service.VideoFileClip")
def test_extract_audio_exception(
    mock_clip,
    audio_dir,
):

    mock_clip.side_effect = Exception(
        "Extraction failed"
    )

    status = DummyStatus()

    result = AudioService.extract_audio(
        "sample.mp4",
        None,
        status,
    )

    assert result is None

    assert status.messages[-1][0] == "error"


def test_list_audio(audio_dir):

    open(
        os.path.join(audio_dir, "one.mp3"),
        "wb",
    ).close()

    open(
        os.path.join(audio_dir, "two.mp3"),
        "wb",
    ).close()

    files = AudioService.list_audio()

    assert len(files) == 2

    assert "one.mp3" in files

    assert "two.mp3" in files


def test_delete_audio(audio_dir):

    file = os.path.join(
        audio_dir,
        "sample.mp3",
    )

    open(
        file,
        "wb",
    ).close()

    assert AudioService.delete_audio(
        "sample.mp3"
    ) is True

    assert not os.path.exists(file)


def test_delete_missing_audio(audio_dir):

    assert AudioService.delete_audio(
        "missing.mp3"
    ) is False