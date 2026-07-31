import os
from unittest.mock import MagicMock, patch

from utils.audio_splitter import AudioSplitter


class TestAudioSplitter:

    @patch("utils.audio_splitter.uuid.uuid4")
    @patch("utils.audio_splitter.AudioSegment.from_file")
    @patch("utils.audio_splitter.os.makedirs")
    def test_split_audio_success(
        self,
        mock_makedirs,
        mock_from_file,
        mock_uuid,
    ):
        audio = MagicMock()
        audio.__len__.return_value = 10 * 60 * 1000  # 10 minutes

        chunk = MagicMock()
        audio.__getitem__.return_value = chunk

        mock_from_file.return_value = audio

        uuid_obj = MagicMock()
        uuid_obj.hex = "1234567890abcdef"
        mock_uuid.return_value = uuid_obj

        result = AudioSplitter.split_audio(
            "audio.mp3",
            chunk_minutes=5,
        )

        expected = [
            os.path.join(
                "audio_chunks",
                "chunk_1_12345678.wav",
            ),
            os.path.join(
                "audio_chunks",
                "chunk_2_12345678.wav",
            ),
        ]

        assert result == expected

        assert chunk.export.call_count == 2

        chunk.export.assert_any_call(
            expected[0],
            format="wav",
        )

        chunk.export.assert_any_call(
            expected[1],
            format="wav",
        )

    @patch("utils.audio_splitter.AudioSegment.from_file")
    @patch("utils.audio_splitter.os.makedirs")
    def test_split_audio_single_chunk(
        self,
        mock_makedirs,
        mock_from_file,
    ):
        audio = MagicMock()
        audio.__len__.return_value = 2 * 60 * 1000

        chunk = MagicMock()
        audio.__getitem__.return_value = chunk

        mock_from_file.return_value = audio

        result = AudioSplitter.split_audio(
            "audio.mp3",
            chunk_minutes=5,
        )

        assert len(result) == 1

    @patch("utils.audio_splitter.os.remove")
    @patch("utils.audio_splitter.os.path.exists")
    def test_cleanup_success(
        self,
        mock_exists,
        mock_remove,
    ):
        mock_exists.return_value = True

        paths = [
            "a.wav",
            "b.wav",
        ]

        AudioSplitter.cleanup(paths)

        assert mock_remove.call_count == 2

        mock_remove.assert_any_call("a.wav")
        mock_remove.assert_any_call("b.wav")

    @patch("utils.audio_splitter.os.path.exists")
    def test_cleanup_file_not_found(
        self,
        mock_exists,
    ):
        mock_exists.return_value = False

        AudioSplitter.cleanup(
            ["a.wav"]
        )

        mock_exists.assert_called_once_with(
            "a.wav"
        )

    @patch("utils.audio_splitter.os.remove")
    @patch("utils.audio_splitter.os.path.exists")
    def test_cleanup_remove_exception(
        self,
        mock_exists,
        mock_remove,
    ):
        mock_exists.return_value = True

        mock_remove.side_effect = Exception(
            "Delete Error"
        )

        AudioSplitter.cleanup(
            ["a.wav"]
        )

        mock_remove.assert_called_once_with(
            "a.wav"
        )