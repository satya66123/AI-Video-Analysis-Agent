from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from services.export_service import ExportService


class TestExportService:

    @patch.object(ExportService, "create_export_folder")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_txt(
        self,
        mock_file,
        mock_folder,
    ):
        path = ExportService.save_txt(
            "report",
            "Hello",
        )

        expected = Path("exports") / "report.txt"

        assert path == expected

        mock_file.assert_called_once_with(
            expected,
            "w",
            encoding="utf-8",
        )

        mock_file().write.assert_called_once_with(
            "Hello"
        )

    @patch.object(ExportService, "create_export_folder")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_md(
        self,
        mock_file,
        mock_folder,
    ):
        path = ExportService.save_md(
            "report",
            "Markdown",
        )

        expected = Path("exports") / "report.md"

        assert path == expected

        mock_file().write.assert_called_once_with(
            "Markdown"
        )

    @patch.object(ExportService, "create_export_folder")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_html(
        self,
        mock_file,
        mock_folder,
    ):
        path = ExportService.save_html(
            "report",
            "Content",
        )

        expected = Path("exports") / "report.html"

        assert path == expected

        written = mock_file().write.call_args.args[0]

        assert "<html>" in written
        assert "Content" in written
        assert "</html>" in written

    @patch.object(ExportService, "create_export_folder")
    @patch("services.export_service.SimpleDocTemplate")
    @patch("services.export_service.Paragraph")
    @patch("services.export_service.getSampleStyleSheet")
    def test_save_pdf(
        self,
        mock_styles,
        mock_paragraph,
        mock_doc,
        mock_folder,
    ):
        styles = {
            "BodyText": MagicMock()
        }

        mock_styles.return_value = styles

        doc = MagicMock()
        mock_doc.return_value = doc

        path = ExportService.save_pdf(
            "report",
            "Line1\nLine2",
        )

        expected = Path("exports") / "report.pdf"

        assert path == expected

        assert mock_paragraph.call_count == 2

        doc.build.assert_called_once()

    @patch("pathlib.Path.mkdir")
    def test_create_export_folder(self, mock_mkdir):
        ExportService.create_export_folder()

        mock_mkdir.assert_called_once_with(exist_ok=True)

    @patch("services.export_service.datetime")
    def test_generate_filename(
        self,
        mock_datetime,
    ):
        mock_datetime.now.return_value.strftime.return_value = (
            "20260101_120000"
        )

        result = ExportService.generate_filename(
            "My Video.mp4"
        )

        assert (
            result
            == "My_Video_video_report_20260101_120000"
        )