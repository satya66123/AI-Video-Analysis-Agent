"""
tests/test_speech_agent_service.py
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from services.speech_agent_service import SpeechService


class DummyProgressBar:

    def __init__(self):
        self.calls = []

    def progress(self, value):
        self.calls.append(value)


class DummyStatus:

    def __init__(self):
        self.info_calls = []
        self.warning_calls = []
        self.success_calls = []
        self.error_calls = []

    def info(self, message):
        self.info_calls.append(message)

    def warning(self, message):
        self.warning_calls.append(message)

    def success(self, message):
        self.success_calls.append(message)

    def error(self, message):
        self.error_calls.append(message)


@pytest.fixture
def transcript_folder(tmp_path, monkeypatch):

    monkeypatch.setattr(
        SpeechService,
        "TRANSCRIPT_FOLDER",
        str(tmp_path),
    )

    SpeechService._model = None
    SpeechService._model_name = None

    return tmp_path


@pytest.fixture
def sample_audio(tmp_path):

    path = tmp_path / "sample.mp3"

    path.write_bytes(b"dummy audio")

    return str(path)


@patch("services.speech_agent_service.whisper.load_model")
def test_load_model(mock_load):

    model = MagicMock()

    mock_load.return_value = model

    loaded = SpeechService.load_model("base")

    assert loaded == model
    assert SpeechService._model == model

    assert SpeechService._model_name == "base"


@patch("services.speech_agent_service.AudioSplitter.cleanup")
@patch("services.speech_agent_service.AudioSplitter.split_audio")
@patch("services.speech_agent_service.whisper.load_model")
def test_transcribe_success(
    mock_load,
    mock_split,
    mock_cleanup,
    transcript_folder,
    sample_audio,
):

    model = MagicMock()

    model.transcribe.return_value = {
        "text": "Hello World"
    }

    mock_load.return_value = model

    chunk = os.path.join(
        transcript_folder,
        "chunk1.mp3",
    )

    open(chunk, "wb").close()

    mock_split.return_value = [chunk]

    progress = DummyProgressBar()

    status = DummyStatus()

    result = SpeechService.transcribe(
        sample_audio,
        progress,
        status,
    )

    assert result is not None

    assert result["text"] == "Hello World"

    assert result["chunks"] == 1

    assert result["model"] == "base"

    assert result["word_count"] == 2

    assert os.path.exists(result["path"])

    assert progress.calls[-1] == 100

    assert len(status.success_calls) == 1

    mock_cleanup.assert_called_once()


def test_missing_audio_file(transcript_folder):

    with pytest.raises(FileNotFoundError):

        SpeechService.transcribe(
            "missing.mp3"
        )


def test_empty_audio_file(
    transcript_folder,
    tmp_path,
):

    empty = tmp_path / "empty.mp3"

    empty.write_bytes(b"")

    with pytest.raises(ValueError):

        SpeechService.transcribe(
            str(empty)
        )


def test_duplicate_transcript(
    transcript_folder,
    sample_audio,
):

    transcript = os.path.join(
        transcript_folder,
        "sample.txt",
    )

    with open(
        transcript,
        "w",
        encoding="utf-8",
    ) as file:

        file.write("Existing Transcript")

    progress = DummyProgressBar()

    status = DummyStatus()

    result = SpeechService.transcribe(
        sample_audio,
        progress,
        status,
    )

    assert result["text"] == "Existing Transcript"

    assert result["chunks"] == 0

    assert result["model"] == "base"

    assert result["word_count"] == 2

    assert result["character_count"] == len(
        "Existing Transcript"
    )

    assert progress.calls[-1] == 100

    assert len(status.warning_calls) == 1


@patch("services.speech_agent_service.AudioSplitter.cleanup")
@patch("services.speech_agent_service.AudioSplitter.split_audio")
@patch("services.speech_agent_service.whisper.load_model")
def test_no_chunks_created(
    mock_load,
    mock_split,
    mock_cleanup,
    transcript_folder,
    sample_audio,
):

    mock_load.return_value = MagicMock()

    mock_split.return_value = []

    progress = DummyProgressBar()

    status = DummyStatus()

    result = SpeechService.transcribe(
        sample_audio,
        progress,
        status,
    )

    assert result is None

    assert progress.calls[-1] == 0

    assert len(status.error_calls) == 1

    mock_cleanup.assert_called_once()


@patch("services.speech_agent_service.AudioSplitter.cleanup")
@patch("services.speech_agent_service.AudioSplitter.split_audio")
@patch("services.speech_agent_service.whisper.load_model")
def test_no_speech_detected(
    mock_load,
    mock_split,
    mock_cleanup,
    transcript_folder,
    sample_audio,
):

    model = MagicMock()

    model.transcribe.return_value = {
        "text": ""
    }

    mock_load.return_value = model

    chunk = os.path.join(
        transcript_folder,
        "chunk.mp3",
    )

    open(chunk, "wb").close()

    mock_split.return_value = [chunk]

    status = DummyStatus()

    result = SpeechService.transcribe(
        sample_audio,
        None,
        status,
    )

    assert result is None

    assert len(status.warning_calls) == 1


@patch("services.speech_agent_service.AudioSplitter.cleanup")
@patch("services.speech_agent_service.AudioSplitter.split_audio")
@patch("services.speech_agent_service.whisper.load_model")
def test_multiple_chunks(
    mock_load,
    mock_split,
    mock_cleanup,
    transcript_folder,
    sample_audio,
):

    model = MagicMock()

    model.transcribe.side_effect = [
        {"text": "Hello"},
        {"text": "World"},
    ]

    mock_load.return_value = model

    chunk1 = os.path.join(
        transcript_folder,
        "chunk1.mp3",
    )

    chunk2 = os.path.join(
        transcript_folder,
        "chunk2.mp3",
    )

    open(chunk1, "wb").close()
    open(chunk2, "wb").close()

    mock_split.return_value = [
        chunk1,
        chunk2,
    ]

    result = SpeechService.transcribe(
        sample_audio
    )

    assert result is not None

    assert result["text"] == "Hello\n\nWorld"

    assert result["chunks"] == 2

    mock_cleanup.assert_called_once()