# tests/test_download_center.py

from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from components.download_reports import show_download_center


class TestDownloadCenter:

    @patch("components.download_reports.st.info")
    @patch("components.download_reports.Path")
    @patch("components.download_reports.st.subheader")
    def test_show_download_center_empty_folder(
        self,
        mock_subheader,
        mock_path,
        mock_info,
    ):
        folder = MagicMock()
        folder.iterdir.return_value = []
        mock_path.return_value = folder

        show_download_center()

        mock_subheader.assert_called_once_with(
            "📥 Export Center"
        )

        folder.mkdir.assert_called_once_with(
            exist_ok=True
        )

        mock_info.assert_called_once_with(
            "No exported reports found."
        )

    @patch("builtins.open", new_callable=mock_open, read_data=b"dummy")
    @patch("components.download_reports.st.success")
    @patch("components.download_reports.st.download_button")
    @patch("components.download_reports.st.selectbox")
    @patch("components.download_reports.st.divider")
    @patch("components.download_reports.st.markdown")
    @patch("components.download_reports.st.columns")
    @patch("components.download_reports.Path")
    @patch("components.download_reports.st.subheader")
    def test_show_download_center_all_files(
        self,
        mock_subheader,
        mock_path,
        mock_columns,
        mock_markdown,
        mock_divider,
        mock_selectbox,
        mock_download_button,
        mock_success,
        mock_open_file,
    ):
        folder = MagicMock()
        folder.iterdir.return_value = [object()]

        pdf = MagicMock(spec=Path)
        pdf.name = "report.pdf"

        md = MagicMock(spec=Path)
        md.name = "report.md"

        html = MagicMock(spec=Path)
        html.name = "report.html"

        txt = MagicMock(spec=Path)
        txt.name = "report.txt"

        folder.glob.side_effect = [
            [pdf],
            [md],
            [html],
            [txt],
            [pdf],
            [md],
            [html],
            [txt],
        ]

        mock_path.return_value = folder

        metric_cols = [MagicMock() for _ in range(5)]
        download_cols = [MagicMock(), MagicMock()]

        for c in metric_cols + download_cols:
            c.__enter__.return_value = c
            c.__exit__.return_value = False

        mock_columns.side_effect = [
            tuple(metric_cols),
            tuple(download_cols),
        ]

        mock_selectbox.side_effect = [
            pdf,
            md,
            html,
            txt,
        ]

        mock_download_button.side_effect = [
            True,
            True,
            True,
            True,
        ]

        show_download_center()

        metric_cols[0].metric.assert_called_once_with(
            "Total",
            4,
        )

        metric_cols[1].metric.assert_called_once_with(
            "PDF",
            1,
        )

        metric_cols[2].metric.assert_called_once_with(
            "Markdown",
            1,
        )

        metric_cols[3].metric.assert_called_once_with(
            "HTML",
            1,
        )

        metric_cols[4].metric.assert_called_once_with(
            "TXT",
            1,
        )

        assert mock_selectbox.call_count == 4
        assert mock_download_button.call_count == 4
        assert mock_success.call_count == 4

    @patch("components.download_reports.st.info")
    @patch("components.download_reports.st.columns")
    @patch("components.download_reports.st.divider")
    @patch("components.download_reports.st.markdown")
    @patch("components.download_reports.Path")
    @patch("components.download_reports.st.subheader")
    def test_show_download_center_no_export_types(
        self,
        mock_subheader,
        mock_path,
        mock_markdown,
        mock_divider,
        mock_columns,
        mock_info,
    ):
        folder = MagicMock()
        folder.iterdir.return_value = [object()]

        folder.glob.side_effect = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]

        mock_path.return_value = folder

        metric_cols = [MagicMock() for _ in range(5)]
        download_cols = [MagicMock(), MagicMock()]

        for c in metric_cols + download_cols:
            c.__enter__.return_value = c
            c.__exit__.return_value = False

        mock_columns.side_effect = [
            tuple(metric_cols),
            tuple(download_cols),
        ]

        show_download_center()

        metric_cols[0].metric.assert_called_once_with(
            "Total",
            0,
        )

        metric_cols[1].metric.assert_called_once_with(
            "PDF",
            0,
        )

        metric_cols[2].metric.assert_called_once_with(
            "Markdown",
            0,
        )

        metric_cols[3].metric.assert_called_once_with(
            "HTML",
            0,
        )

        metric_cols[4].metric.assert_called_once_with(
            "TXT",
            0,
        )

        assert mock_info.call_count == 4

        mock_info.assert_any_call(
            "No PDF files found."
        )

        mock_info.assert_any_call(
            "No Markdown files found."
        )

        mock_info.assert_any_call(
            "No HTML files found."
        )

        mock_info.assert_any_call(
            "No TXT files found."
        )

    @patch("builtins.open", new_callable=mock_open, read_data=b"dummy")
    @patch("components.download_reports.st.success")
    @patch("components.download_reports.st.download_button")
    @patch("components.download_reports.st.selectbox")
    @patch("components.download_reports.st.columns")
    @patch("components.download_reports.Path")
    @patch("components.download_reports.st.subheader")
    @patch("components.download_reports.st.divider")
    @patch("components.download_reports.st.markdown")
    def test_show_download_center_download_returns_false(
        self,
        mock_markdown,
        mock_divider,
        mock_subheader,
        mock_path,
        mock_columns,
        mock_selectbox,
        mock_download_button,
        mock_success,
        mock_open_file,
    ):
        folder = MagicMock()
        folder.iterdir.return_value = [object()]

        pdf = MagicMock(spec=Path)
        pdf.name = "report.pdf"

        md = MagicMock(spec=Path)
        md.name = "report.md"

        html = MagicMock(spec=Path)
        html.name = "report.html"

        txt = MagicMock(spec=Path)
        txt.name = "report.txt"

        folder.glob.side_effect = [
            [pdf],
            [md],
            [html],
            [txt],
            [pdf],
            [md],
            [html],
            [txt],
        ]

        mock_path.return_value = folder

        metric_cols = [MagicMock() for _ in range(5)]
        download_cols = [MagicMock(), MagicMock()]

        for c in metric_cols + download_cols:
            c.__enter__.return_value = c
            c.__exit__.return_value = False

        mock_columns.side_effect = [
            tuple(metric_cols),
            tuple(download_cols),
        ]

        mock_selectbox.side_effect = [
            pdf,
            md,
            html,
            txt,
        ]

        mock_download_button.side_effect = [
            False,
            False,
            False,
            False,
        ]

        show_download_center()

        mock_success.assert_not_called()