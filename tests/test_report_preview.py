import json
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import streamlit as st

from components.report_preview import show_report_preview


class TestReportPreviewComponent:

    def _mock_tabs(self):
        tabs = []
        for _ in range(8):
            tab = MagicMock()
            tab.__enter__.return_value = tab
            tab.__exit__.return_value = None
            tabs.append(tab)
        return tabs

    def _mock_columns(self, count):
        cols = []
        for _ in range(count):
            col = MagicMock()
            col.__enter__.return_value = col
            col.__exit__.return_value = None
            cols.append(col)
        return cols

    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_video_tab_no_videos(
        self,
        mock_path,
        mock_st,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        upload_folder.glob.return_value = []

        audio_folder.glob.return_value = []
        transcript_folder.glob.return_value = []
        analysis_folder.glob.return_value = []
        chat_folder.glob.return_value = []

        upload_folder.iterdir.return_value = []
        audio_folder.iterdir.return_value = []
        transcript_folder.iterdir.return_value = []
        analysis_folder.iterdir.return_value = []
        chat_folder.iterdir.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        mock_st.columns.side_effect = [
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(5),
            self._mock_columns(2),
        ]

        mock_st.checkbox.return_value = True
        mock_st.button.return_value = False
        mock_st.session_state = {}

        show_report_preview()

        upload_folder.mkdir.assert_called_once_with(
            exist_ok=True
        )

        mock_st.warning.assert_any_call(
            "No videos found in uploads folder."
        )

    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_audio_tab_no_audio(
        self,
        mock_path,
        mock_st,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        upload_folder.glob.return_value = [Path("video.mp4")]
        audio_folder.glob.return_value = []
        transcript_folder.glob.return_value = []
        analysis_folder.glob.return_value = []
        chat_folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        mock_st.columns.side_effect = [
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(5),
            self._mock_columns(2),
        ]

        mock_st.selectbox.return_value = Path("video.mp4")

        mock_st.session_state = {}

        with patch(
            "components.report_preview.MetadataService.get_video_metadata",
            return_value={
                "filename": "video.mp4",
                "duration": "10 sec",
                "resolution": "1920x1080",
                "fps": 30,
                "format": "mp4",
                "size": "10 MB",
            },
        ):
            mock_st.checkbox.return_value = True
            mock_st.button.return_value = False

            show_report_preview()

        mock_st.warning.assert_any_call(
            "No audio files found."
        )

    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_transcript_tab_no_transcripts(
        self,
        mock_path,
        mock_st,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        upload_folder.glob.return_value = [Path("video.mp4")]
        audio_folder.glob.return_value = [Path("audio.wav")]
        transcript_folder.glob.return_value = []
        analysis_folder.glob.return_value = []
        chat_folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        mock_st.columns.side_effect = [
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(5),
            self._mock_columns(2),
        ]

        mock_st.selectbox.side_effect = [
            Path("video.mp4"),
            Path("audio.wav"),
        ]

        mock_st.session_state = {}

        with patch(
            "components.report_preview.MetadataService.get_video_metadata",
            return_value={
                "filename": "video.mp4",
                "duration": "10",
                "resolution": "1920x1080",
                "fps": 30,
                "format": "mp4",
                "size": "10 MB",
            },
        ), patch(
            "components.report_preview.MetadataService.get_audio_metadata",
            return_value={
                "duration": "10",
                "channels": 2,
                "sample_rate": 44100,
            },
        ), patch.object(
            Path,
            "stat",
            return_value=MagicMock(st_size=1048576),
        ):
            mock_st.checkbox.return_value = True
            mock_st.button.return_value = False

            show_report_preview()

        mock_st.warning.assert_any_call(
            "No transcript files found."
        )

    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_analysis_tab_no_reports(
        self,
        mock_path,
        mock_st,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        upload_folder.glob.return_value = [Path("video.mp4")]
        audio_folder.glob.return_value = [Path("audio.wav")]
        transcript_folder.glob.return_value = [Path("text.txt")]
        analysis_folder.glob.return_value = []
        chat_folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        mock_st.columns.side_effect = [
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(5),
            self._mock_columns(2),
        ]

        transcript = MagicMock(spec=Path)
        transcript.name = "text.txt"
        transcript.read_text.return_value = "sample transcript"

        mock_st.selectbox.side_effect = [
            Path("video.mp4"),
            Path("audio.wav"),
            transcript,
        ]

        mock_st.session_state = {}

        with patch(
            "components.report_preview.MetadataService.get_video_metadata",
            return_value={
                "filename": "video.mp4",
                "duration": "10",
                "resolution": "1920x1080",
                "fps": 30,
                "format": "mp4",
                "size": "10 MB",
            },
        ), patch(
            "components.report_preview.MetadataService.get_audio_metadata",
            return_value={
                "duration": "10",
                "channels": 2,
                "sample_rate": 44100,
            },
        ), patch.object(
            Path,
            "stat",
            return_value=MagicMock(st_size=1048576),
        ):
            mock_st.checkbox.return_value = True
            mock_st.button.return_value = False

            show_report_preview()

        mock_st.warning.assert_any_call(
            "No analysis reports found."
        )

    @patch("builtins.open", new_callable=mock_open, read_data='[{"role":"user","content":"hello"}]')
    @patch("components.report_preview.json.load")
    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_chat_tab_success(
        self,
        mock_path,
        mock_st,
        mock_export_center,
        mock_json_load,
        mock_file,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        video = Path("video.mp4")
        audio = Path("audio.wav")
        transcript = Path("transcript.txt")
        analysis = Path("analysis.md")
        chat = Path("chat.json")

        video = MagicMock(spec=Path)
        video.name = "video.mp4"

        audio = MagicMock(spec=Path)
        audio.name = "audio.wav"
        audio.suffix = ".wav"
        audio.stat.return_value.st_size = 1048576

        transcript = MagicMock(spec=Path)
        transcript.name = "transcript.txt"
        transcript.read_text.return_value = "Transcript"

        analysis = MagicMock(spec=Path)
        analysis.name = "analysis.md"
        analysis.read_text.return_value = "# Analysis"

        chat = MagicMock(spec=Path)
        chat.name = "chat.json"

        upload_folder.glob.return_value = [video]
        audio_folder.glob.return_value = [audio]
        transcript_folder.glob.return_value = [transcript]
        analysis_folder.glob.return_value = [analysis]
        chat_folder.glob.return_value = [chat]

        mock_st.tabs.return_value = self._mock_tabs()

        mock_st.columns.side_effect = [
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(5),
            self._mock_columns(2),
        ]

        mock_st.selectbox.side_effect = [
            video,
            audio,
            transcript,
            analysis,
            chat,
        ]

        mock_json_load.return_value = [
            {
                "role": "user",
                "content": "hello",
            }
        ]

        mock_st.checkbox.return_value = True
        mock_st.button.return_value = False

        mock_st.session_state = {
            "provider": "Ollama",
            "model": "qwen2.5",
        }

        with patch(
            "components.report_preview.MetadataService.get_video_metadata",
            return_value={
                "filename": "video.mp4",
                "duration": "10 sec",
                "resolution": "1920x1080",
                "fps": 30,
                "format": "mp4",
                "size": "1 MB",
            },
        ), patch(
            "components.report_preview.MetadataService.get_audio_metadata",
            return_value={
                "filename": "audio.wav",
                "duration": "10 sec",
                "channels": 2,
                "sample_rate": 44100,
                "format": "wav",
                "size": "2 MB",
            },
        ), patch.object(
            Path,
            "stat",
            return_value=MagicMock(
                st_size=1048576
            ),
        ):

            show_report_preview()

        assert (
            mock_st.session_state["report_video_metadata"][
                "filename"
            ]
            == "video.mp4"
        )

        assert (
            mock_st.session_state["report_audio_metadata"][
                "duration"
            ]
            == "10 sec"
        )

        assert (
            mock_st.session_state[
                "report_transcript"
            ]
            == "Transcript"
        )

        assert (
            mock_st.session_state[
                "report_analysis"
            ]
            == "# Analysis"
        )

        assert (
            mock_st.session_state[
                "report_chat"
            ]
            == [
                {
                    "role": "user",
                    "content": "hello",
                }
            ]
        )

        mock_st.json.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    @patch("components.report_preview.json.load")
    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_metadata_tab_provider_model(
        self,
        mock_path,
        mock_st,
        mock_export_center,
        mock_json_load,
        mock_file,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        video = MagicMock(spec=Path)
        video.name = "video.mp4"

        audio = MagicMock(spec=Path)
        audio.name = "audio.wav"
        audio.suffix = ".wav"
        audio.stat.return_value.st_size = 1048576

        transcript = MagicMock(spec=Path)
        transcript.name = "transcript.txt"
        transcript.read_text.return_value = "Transcript"

        analysis = MagicMock(spec=Path)
        analysis.name = "analysis.md"
        analysis.read_text.return_value = "Analysis"

        chat = MagicMock(spec=Path)
        chat.name = "chat.json"

        upload_folder.glob.return_value = [video]
        audio_folder.glob.return_value = [audio]
        transcript_folder.glob.return_value = [transcript]
        analysis_folder.glob.return_value = [analysis]
        chat_folder.glob.return_value = [chat]

        mock_st.tabs.return_value = self._mock_tabs()

        mock_st.columns.side_effect = [
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(5),
            self._mock_columns(2),
        ]

        mock_st.selectbox.side_effect = [
            video,
            audio,
            transcript,
            analysis,
            chat,
        ]

        mock_st.checkbox.return_value = True
        mock_st.button.return_value = False

        mock_st.session_state = {
            "provider": "OpenAI",
            "model": "gpt",
        }

        mock_json_load.return_value = []

        with patch(
            "components.report_preview.MetadataService.get_video_metadata",
            return_value={
                "filename": "video.mp4",
                "duration": "10",
                "resolution": "1080p",
                "fps": 30,
                "format": "mp4",
                "size": "1 MB",
            },
        ), patch(
            "components.report_preview.MetadataService.get_audio_metadata",
            return_value={
                "filename": "audio.wav",
                "duration": "10",
                "channels": 2,
                "sample_rate": 44100,
                "format": "wav",
                "size": "2 MB",
            },
        ), patch.object(
            Path,
            "stat",
            return_value=MagicMock(
                st_size=1048576
            ),
        ):

            show_report_preview()

        mock_st.text_input.assert_any_call(
            "Provider",
            "OpenAI",
            disabled=True,
            key="rp_provider",
        )

        mock_st.text_input.assert_any_call(
            "Model",
            "gpt",
            disabled=True,
            key="rp_model",
        )

    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.ExportService.generate_filename")
    @patch("components.report_preview.ReportService.generate_complete_report")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_generate_report_success(
        self,
        mock_path,
        mock_st,
        mock_generate_report,
        mock_generate_filename,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        upload_folder.glob.return_value = []
        audio_folder.glob.return_value = []
        transcript_folder.glob.return_value = []
        analysis_folder.glob.return_value = []
        chat_folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        def columns_side_effect(n):
            return self._mock_columns(n)

        mock_st.columns.side_effect = columns_side_effect

        mock_st.checkbox.return_value = True

        def button_side_effect(*args, **kwargs):
            return kwargs.get("key") == "rp_generate"

        mock_st.button.side_effect = [
            True,  # Generate
            False,  # PDF
            False,  # Markdown
            False,  # HTML
            False,  # TXT
        ]

        mock_generate_filename.return_value = (
            "report_001"
        )

        mock_generate_report.return_value = (
            "# Generated Report"
        )

        mock_st.session_state = {
            "report_video_metadata": {
                "filename": "video.mp4",
                "duration": "20 sec",
                "resolution": "1920x1080",
                "fps": 30,
                "format": "mp4",
                "size": "5 MB",
            },
            "report_audio_metadata": {
                "filename": "audio.wav",
                "duration": "20 sec",
                "channels": 2,
                "sample_rate": 44100,
                "format": "wav",
                "size": "2 MB",
            },
            "report_transcript": "Transcript",
            "report_analysis": "Analysis",
            "report_chat": [
                {
                    "role": "user",
                    "content": "Hello",
                }
            ],
            "provider": "Ollama",
            "model": "qwen2.5",
        }

        show_report_preview()

        mock_generate_filename.assert_called_once_with(
            "video.mp4"
        )

        mock_generate_report.assert_called_once()

        assert (
            mock_st.session_state[
                "export_filename"
            ]
            == "report_001"
        )

        assert (
            mock_st.session_state[
                "generated_report"
            ]
            == "# Generated Report"
        )

        mock_st.success.assert_any_call(
            "✅ Report generated successfully!"
        )

    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.ExportService.generate_filename")
    @patch("components.report_preview.ReportService.generate_complete_report")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_generate_report_default_video_name(
        self,
        mock_path,
        mock_st,
        mock_generate_report,
        mock_generate_filename,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        upload_folder.glob.return_value = []
        audio_folder.glob.return_value = []
        transcript_folder.glob.return_value = []
        analysis_folder.glob.return_value = []
        chat_folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        def columns_side_effect(n):
            return self._mock_columns(n)

        mock_st.columns.side_effect = columns_side_effect

        mock_st.checkbox.return_value = True

        mock_st.button.side_effect = [
            True,  # Generate
            False,  # PDF
            False,  # Markdown
            False,  # HTML
            False,  # TXT
        ]

        mock_generate_filename.return_value = (
            "generated"
        )

        mock_generate_report.return_value = (
            "Report"
        )

        mock_st.session_state = {
            "report_video_metadata": {},
            "report_audio_metadata": {},
        }

        show_report_preview()

        mock_generate_filename.assert_called_once_with(
            "video"
        )

        assert (
            mock_st.session_state[
                "generated_report"
            ]
            == "Report"
        )

    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.ExportService.generate_filename")
    @patch("components.report_preview.ReportService.generate_complete_report")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_generated_report_preview_displayed(
        self,
        mock_path,
        mock_st,
        mock_generate_report,
        mock_generate_filename,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        upload_folder.glob.return_value = []
        audio_folder.glob.return_value = []
        transcript_folder.glob.return_value = []
        analysis_folder.glob.return_value = []
        chat_folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        def columns_side_effect(n):
            return self._mock_columns(n)

        mock_st.columns.side_effect = columns_side_effect

        mock_st.checkbox.return_value = True

        def button_side_effect(*args, **kwargs):
            return kwargs.get("key") == "rp_generate"

        mock_st.button.side_effect = button_side_effect

        mock_generate_filename.return_value = (
            "report"
        )

        mock_generate_report.return_value = (
            "# Report Content"
        )

        mock_st.session_state = {
            "report_video_metadata": {},
            "report_audio_metadata": {},
        }

        show_report_preview()

        mock_st.markdown.assert_any_call(
            "# Report Content"
        )

        mock_st.subheader.assert_any_call(
            "📖 Generated Report Preview"
        )
    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.ExportService.save_pdf")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_pdf_export_success(
        self,
        mock_path,
        mock_st,
        mock_save_pdf,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        for folder in (
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ):
            folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        def columns_side_effect(n):
            return self._mock_columns(n)

        mock_st.columns.side_effect = columns_side_effect

        mock_st.checkbox.return_value = True

        mock_st.button.side_effect = [
            True,  # Generate
            True,  # PDF
            False,
            False,
            False,
        ]


        mock_st.session_state = {
            "generated_report": "# Report",
            "export_filename": "sample",
        }

        mock_save_pdf.return_value = Path(
            "exports/sample.pdf"
        )

        show_report_preview()

        mock_save_pdf.assert_called_once()

        args = mock_save_pdf.call_args.args

        assert args[0].startswith("video_")
        assert "AI Video Analyzer Report" in args[1]

        mock_st.success.assert_any_call(
            "✅ PDF saved successfully!"
        )

        path = mock_st.code.call_args.args[0]

        assert Path(path) == Path("exports/sample.pdf")

    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.ExportService.save_md")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_markdown_export_success(
        self,
        mock_path,
        mock_st,
        mock_save_md,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        for folder in (
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ):
            folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        def columns_side_effect(n):
            return self._mock_columns(n)

        mock_st.columns.side_effect = columns_side_effect

        mock_st.checkbox.return_value = True

        mock_st.button.side_effect = [
            True,
            False,
            True,
            False,
            False,
        ]

        mock_st.session_state = {
            "generated_report": "# Report",
            "export_filename": "sample",
        }

        mock_save_md.return_value = Path(
            "exports/sample.md"
        )

        show_report_preview()

        mock_save_md.assert_called_once()

        args = mock_save_md.call_args.args

        assert args[0].startswith("video_")
        assert "AI Video Analyzer Report" in args[1]

        mock_st.success.assert_any_call(
            "✅ Markdown saved successfully!"
        )

    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.ExportService.save_html")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_html_export_success(
        self,
        mock_path,
        mock_st,
        mock_save_html,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        for folder in (
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ):
            folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        def columns_side_effect(n):
            return self._mock_columns(n)

        mock_st.columns.side_effect = columns_side_effect

        mock_st.checkbox.return_value = True

        mock_st.button.side_effect = [
            True,
            False,
            False,
            True,
            False,
        ]

        mock_st.session_state = {
            "generated_report": "# Report",
            "export_filename": "sample",
        }

        mock_save_html.return_value = Path(
            "exports/sample.html"
        )

        show_report_preview()

        mock_save_html.assert_called_once()

        args = mock_save_html.call_args.args

        assert args[0].startswith("video_")
        assert "AI Video Analyzer Report" in args[1]

        mock_st.success.assert_any_call(
            "✅ HTML saved successfully!"
        )

    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.ExportService.save_txt")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_txt_export_success(
        self,
        mock_path,
        mock_st,
        mock_save_txt,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        for folder in (
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ):
            folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        def columns_side_effect(n):
            return self._mock_columns(n)

        mock_st.columns.side_effect = columns_side_effect

        mock_st.checkbox.return_value = True

        mock_st.button.side_effect = [
            True,
            False,
            False,
            False,
            True,
        ]

        mock_st.session_state = {
            "generated_report": "# Report",
            "export_filename": "sample",
        }

        mock_save_txt.return_value = Path(
            "exports/sample.txt"
        )

        show_report_preview()

        mock_save_txt.assert_called_once()

        args = mock_save_txt.call_args.args

        assert args[0].startswith("video_")
        assert "AI Video Analyzer Report" in args[1]

        mock_st.success.assert_any_call(
            "✅ TXT saved successfully!"
        )

        path = mock_st.code.call_args.args[0]

        assert Path(path) == Path("exports/sample.txt")



    @patch("components.report_preview.show_export_center")
    @patch("components.report_preview.st")
    @patch("components.report_preview.Path")
    def test_export_center_called(
        self,
        mock_path,
        mock_st,
        mock_export_center,
    ):
        upload_folder = MagicMock()
        audio_folder = MagicMock()
        transcript_folder = MagicMock()
        analysis_folder = MagicMock()
        chat_folder = MagicMock()

        mock_path.side_effect = [
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ]

        for folder in (
            upload_folder,
            audio_folder,
            transcript_folder,
            analysis_folder,
            chat_folder,
        ):
            folder.glob.return_value = []

        mock_st.tabs.return_value = self._mock_tabs()

        mock_st.columns.side_effect = [
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(2),
            self._mock_columns(5),
            self._mock_columns(2),
        ]

        mock_st.checkbox.return_value = True
        mock_st.button.return_value = False
        mock_st.session_state = {}

        show_report_preview()

        mock_export_center.assert_called_once()