import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from services.speech_service import SpeechService


class TestSpeechService:

    def setup_method(self):
        SpeechService._model = None
        SpeechService._model_name = None

    @patch("services.speech_service.whisper.load_model")
    def test_load_model_first_time(
        self,
        mock_load_model,
    ):
        model = MagicMock()
        mock_load_model.return_value = model

        result = SpeechService.load_model("base")

        assert result is model
        assert SpeechService._model is model
        assert SpeechService._model_name == "base"

        mock_load_model.assert_called_once_with("base")

    @patch("services.speech_service.whisper.load_model")
    def test_load_model_cached(
        self,
        mock_load_model,
    ):
        model = MagicMock()

        SpeechService._model = model
        SpeechService._model_name = "base"

        result = SpeechService.load_model("base")

        assert result is model

        mock_load_model.assert_not_called()

    @patch("services.speech_service.whisper.load_model")
    def test_load_model_new_model(
        self,
        mock_load_model,
    ):
        old = MagicMock()
        new = MagicMock()

        SpeechService._model = old
        SpeechService._model_name = "tiny"

        mock_load_model.return_value = new

        result = SpeechService.load_model("base")

        assert result is new

        mock_load_model.assert_called_once_with(
            "base"
        )

    @patch("services.speech_service.os.makedirs")
    @patch("services.speech_service.os.path.exists")
    def test_transcribe_audio_not_found(
        self,
        mock_exists,
        mock_makedirs,
    ):
        mock_exists.return_value = False

        with pytest.raises(FileNotFoundError):
            SpeechService.transcribe(
                "audio.mp3"
            )

    @patch("services.speech_service.os.makedirs")
    @patch("services.speech_service.os.path.getsize")
    @patch("services.speech_service.os.path.exists")
    def test_transcribe_empty_audio(
        self,
        mock_exists,
        mock_getsize,
        mock_makedirs,
    ):
        mock_exists.side_effect = [True]

        mock_getsize.return_value = 0

        with pytest.raises(ValueError):
            SpeechService.transcribe(
                "audio.mp3"
            )

    @patch("builtins.open", new_callable=mock_open, read_data="Transcript")
    @patch("services.speech_service.os.path.getsize")
    @patch("services.speech_service.os.path.exists")
    @patch("services.speech_service.os.makedirs")
    def test_transcribe_duplicate(
        self,
        mock_makedirs,
        mock_exists,
        mock_getsize,
        mock_file,
    ):
        mock_exists.side_effect = [
            True,
            True,
        ]

        mock_getsize.return_value = 100

        progress = MagicMock()
        status = MagicMock()

        result = SpeechService.transcribe(
            "audio.mp3",
            progress_bar=progress,
            status_text=status,
        )

        assert result == "Transcript"

        progress.progress.assert_called_once_with(
            100
        )

        status.warning.assert_called_once_with(
            "⚠ Transcript already exists."
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("services.speech_service.AudioSplitter.cleanup")
    @patch("services.speech_service.AudioSplitter.split_audio")
    @patch("services.speech_service.SpeechService.load_model")
    @patch("services.speech_service.os.path.getsize")
    @patch("services.speech_service.os.path.exists")
    @patch("services.speech_service.os.makedirs")
    def test_transcribe_success(
        self,
        mock_makedirs,
        mock_exists,
        mock_getsize,
        mock_load_model,
        mock_split,
        mock_cleanup,
        mock_file,
    ):
        mock_exists.side_effect = [
            True,
            False,
        ]

        mock_getsize.return_value = 100

        mock_split.return_value = [
            "c1.wav",
            "c2.wav",
        ]

        model = MagicMock()

        model.transcribe.side_effect = [
            {"text": "Hello"},
            {"text": "World"},
        ]

        mock_load_model.return_value = model

        progress = MagicMock()
        status = MagicMock()

        result = SpeechService.transcribe(
            "audio.mp3",
            progress_bar=progress,
            status_text=status,
        )

        assert result == "Hello\n\nWorld"

        mock_cleanup.assert_called_once()

        mock_file().write.assert_called_once_with(
            "Hello\n\nWorld"
        )

        status.success.assert_called_once()

    @patch("services.speech_service.AudioSplitter.split_audio")
    @patch("services.speech_service.SpeechService.load_model")
    @patch("services.speech_service.os.path.getsize")
    @patch("services.speech_service.os.path.exists")
    @patch("services.speech_service.os.makedirs")
    def test_transcribe_no_chunks(
        self,
        mock_makedirs,
        mock_exists,
        mock_getsize,
        mock_load_model,
        mock_split,
    ):
        mock_exists.side_effect = [
            True,
            False,
        ]

        mock_getsize.return_value = 100

        mock_split.return_value = []

        result = SpeechService.transcribe(
            "audio.mp3"
        )

        assert result is None

    @patch("services.speech_service.AudioSplitter.cleanup")
    @patch("services.speech_service.AudioSplitter.split_audio")
    @patch("services.speech_service.SpeechService.load_model")
    @patch("services.speech_service.os.path.getsize")
    @patch("services.speech_service.os.path.exists")
    @patch("services.speech_service.os.makedirs")
    def test_transcribe_exception(
        self,
        mock_makedirs,
        mock_exists,
        mock_getsize,
        mock_load_model,
        mock_split,
        mock_cleanup,
    ):
        mock_exists.side_effect = [
            True,
            False,
        ]

        mock_getsize.return_value = 100

        mock_split.side_effect = Exception(
            "Split Error"
        )

        progress = MagicMock()
        status = MagicMock()

        result = SpeechService.transcribe(
            "audio.mp3",
            progress_bar=progress,
            status_text=status,
        )

        assert result is None

        progress.progress.assert_called_with(0)

        status.error.assert_called_once()

        mock_cleanup.assert_called_once()