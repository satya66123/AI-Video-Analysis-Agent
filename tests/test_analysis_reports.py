from unittest.mock import MagicMock, patch

from components.analysis_reports import show_analysis_reports


class TestAnalysisReports:

    @patch("components.analysis_reports.st.subheader")
    @patch("components.analysis_reports.show_file_browser")
    def test_show_analysis_reports_no_file(
        self,
        mock_show_file_browser,
        mock_subheader,
    ):
        mock_show_file_browser.return_value = None

        show_analysis_reports()

        mock_subheader.assert_called_once_with(
            "🤖 AI Analysis Reports"
        )

        mock_show_file_browser.assert_called_once_with(
            folder="analysis",
            extension=".md",
            key="analysis_browser",
        )

    @patch("components.analysis_reports.st.download_button")
    @patch("components.analysis_reports.st.markdown")
    @patch("components.analysis_reports.st.divider")
    @patch("components.analysis_reports.st.columns")
    @patch("components.analysis_reports.st.subheader")
    @patch("components.analysis_reports.show_file_browser")
    def test_show_analysis_reports_with_file(
        self,
        mock_show_file_browser,
        mock_subheader,
        mock_columns,
        mock_divider,
        mock_markdown,
        mock_download_button,
    ):
        mock_file = MagicMock()
        mock_file.name = "report.md"
        mock_file.stem = "report"

        mock_file.read_text.return_value = (
            "This is a sample report."
        )

        stat = MagicMock()
        stat.st_size = 4096
        stat.st_mtime = 123456789

        mock_file.stat.return_value = stat

        mock_show_file_browser.return_value = mock_file

        metric1 = MagicMock()
        metric2 = MagicMock()
        metric3 = MagicMock()

        download_col1 = MagicMock()
        download_col2 = MagicMock()

        download_col1.__enter__.return_value = download_col1
        download_col1.__exit__.return_value = False

        download_col2.__enter__.return_value = download_col2
        download_col2.__exit__.return_value = False

        mock_columns.side_effect = [
            (metric1, metric2, metric3),
            (download_col1, download_col2),
        ]

        show_analysis_reports()

        mock_subheader.assert_called_once_with(
            "🤖 AI Analysis Reports"
        )

        mock_file.read_text.assert_called_once_with(
            encoding="utf-8"
        )

        metric1.metric.assert_called_once_with(
            "File",
            "report.md",
        )

        metric2.metric.assert_called_once_with(
            "Size",
            "4.00 KB",
        )

        metric3.metric.assert_called_once_with(
            "Words",
            5,
        )

        assert mock_divider.call_count == 2

        mock_markdown.assert_any_call(
            "### 📖 Report Preview"
        )

        mock_markdown.assert_any_call(
            "This is a sample report."
        )

        assert mock_download_button.call_count == 2

        mock_download_button.assert_any_call(
            "⬇ Download Markdown",
            data="This is a sample report.",
            file_name="report.md",
            mime="text/markdown",
            use_container_width=True,
        )

        mock_download_button.assert_any_call(
            "📄 Download TXT",
            data="This is a sample report.",
            file_name="report.txt",
            mime="text/plain",
            use_container_width=True,
        )