# tests/test_file_browser.py

from pathlib import Path
from unittest.mock import MagicMock, patch

from components.file_browser import show_file_browser


class TestFileBrowser:

    @patch("components.file_browser.st.info")
    @patch("components.file_browser.Path")
    def test_folder_not_exists(
        self,
        mock_path,
        mock_info,
    ):
        directory = MagicMock()
        directory.exists.return_value = False
        mock_path.return_value = directory

        result = show_file_browser("uploads")

        assert result is None

        mock_info.assert_called_once_with(
            "uploads folder not found."
        )

    @patch("components.file_browser.st.info")
    @patch("components.file_browser.Path")
    def test_no_files_with_extension(
        self,
        mock_path,
        mock_info,
    ):
        directory = MagicMock()
        directory.exists.return_value = True
        directory.glob.return_value = []

        mock_path.return_value = directory

        result = show_file_browser(
            "uploads",
            extension=".mp4",
        )

        assert result is None

        directory.glob.assert_called_once_with(
            "*.mp4"
        )

        mock_info.assert_called_once_with(
            "No files available."
        )

    @patch("components.file_browser.st.info")
    @patch("components.file_browser.Path")
    def test_no_files_without_extension(
        self,
        mock_path,
        mock_info,
    ):
        directory = MagicMock()
        directory.exists.return_value = True
        directory.iterdir.return_value = []

        mock_path.return_value = directory

        result = show_file_browser("uploads")

        assert result is None

        directory.iterdir.assert_called_once()

        mock_info.assert_called_once_with(
            "No files available."
        )

    @patch("components.file_browser.st.selectbox")
    @patch("components.file_browser.Path")
    def test_show_files_with_extension(
        self,
        mock_path,
        mock_selectbox,
    ):
        directory = MagicMock()
        directory.exists.return_value = True

        from pathlib import Path

        file1 = Path("a.mp4")
        file2 = Path("b.mp4")

        directory.glob.return_value = [
            file2,
            file1,
        ]

        mock_path.return_value = directory

        mock_selectbox.return_value = file1

        result = show_file_browser(
            folder="uploads",
            extension=".mp4",
            key="video_browser",
        )

        assert result == file1

        mock_selectbox.assert_called_once()

        args = mock_selectbox.call_args

        assert args.args[0] == "Select File"
        assert args.args[1] == sorted(
            [file2, file1]
        )

        assert args.kwargs["key"] == "video_browser"

    @patch("components.file_browser.st.selectbox")
    @patch("components.file_browser.Path")
    def test_show_files_without_extension(
        self,
        mock_path,
        mock_selectbox,
    ):
        directory = MagicMock()
        directory.exists.return_value = True

        file1 = Path("a.txt")
        file2 = Path("b.pdf")

        directory.iterdir.return_value = [
            file2,
            file1,
        ]

        mock_path.return_value = directory

        mock_selectbox.return_value = file2

        result = show_file_browser(
            folder="exports",
            key="export_browser",
        )

        assert result == file2

        directory.iterdir.assert_called_once()

        mock_selectbox.assert_called_once()

        args = mock_selectbox.call_args

        assert args.args[0] == "Select File"
        assert args.kwargs["key"] == "export_browser"