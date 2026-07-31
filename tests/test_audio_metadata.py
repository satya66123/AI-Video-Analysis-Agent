from unittest.mock import MagicMock, patch

from components.audio_metadata import show_audio_metadata


class TestAudioMetadata:

    @patch("components.audio_metadata.st.columns")
    @patch("components.audio_metadata.st.subheader")
    def test_show_audio_metadata(
        self,
        mock_subheader,
        mock_columns,
    ):
        metadata = {
            "duration": 120,
            "bitrate": 320,
            "channels": 2,
            "sample_rate": 44100,
            "size_mb": 8.5,
            "filename": "song.mp3",
        }

        col1 = MagicMock()
        col2 = MagicMock()

        col1.__enter__.return_value = col1
        col1.__exit__.return_value = False

        col2.__enter__.return_value = col2
        col2.__exit__.return_value = False

        mock_columns.return_value = (col1, col2)

        show_audio_metadata(metadata)

        mock_subheader.assert_called_once_with(
            "🎵 Audio Metadata"
        )

        mock_columns.assert_called_once_with(2)

        expected_calls = [
            ("Duration", "120 sec"),
            ("Bitrate", "320 kbps"),
            ("Channels", 2),
            ("Sample Rate", "44100 Hz"),
            ("Size", "8.5 MB"),
            ("Filename", "song.mp3"),
        ]

        actual_calls = [
            call.args
            for call in patch(
                "components.audio_metadata.st.metric"
            ).start().mock_calls
        ]
        patch.stopall()