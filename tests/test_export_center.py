# tests/test_export_center.py

from unittest.mock import MagicMock, mock_open, patch

from components.export_center import show_export_center


class TestExportCenter:

    @patch("components.export_center.st.info")
    @patch("components.export_center.Path")
    @patch("components.export_center.st.subheader")
    def test_show_export_center_no_files(
        self,
        mock_subheader,
        mock_path,
        mock_info,
    ):
        folder = MagicMock()
        folder.glob.return_value = []
        mock_path.return_value = folder

        show_export_center()

        mock_subheader.assert_called_once_with(
            "📦 Export Center"
        )

        folder.mkdir.assert_called_once_with(
            exist_ok=True
        )

        mock_info.assert_called_once_with(
            "No exported reports found."
        )

    @patch("builtins.open", new_callable=mock_open, read_data="sample")
    @patch("components.export_center.st.download_button")
    @patch("components.export_center.st.text_area")
    @patch("components.export_center.st.button")
    @patch("components.export_center.st.write")
    @patch("components.export_center.st.selectbox")
    @patch("components.export_center.st.text_input")
    @patch("components.export_center.st.divider")
    @patch("components.export_center.st.caption")
    @patch("components.export_center.st.columns")
    @patch("components.export_center.Path")
    @patch("components.export_center.st.subheader")
    def test_show_export_center_text_file(
        self,
        mock_subheader,
        mock_path,
        mock_columns,
        mock_caption,
        mock_divider,
        mock_text_input,
        mock_selectbox,
        mock_write,
        mock_button,
        mock_text_area,
        mock_download_button,
        mock_open_file,
    ):
        folder = MagicMock()

        file = MagicMock()
        file.name = "report.md"
        file.suffix = ".md"

        stat = MagicMock()
        stat.st_size = 2048
        stat.st_mtime = 1000

        file.stat.return_value = stat
        file.read_text.return_value = "# Report"

        folder.glob.side_effect = [
            [file],
            [MagicMock()],
            [],
            [MagicMock()],
            [],
        ]

        mock_path.return_value = folder

        cols = [MagicMock() for _ in range(5)]
        mock_columns.return_value = tuple(cols)

        mock_text_input.return_value = ""
        mock_selectbox.return_value = file
        mock_button.return_value = False

        show_export_center()

        cols[0].metric.assert_called_once_with(
            "Files",
            1,
        )

        cols[1].metric.assert_called_once_with(
            "PDF",
            1,
        )

        cols[2].metric.assert_called_once_with(
            "HTML",
            0,
        )

        cols[3].metric.assert_called_once_with(
            "Markdown",
            1,
        )

        cols[4].metric.assert_called_once_with(
            "TXT",
            0,
        )

        mock_caption.assert_called_once()

        mock_text_area.assert_called_once_with(
            "Preview",
            "# Report",
            height=400,
        )

        mock_download_button.assert_called_once()

    @patch("components.export_center.st.warning")
    @patch("components.export_center.st.text_input")
    @patch("components.export_center.st.caption")
    @patch("components.export_center.st.columns")
    @patch("components.export_center.Path")
    @patch("components.export_center.st.subheader")
    def test_show_export_center_search_no_match(
        self,
        mock_subheader,
        mock_path,
        mock_columns,
        mock_caption,
        mock_text_input,
        mock_warning,
    ):
        folder = MagicMock()

        file = MagicMock()
        file.name = "report.md"

        stat = MagicMock()
        stat.st_size = 100
        stat.st_mtime = 100

        file.stat.return_value = stat

        folder.glob.side_effect = [
            [file],
            [],
            [],
            [file],
            [],
        ]

        mock_path.return_value = folder

        cols = [MagicMock() for _ in range(5)]
        mock_columns.return_value = tuple(cols)

        mock_text_input.return_value = "python"

        show_export_center()

        mock_warning.assert_called_once_with(
            "No matching reports."
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("components.export_center.st.download_button")
    @patch("components.export_center.st.info")
    @patch("components.export_center.st.button")
    @patch("components.export_center.st.write")
    @patch("components.export_center.st.selectbox")
    @patch("components.export_center.st.text_input")
    @patch("components.export_center.st.caption")
    @patch("components.export_center.st.columns")
    @patch("components.export_center.Path")
    @patch("components.export_center.st.subheader")
    def test_show_export_center_pdf_preview(
        self,
        mock_subheader,
        mock_path,
        mock_columns,
        mock_caption,
        mock_text_input,
        mock_selectbox,
        mock_write,
        mock_button,
        mock_info,
        mock_download_button,
        mock_open_file,
    ):
        folder = MagicMock()

        file = MagicMock()
        file.name = "report.pdf"
        file.suffix = ".pdf"

        stat = MagicMock()
        stat.st_size = 1024
        stat.st_mtime = 1000

        file.stat.return_value = stat

        folder.glob.side_effect = [
            [file],
            [file],
            [],
            [],
            [],
        ]

        mock_path.return_value = folder

        cols = [MagicMock() for _ in range(5)]
        mock_columns.return_value = tuple(cols)

        mock_text_input.return_value = ""
        mock_selectbox.return_value = file
        mock_button.return_value = False

        show_export_center()

        mock_info.assert_called_with(
            "PDF preview is not available."
        )

        mock_download_button.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("components.export_center.st.success")
    @patch("components.export_center.st.rerun")
    @patch("components.export_center.st.download_button")
    @patch("components.export_center.st.text_area")
    @patch("components.export_center.st.button")
    @patch("components.export_center.st.write")
    @patch("components.export_center.st.selectbox")
    @patch("components.export_center.st.text_input")
    @patch("components.export_center.st.caption")
    @patch("components.export_center.st.columns")
    @patch("components.export_center.Path")
    @patch("components.export_center.st.subheader")
    def test_show_export_center_delete_export(
        self,
        mock_subheader,
        mock_path,
        mock_columns,
        mock_caption,
        mock_text_input,
        mock_selectbox,
        mock_write,
        mock_button,
        mock_text_area,
        mock_download_button,
        mock_rerun,
        mock_success,
        mock_open_file,
    ):
        folder = MagicMock()

        file = MagicMock()
        file.name = "report.txt"
        file.suffix = ".txt"

        stat = MagicMock()
        stat.st_size = 1024
        stat.st_mtime = 1000

        file.stat.return_value = stat
        file.read_text.return_value = "content"

        folder.glob.side_effect = [
            [file],
            [],
            [],
            [],
            [file],
        ]

        mock_path.return_value = folder

        cols = [MagicMock() for _ in range(5)]
        mock_columns.return_value = tuple(cols)

        mock_text_input.return_value = ""
        mock_selectbox.return_value = file
        mock_button.return_value = True

        show_export_center()

        file.unlink.assert_called_once()

        mock_success.assert_called_once_with(
            "Export deleted successfully."
        )

        mock_rerun.assert_called_once()