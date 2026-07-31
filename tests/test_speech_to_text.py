import os
from unittest.mock import MagicMock, patch

from pages.speech_to_text import show_speech_to_text


class TestSpeechToText:

    @patch("pages.speech_to_text.st.info")
    @patch("pages.speech_to_text.show_transcript_dashboard")
    @patch("pages.speech_to_text.st.divider")
    @patch("pages.speech_to_text.st.columns")
    @patch("pages.speech_to_text.TranscriptUtils.read_transcript")
    @patch("pages.speech_to_text.TranscriptUtils.list_transcripts")
    @patch("pages.speech_to_text.AudioService.list_audio")
    @patch("pages.speech_to_text.st.selectbox")
    @patch("pages.speech_to_text.st.title")
    def test_no_audio_files(
        self,
        mock_title,
        mock_selectbox,
        mock_list_audio,
        mock_list_transcripts,
        mock_read,
        mock_columns,
        mock_divider,
        mock_dashboard,
        mock_info,
    ):
        mock_selectbox.return_value = "base"

        mock_list_audio.return_value = []

        mock_list_transcripts.return_value = [
            "t1.txt",
            "t2.txt",
        ]

        mock_read.side_effect = [
            "hello world",
            "another transcript here",
        ]

        col1 = MagicMock()
        col2 = MagicMock()
        col3 = MagicMock()

        mock_columns.return_value = (
            col1,
            col2,
            col3,
        )

        show_speech_to_text()

        mock_title.assert_called_once_with(
            "🎤 Speech To Text"
        )

        mock_selectbox.assert_called_once_with(
            "Whisper Model",
            [
                "tiny",
                "base",
                "small",
                "medium",
                "large",
            ],
            index=1,
        )

        col1.metric.assert_called_once_with(
            "🎵 Audio Files",
            0,
        )

        col2.metric.assert_called_once_with(
            "📄 Transcripts",
            2,
        )

        col3.metric.assert_called_once_with(
            "📝 Total Words",
            5,
        )

        mock_dashboard.assert_called_once()

        mock_info.assert_called_once_with(
            "No extracted audio found."
        )

    @patch("pages.speech_to_text.show_transcript_dashboard")
    @patch("pages.speech_to_text.st.divider")
    @patch("pages.speech_to_text.st.columns")
    @patch("pages.speech_to_text.TranscriptUtils.read_transcript")
    @patch("pages.speech_to_text.TranscriptUtils.list_transcripts")
    @patch("pages.speech_to_text.AudioService.list_audio")
    @patch("pages.speech_to_text.st.selectbox")
    def test_total_words_calculation(
        self,
        mock_selectbox,
        mock_list_audio,
        mock_list_transcripts,
        mock_read,
        mock_columns,
        mock_divider,
        mock_dashboard,
    ):
        mock_selectbox.return_value = "base"

        mock_list_audio.return_value = []

        mock_list_transcripts.return_value = [
            "a.txt",
            "b.txt",
            "c.txt",
        ]

        mock_read.side_effect = [
            "one two",
            "three four five",
            "six",
        ]

        col1 = MagicMock()
        col2 = MagicMock()
        col3 = MagicMock()

        mock_columns.return_value = (
            col1,
            col2,
            col3,
        )

        show_speech_to_text()

        col3.metric.assert_called_once_with(
            "📝 Total Words",
            6,
        )


    @patch("pages.speech_to_text.show_transcripts")
    @patch("pages.speech_to_text.show_export_transcripts")
    @patch("pages.speech_to_text.show_transcript_stats")
    @patch("pages.speech_to_text.show_transcript_dashboard")
    @patch("pages.speech_to_text.st.divider")
    @patch("pages.speech_to_text.st.success")
    @patch("pages.speech_to_text.st.text_area")
    @patch("pages.speech_to_text.SpeechService.transcribe")
    @patch("pages.speech_to_text.st.empty")
    @patch("pages.speech_to_text.st.progress")
    @patch("pages.speech_to_text.st.button")
    @patch("pages.speech_to_text.st.audio")
    @patch("pages.speech_to_text.os.path.exists")
    @patch("pages.speech_to_text.st.columns")
    @patch("pages.speech_to_text.TranscriptUtils.read_transcript")
    @patch("pages.speech_to_text.TranscriptUtils.list_transcripts")
    @patch("pages.speech_to_text.AudioService.list_audio")
    @patch("pages.speech_to_text.st.selectbox")
    def test_transcribe_success(
            self,
            mock_selectbox,
            mock_list_audio,
            mock_list_transcripts,
            mock_read,
            mock_columns,
            mock_exists,
            mock_audio,
            mock_button,
            mock_progress,
            mock_empty,
            mock_transcribe,
            mock_text_area,
            mock_success,
            mock_divider,
            mock_dashboard,
            mock_stats,
            mock_export,
            mock_transcripts,
    ):
        mock_selectbox.side_effect = [
            "base",
            "sample.mp3",
        ]

        # Called twice in the page
        mock_list_audio.side_effect = [
            ["sample.mp3"],
            ["sample.mp3"],
        ]

        mock_list_transcripts.return_value = []



        mock_columns.return_value = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )




        mock_exists.return_value = True

        progress = mock_progress.return_value
        status = mock_empty.return_value

        mock_button.return_value = True

        mock_transcribe.return_value = (
            "This is a transcript."
        )

        show_speech_to_text()

        mock_audio.assert_called_once()

        mock_transcribe.assert_called_once_with(
            "audio\\sample.mp3"
            if __import__("os").name == "nt"
            else "audio/sample.mp3",
            progress,
            status,
            "base",
        )

        mock_success.assert_called_once_with(
            "Transcript generated."
        )

        mock_text_area.assert_called_once_with(
            "Transcript",
            "This is a transcript.",
            height=300,
        )

        mock_dashboard.assert_called_once()
        mock_stats.assert_called_once()
        mock_export.assert_called_once()
        mock_transcripts.assert_called_once()

    @patch("pages.speech_to_text.show_transcripts")
    @patch("pages.speech_to_text.show_export_transcripts")
    @patch("pages.speech_to_text.show_transcript_stats")
    @patch("pages.speech_to_text.show_transcript_dashboard")
    @patch("pages.speech_to_text.st.divider")
    @patch("pages.speech_to_text.st.audio")
    @patch("pages.speech_to_text.os.path.exists")
    @patch("pages.speech_to_text.st.columns")
    @patch("pages.speech_to_text.TranscriptUtils.read_transcript")
    @patch("pages.speech_to_text.TranscriptUtils.list_transcripts")
    @patch("pages.speech_to_text.AudioService.list_audio")
    @patch("pages.speech_to_text.st.button")
    @patch("pages.speech_to_text.st.selectbox")
    def test_audio_preview(
            self,
            mock_selectbox,
            mock_button,
            mock_list_audio,
            mock_list_transcripts,
            mock_read,
            mock_columns,
            mock_exists,
            mock_audio,
            mock_divider,
            mock_dashboard,
            mock_stats,
            mock_export,
            mock_transcripts,
    ):
        mock_selectbox.side_effect = [
            "base",
            "sample.mp3",
        ]

        mock_list_audio.side_effect = [
            ["sample.mp3"],
            ["sample.mp3"],
        ]

        mock_list_transcripts.return_value = []

        from unittest.mock import MagicMock

        mock_columns.return_value = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        mock_exists.return_value = True

        mock_button.return_value = False

        show_speech_to_text()

        mock_audio.assert_called_once()

    @patch("pages.speech_to_text.show_transcripts")
    @patch("pages.speech_to_text.show_export_transcripts")
    @patch("pages.speech_to_text.show_transcript_stats")
    @patch("pages.speech_to_text.show_transcript_dashboard")
    @patch("pages.speech_to_text.st.divider")
    @patch("pages.speech_to_text.st.text_area")
    @patch("pages.speech_to_text.st.success")
    @patch("pages.speech_to_text.SpeechService.transcribe")
    @patch("pages.speech_to_text.st.empty")
    @patch("pages.speech_to_text.st.progress")
    @patch("pages.speech_to_text.st.button")
    @patch("pages.speech_to_text.st.audio")
    @patch("pages.speech_to_text.os.path.exists")
    @patch("pages.speech_to_text.st.columns")
    @patch("pages.speech_to_text.TranscriptUtils.read_transcript")
    @patch("pages.speech_to_text.TranscriptUtils.list_transcripts")
    @patch("pages.speech_to_text.AudioService.list_audio")
    @patch("pages.speech_to_text.st.selectbox")
    def test_transcribe_returns_none(
            self,
            mock_selectbox,
            mock_list_audio,
            mock_list_transcripts,
            mock_read,
            mock_columns,
            mock_exists,
            mock_audio,
            mock_button,
            mock_progress,
            mock_empty,
            mock_transcribe,
            mock_success,
            mock_text_area,
            mock_divider,
            mock_dashboard,
            mock_stats,
            mock_export,
            mock_transcripts,
    ):
        mock_selectbox.side_effect = [
            "base",
            "sample.mp3",
        ]

        mock_list_audio.side_effect = [
            ["sample.mp3"],
            ["sample.mp3"],
        ]

        mock_list_transcripts.return_value = []

        mock_columns.return_value = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        mock_exists.return_value = True

        mock_button.return_value = True

        mock_transcribe.return_value = None

        show_speech_to_text()

        mock_success.assert_not_called()

        mock_text_area.assert_not_called()

        mock_dashboard.assert_called_once()

        mock_stats.assert_called_once()

        mock_export.assert_called_once()

        mock_transcripts.assert_called_once()

    @patch("pages.speech_to_text.show_transcripts")
    @patch("pages.speech_to_text.show_export_transcripts")
    @patch("pages.speech_to_text.show_transcript_stats")
    @patch("pages.speech_to_text.show_transcript_dashboard")
    @patch("pages.speech_to_text.st.divider")
    @patch("pages.speech_to_text.st.audio")
    @patch("pages.speech_to_text.os.path.exists")
    @patch("pages.speech_to_text.st.columns")
    @patch("pages.speech_to_text.TranscriptUtils.read_transcript")
    @patch("pages.speech_to_text.TranscriptUtils.list_transcripts")
    @patch("pages.speech_to_text.AudioService.list_audio")
    @patch("pages.speech_to_text.st.button")
    @patch("pages.speech_to_text.st.selectbox")
    def test_audio_file_missing(
            self,
            mock_selectbox,
            mock_button,
            mock_list_audio,
            mock_list_transcripts,
            mock_read,
            mock_columns,
            mock_exists,
            mock_audio,
            mock_divider,
            mock_dashboard,
            mock_stats,
            mock_export,
            mock_transcripts,
    ):
        mock_selectbox.side_effect = [
            "base",
            "sample.mp3",
        ]

        mock_list_audio.side_effect = [
            ["sample.mp3"],
            ["sample.mp3"],
        ]

        mock_list_transcripts.return_value = []

        mock_columns.return_value = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        mock_exists.return_value = False

        mock_button.return_value = False

        show_speech_to_text()

        mock_audio.assert_not_called()

        mock_dashboard.assert_called_once()

        mock_stats.assert_called_once()

        mock_export.assert_called_once()

        mock_transcripts.assert_called_once()



    @patch("pages.speech_to_text.show_transcripts")
    @patch("pages.speech_to_text.show_export_transcripts")
    @patch("pages.speech_to_text.show_transcript_stats")
    @patch("pages.speech_to_text.show_transcript_dashboard")
    @patch("pages.speech_to_text.st.divider")
    @patch("pages.speech_to_text.st.text_area")
    @patch("pages.speech_to_text.st.success")
    @patch("pages.speech_to_text.SpeechService.transcribe")
    @patch("pages.speech_to_text.st.empty")
    @patch("pages.speech_to_text.st.progress")
    @patch("pages.speech_to_text.st.button")
    @patch("pages.speech_to_text.st.audio")
    @patch("pages.speech_to_text.os.path.exists")
    @patch("pages.speech_to_text.st.columns")
    @patch("pages.speech_to_text.TranscriptUtils.read_transcript")
    @patch("pages.speech_to_text.TranscriptUtils.list_transcripts")
    @patch("pages.speech_to_text.AudioService.list_audio")
    @patch("pages.speech_to_text.st.selectbox")
    def test_transcribe_arguments(
            self,
            mock_selectbox,
            mock_list_audio,
            mock_list_transcripts,
            mock_read,
            mock_columns,
            mock_exists,
            mock_audio,
            mock_button,
            mock_progress,
            mock_empty,
            mock_transcribe,
            mock_success,
            mock_text_area,
            mock_divider,
            mock_dashboard,
            mock_stats,
            mock_export,
            mock_transcripts,
    ):
        mock_selectbox.side_effect = [
            "medium",
            "lecture.mp3",
        ]

        mock_list_audio.side_effect = [
            ["lecture.mp3"],
            ["lecture.mp3"],
        ]

        mock_list_transcripts.return_value = []

        mock_columns.return_value = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        mock_exists.return_value = True

        mock_button.return_value = True

        progress = mock_progress.return_value
        status = mock_empty.return_value

        mock_transcribe.return_value = "Transcript"

        show_speech_to_text()

        mock_transcribe.assert_called_once_with(
            os.path.join("audio", "lecture.mp3"),
            progress,
            status,
            "medium",
        )

    @patch("pages.speech_to_text.show_transcripts")
    @patch("pages.speech_to_text.show_export_transcripts")
    @patch("pages.speech_to_text.show_transcript_stats")
    @patch("pages.speech_to_text.show_transcript_dashboard")
    @patch("pages.speech_to_text.st.divider")
    @patch("pages.speech_to_text.st.button")
    @patch("pages.speech_to_text.st.audio")
    @patch("pages.speech_to_text.os.path.exists")
    @patch("pages.speech_to_text.st.columns")
    @patch("pages.speech_to_text.TranscriptUtils.read_transcript")
    @patch("pages.speech_to_text.TranscriptUtils.list_transcripts")
    @patch("pages.speech_to_text.AudioService.list_audio")
    @patch("pages.speech_to_text.st.selectbox")
    def test_audio_exists_preview_only(
            self,
            mock_selectbox,
            mock_list_audio,
            mock_list_transcripts,
            mock_read,
            mock_columns,
            mock_exists,
            mock_audio,
            mock_button,
            mock_divider,
            mock_dashboard,
            mock_stats,
            mock_export,
            mock_transcripts,
    ):
        mock_selectbox.side_effect = [
            "base",
            "sample.mp3",
        ]

        mock_list_audio.side_effect = [
            ["sample.mp3"],
            ["sample.mp3"],
        ]

        mock_list_transcripts.return_value = []

        mock_columns.return_value = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        mock_exists.return_value = True

        mock_button.return_value = False

        show_speech_to_text()

        mock_audio.assert_called_once_with(
            os.path.join("audio", "sample.mp3")
        )

        mock_dashboard.assert_called_once()
        mock_stats.assert_called_once()
        mock_export.assert_called_once()
        mock_transcripts.assert_called_once()