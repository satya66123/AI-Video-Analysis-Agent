from unittest.mock import MagicMock, patch

from utils.pdf_export import export_pdf


class TestPdfExportUtils:

    @patch("utils.pdf_export.Spacer")
    @patch("utils.pdf_export.Paragraph")
    @patch("utils.pdf_export.getSampleStyleSheet")
    @patch("utils.pdf_export.SimpleDocTemplate")
    @patch("utils.pdf_export.os.makedirs")
    @patch("utils.pdf_export.os.path.dirname")
    def test_export_pdf_success(
        self,
        mock_dirname,
        mock_makedirs,
        mock_doc_class,
        mock_styles,
        mock_paragraph,
        mock_spacer,
    ):
        mock_dirname.return_value = "exports"

        styles = {
            "Heading1": MagicMock(),
            "Heading2": MagicMock(),
            "BodyText": MagicMock(),
        }

        mock_styles.return_value = styles

        mock_doc = MagicMock()
        mock_doc_class.return_value = mock_doc

        mock_paragraph.side_effect = (
            lambda text, style: f"P:{text}"
        )

        mock_spacer.side_effect = (
            lambda *args: "Spacer"
        )

        report = (
            "# Title\n"
            "## Section\n"
            "Body text"
        )

        export_pdf(
            report,
            "exports/report.pdf",
        )

        mock_makedirs.assert_called_once_with(
            "exports",
            exist_ok=True,
        )

        mock_doc_class.assert_called_once()

        mock_doc.build.assert_called_once()

        story = mock_doc.build.call_args.args[0]

        assert len(story) == 5

    @patch("utils.pdf_export.Spacer")
    @patch("utils.pdf_export.Paragraph")
    @patch("utils.pdf_export.getSampleStyleSheet")
    @patch("utils.pdf_export.SimpleDocTemplate")
    @patch("utils.pdf_export.os.makedirs")
    @patch("utils.pdf_export.os.path.dirname")
    def test_export_pdf_empty_report(
        self,
        mock_dirname,
        mock_makedirs,
        mock_doc_class,
        mock_styles,
        mock_paragraph,
        mock_spacer,
    ):
        mock_dirname.return_value = "exports"

        styles = {
            "Heading1": MagicMock(),
            "Heading2": MagicMock(),
            "BodyText": MagicMock(),
        }

        mock_styles.return_value = styles

        mock_doc = MagicMock()
        mock_doc_class.return_value = mock_doc

        mock_paragraph.side_effect = (
            lambda text, style: text
        )

        mock_spacer.side_effect = (
            lambda *args: "Spacer"
        )

        export_pdf(
            "",
            "exports/report.pdf",
        )

        mock_doc.build.assert_called_once()

        story = mock_doc.build.call_args.args[0]

        # Title + initial spacer only
        assert len(story) == 2

    @patch("utils.pdf_export.Spacer")
    @patch("utils.pdf_export.Paragraph")
    @patch("utils.pdf_export.getSampleStyleSheet")
    @patch("utils.pdf_export.SimpleDocTemplate")
    @patch("utils.pdf_export.os.makedirs")
    @patch("utils.pdf_export.os.path.dirname")
    def test_export_pdf_blank_lines(
        self,
        mock_dirname,
        mock_makedirs,
        mock_doc_class,
        mock_styles,
        mock_paragraph,
        mock_spacer,
    ):
        mock_dirname.return_value = "exports"

        styles = {
            "Heading1": MagicMock(),
            "Heading2": MagicMock(),
            "BodyText": MagicMock(),
        }

        mock_styles.return_value = styles

        mock_doc = MagicMock()
        mock_doc_class.return_value = mock_doc

        mock_paragraph.side_effect = (
            lambda text, style: text
        )

        mock_spacer.side_effect = (
            lambda *args: "Spacer"
        )

        report = (
            "# Title\n\n"
            "Body"
        )

        export_pdf(
            report,
            "exports/report.pdf",
        )

        story = mock_doc.build.call_args.args[0]

        assert "Spacer" in story

    @patch("utils.pdf_export.Spacer")
    @patch("utils.pdf_export.Paragraph")
    @patch("utils.pdf_export.getSampleStyleSheet")
    @patch("utils.pdf_export.SimpleDocTemplate")
    @patch("utils.pdf_export.os.makedirs")
    @patch("utils.pdf_export.os.path.dirname")
    def test_export_pdf_body_only(
        self,
        mock_dirname,
        mock_makedirs,
        mock_doc_class,
        mock_styles,
        mock_paragraph,
        mock_spacer,
    ):
        mock_dirname.return_value = "exports"

        styles = {
            "Heading1": MagicMock(),
            "Heading2": MagicMock(),
            "BodyText": MagicMock(),
        }

        mock_styles.return_value = styles

        mock_doc = MagicMock()
        mock_doc_class.return_value = mock_doc

        mock_paragraph.side_effect = (
            lambda text, style: text
        )

        mock_spacer.side_effect = (
            lambda *args: "Spacer"
        )

        export_pdf(
            "Only body text",
            "exports/report.pdf",
        )

        story = mock_doc.build.call_args.args[0]

        assert "Only body text" in story