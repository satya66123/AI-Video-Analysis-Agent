import os
from unittest.mock import MagicMock, patch

from utils.audio_metadata import AudioMetadata


class TestAudioMetadata:

    @patch("utils.audio_metadata.os.path.getsize")
    @patch("utils.audio_metadata.MP3")
    def test_get_metadata_success(
        self,
        mock_mp3,
        mock_getsize,
    ):
        audio = MagicMock()

        audio.info.length = 120.567
        audio.info.bitrate = 192000
        audio.info.sample_rate = 44100
        audio.info.channels = 2

        mock_mp3.return_value = audio
        mock_getsize.return_value = 5 * 1024 * 1024

        result = AudioMetadata.get_metadata(
            "audio/test.mp3"
        )

        assert result == {
            "filename": "test.mp3",
            "duration": 120.57,
            "bitrate": 192,
            "sample_rate": 44100,
            "channels": 2,
            "size_mb": 5.0,
        }

        mock_mp3.assert_called_once_with(
            "audio/test.mp3"
        )

        mock_getsize.assert_called_once_with(
            "audio/test.mp3"
        )

    @patch("utils.audio_metadata.MP3")
    def test_get_metadata_exception(
        self,
        mock_mp3,
    ):
        mock_mp3.side_effect = Exception(
            "Invalid audio"
        )

        result = AudioMetadata.get_metadata(
            "audio/test.mp3"
        )

        assert result is None