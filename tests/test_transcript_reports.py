# tests/test_transcript_reports.py

from unittest.mock import MagicMock, patch

from components.export_transcripts import (
    show_export_transcripts,
    show_transcript_reports,
)


class TestExportTranscripts:

    @patch(
        "components.export_transcripts.TranscriptUtils.list_transcripts"
    )
    @patch("components.export_transcripts.st.download_button")
    def test_show_export_transcripts_no_transcripts(
        self,
        mock_download_button,
        mock_list,
    ):
        mock_list.return_value = []

        show_export_transcripts()

        mock_download_button.assert_not_called()

    @patch(
        "components.export_transcripts.TranscriptUtils.read_transcript"
    )
    @patch(
        "components.export_transcripts.TranscriptUtils.list_transcripts"
    )
    @patch("components.export_transcripts.st.download_button")
    def test_show_export_transcripts_success(
        self,
        mock_download_button,
        mock_list,
        mock_read,
    ):
        mock_list.return_value = [
            "video1.txt",
            "video2.txt",
        ]

        mock_read.side_effect = [
            "Transcript One",
            "Transcript Two",
        ]

        show_export_transcripts()

        assert mock_read.call_count == 2

        mock_read.assert_any_call("video1.txt")
        mock_read.assert_any_call("video2.txt")

        mock_download_button.assert_called_once()

        args = mock_download_button.call_args.kwargs

        assert args["label"] == "📦 Download All Transcripts"
        assert args["file_name"] == "transcripts.zip"
        assert args["mime"] == "application/zip"
        assert args["use_container_width"] is True

        assert isinstance(args["data"], bytes)


class TestTranscriptReports:

    @patch("components.export_transcripts.st.info")
    @patch("components.export_transcripts.st.subheader")
    @patch(
        "components.export_transcripts.st.session_state",
        {},
    )
    def test_show_transcript_reports_no_transcript(
        self,
        mock_subheader,
        mock_info,
    ):
        show_transcript_reports()

        mock_subheader.assert_called_once_with(
            "📑 Transcript Reports"
        )

        mock_info.assert_called_once_with(
            "No transcript available."
        )

    @patch("components.export_transcripts.st.download_button")
    @patch("components.export_transcripts.st.metric")
    @patch("components.export_transcripts.st.columns")
    @patch("components.export_transcripts.st.divider")
    @patch("components.export_transcripts.st.text_area")
    @patch("components.export_transcripts.st.subheader")
    @patch(
        "components.export_transcripts.st.session_state",
        {
            "transcript": (
                "Hello world\n"
                "This is a transcript"
            )
        },
    )
    def test_show_transcript_reports_success(
        self,
        mock_subheader,
        mock_text_area,
        mock_divider,
        mock_columns,
        mock_metric,
        mock_download_button,
    ):
        col1 = MagicMock()
        col2 = MagicMock()
        col3 = MagicMock()

        col1.__enter__.return_value = col1
        col1.__exit__.return_value = False

        col2.__enter__.return_value = col2
        col2.__exit__.return_value = False

        col3.__enter__.return_value = col3
        col3.__exit__.return_value = False

        mock_columns.return_value = (
            col1,
            col2,
            col3,
        )

        transcript = (
            "Hello world\n"
            "This is a transcript"
        )

        show_transcript_reports()

        mock_subheader.assert_called_once_with(
            "📑 Transcript Reports"
        )

        mock_text_area.assert_called_once_with(
            "Transcript",
            transcript,
            height=350,
        )

        mock_columns.assert_called_once_with(3)

        # 6 words, 2 lines
        assert mock_metric.call_count == 3

        mock_metric.assert_any_call(
            "Words",
            6,
        )

        mock_metric.assert_any_call(
            "Characters",
            len(transcript),
        )

        mock_metric.assert_any_call(
            "Lines",
            2,
        )

        assert mock_divider.call_count == 2

        mock_download_button.assert_called_once_with(
            "⬇ Download TXT",
            transcript,
            file_name="transcript.txt",
            mime="text/plain",
            use_container_width=True,
        )