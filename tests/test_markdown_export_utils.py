from unittest.mock import mock_open, patch

from utils.markdown_export import export_markdown


class TestMarkdownExportUtils:

    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.markdown_export.os.makedirs")
    @patch("utils.markdown_export.os.path.dirname")
    def test_export_markdown_success(
        self,
        mock_dirname,
        mock_makedirs,
        mock_file,
    ):
        mock_dirname.return_value = "exports"

        report = "# Report\n\nHello World"

        export_markdown(
            report,
            "exports/report.md",
        )

        mock_dirname.assert_called_once_with(
            "exports/report.md"
        )

        mock_makedirs.assert_called_once_with(
            "exports",
            exist_ok=True,
        )

        mock_file.assert_called_once_with(
            "exports/report.md",
            "w",
            encoding="utf-8",
        )

        mock_file().write.assert_called_once_with(
            report
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.markdown_export.os.makedirs")
    @patch("utils.markdown_export.os.path.dirname")
    def test_export_markdown_empty_report(
        self,
        mock_dirname,
        mock_makedirs,
        mock_file,
    ):
        mock_dirname.return_value = "exports"

        export_markdown(
            "",
            "exports/report.md",
        )

        mock_file().write.assert_called_once_with(
            ""
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.markdown_export.os.makedirs")
    @patch("utils.markdown_export.os.path.dirname")
    def test_export_markdown_directory_creation(
        self,
        mock_dirname,
        mock_makedirs,
        mock_file,
    ):
        mock_dirname.return_value = "reports"

        export_markdown(
            "Sample Report",
            "reports/output.md",
        )

        mock_makedirs.assert_called_once_with(
            "reports",
            exist_ok=True,
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.markdown_export.os.makedirs")
    @patch("utils.markdown_export.os.path.dirname")
    def test_export_markdown_preserves_content(
        self,
        mock_dirname,
        mock_makedirs,
        mock_file,
    ):
        mock_dirname.return_value = "exports"

        report = (
            "# Title\n\n"
            "- Item 1\n"
            "- Item 2\n\n"
            "**Bold Text**"
        )

        export_markdown(
            report,
            "exports/report.md",
        )

        mock_file().write.assert_called_once_with(
            report
        )