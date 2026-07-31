import html
from unittest.mock import mock_open, patch

from utils.html_export import export_html


class TestHtmlExportUtils:

    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.html_export.os.makedirs")
    @patch("utils.html_export.os.path.dirname")
    def test_export_html_success(
        self,
        mock_dirname,
        mock_makedirs,
        mock_file,
    ):
        mock_dirname.return_value = "exports"

        report = "Hello World"

        export_html(
            report,
            "exports/report.html",
        )

        mock_dirname.assert_called_once_with(
            "exports/report.html"
        )

        mock_makedirs.assert_called_once_with(
            "exports",
            exist_ok=True,
        )

        mock_file.assert_called_once_with(
            "exports/report.html",
            "w",
            encoding="utf-8",
        )

        written = mock_file().write.call_args.args[0]

        assert "<!DOCTYPE html>" in written
        assert "<h1>AI Video Analyzer Report</h1>" in written
        assert "Hello World" in written
        assert "<pre>" in written
        assert "</pre>" in written

    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.html_export.os.makedirs")
    @patch("utils.html_export.os.path.dirname")
    def test_export_html_escapes_html(
        self,
        mock_dirname,
        mock_makedirs,
        mock_file,
    ):
        mock_dirname.return_value = "exports"

        report = "<script>alert('x')</script>"

        export_html(
            report,
            "exports/report.html",
        )

        written = mock_file().write.call_args.args[0]

        assert html.escape(report) in written
        assert report not in written

    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.html_export.os.makedirs")
    @patch("utils.html_export.os.path.dirname")
    def test_export_html_empty_report(
        self,
        mock_dirname,
        mock_makedirs,
        mock_file,
    ):
        mock_dirname.return_value = "exports"

        export_html(
            "",
            "exports/report.html",
        )

        written = mock_file().write.call_args.args[0]

        assert "<pre>" in written
        assert "</pre>" in written

    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.html_export.os.makedirs")
    @patch("utils.html_export.os.path.dirname")
    def test_export_html_calls_makedirs(
        self,
        mock_dirname,
        mock_makedirs,
        mock_file,
    ):
        mock_dirname.return_value = "reports"

        export_html(
            "Report",
            "reports/output.html",
        )

        mock_makedirs.assert_called_once_with(
            "reports",
            exist_ok=True,
        )