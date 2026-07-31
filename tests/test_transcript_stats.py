from unittest.mock import MagicMock, patch

from components.transcript_stats import show_transcript_stats


class TestTranscriptStats:

    @patch("components.transcript_stats.st.columns")
    @patch("components.transcript_stats.TranscriptUtils.read_transcript")
    @patch("components.transcript_stats.TranscriptUtils.list_transcripts")
    def test_show_transcript_stats_no_transcripts(
        self,
        mock_list,
        mock_read,
        mock_columns,
    ):
        mock_list.return_value = []

        col1 = MagicMock()
        col2 = MagicMock()
        col3 = MagicMock()

        mock_columns.return_value = (
            col1,
            col2,
            col3,
        )

        show_transcript_stats()

        mock_read.assert_not_called()

        col1.metric.assert_called_once_with(
            "Transcripts",
            0,
        )

        col2.metric.assert_called_once_with(
            "Words",
            0,
        )

        col3.metric.assert_called_once_with(
            "Characters",
            0,
        )

    @patch("components.transcript_stats.st.columns")
    @patch("components.transcript_stats.TranscriptUtils.read_transcript")
    @patch("components.transcript_stats.TranscriptUtils.list_transcripts")
    def test_show_transcript_stats_success(
        self,
        mock_list,
        mock_read,
        mock_columns,
    ):
        mock_list.return_value = [
            "video1.txt",
            "video2.txt",
        ]

        mock_read.side_effect = [
            "Hello world",
            "This is transcript",
        ]

        col1 = MagicMock()
        col2 = MagicMock()
        col3 = MagicMock()

        mock_columns.return_value = (
            col1,
            col2,
            col3,
        )

        show_transcript_stats()

        mock_read.assert_any_call("video1.txt")
        mock_read.assert_any_call("video2.txt")

        assert mock_read.call_count == 2

        total_words = (
            len("Hello world".split())
            + len("This is transcript".split())
        )

        total_characters = (
            len("Hello world")
            + len("This is transcript")
        )

        col1.metric.assert_called_once_with(
            "Transcripts",
            2,
        )

        col2.metric.assert_called_once_with(
            "Words",
            total_words,
        )

        col3.metric.assert_called_once_with(
            "Characters",
            total_characters,
        )