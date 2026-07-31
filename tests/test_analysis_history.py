import os
import time
from unittest.mock import MagicMock, mock_open, patch

from components.analysis_history import AnalysisHistory


class TestAnalysisHistory:

    @patch("components.analysis_history.os.makedirs")
    @patch("components.analysis_history.os.listdir")
    @patch("components.analysis_history.os.path.getmtime")
    def test_get_files_returns_sorted_markdown_files(
        self,
        mock_getmtime,
        mock_listdir,
        mock_makedirs,
    ):
        mock_listdir.return_value = [
            "old.md",
            "notes.txt",
            "new.md",
        ]

        def fake_getmtime(path):
            if path.endswith("new.md"):
                return 200
            return 100

        mock_getmtime.side_effect = fake_getmtime

        files = AnalysisHistory.get_files()

        mock_makedirs.assert_called_once_with(
            AnalysisHistory.ANALYSIS_FOLDER,
            exist_ok=True,
        )

        assert files == [
            "new.md",
            "old.md",
        ]

    @patch.object(AnalysisHistory, "get_files", return_value=[])
    @patch("components.analysis_history.st.info")
    @patch("components.analysis_history.st.subheader")
    def test_render_no_files(
        self,
        mock_subheader,
        mock_info,
        mock_get_files,
    ):
        AnalysisHistory.render()

        mock_subheader.assert_called_once_with(
            "📁 Analysis History"
        )
        mock_info.assert_called_once_with(
            "No analyses found."
        )

    @patch.object(AnalysisHistory, "get_files")
    @patch("components.analysis_history.st.text_input")
    @patch("components.analysis_history.st.expander")
    @patch("components.analysis_history.time.strftime")
    @patch("components.analysis_history.time.localtime")
    @patch("components.analysis_history.os.path.getmtime")
    @patch("builtins.open", new_callable=mock_open, read_data="# Report")
    @patch("components.analysis_history.st.download_button")
    @patch("components.analysis_history.st.button")
    @patch("components.analysis_history.st.columns")
    @patch("components.analysis_history.st.caption")
    @patch("components.analysis_history.st.markdown")
    @patch("components.analysis_history.st.subheader")
    def test_render_displays_analysis(
        self,
        mock_subheader,
        mock_markdown,
        mock_caption,
        mock_columns,
        mock_button,
        mock_download,
        mock_open_file,
        mock_getmtime,
        mock_localtime,
        mock_strftime,
        mock_expander,
        mock_text_input,
        mock_get_files,
    ):
        mock_get_files.return_value = ["analysis.md"]
        mock_text_input.return_value = ""
        mock_button.return_value = False
        mock_getmtime.return_value = 123456
        mock_localtime.return_value = time.localtime(123456)
        mock_strftime.return_value = "2026-07-30 09:00"

        col1 = MagicMock()
        col2 = MagicMock()
        mock_columns.return_value = (col1, col2)

        expander = MagicMock()
        expander.__enter__.return_value = expander
        expander.__exit__.return_value = False
        mock_expander.return_value = expander

        col1.__enter__.return_value = col1
        col1.__exit__.return_value = False
        col2.__enter__.return_value = col2
        col2.__exit__.return_value = False

        AnalysisHistory.render()

        mock_markdown.assert_called_once_with("# Report")
        mock_download.assert_called_once()

    @patch.object(AnalysisHistory, "get_files")
    @patch("components.analysis_history.st.text_input")
    @patch("components.analysis_history.st.expander")
    @patch("components.analysis_history.time.strftime")
    @patch("components.analysis_history.time.localtime")
    @patch("components.analysis_history.os.path.getmtime")
    @patch("builtins.open", new_callable=mock_open, read_data="# Report")
    @patch("components.analysis_history.st.download_button")
    @patch("components.analysis_history.st.button")
    @patch("components.analysis_history.st.columns")
    @patch("components.analysis_history.st.caption")
    @patch("components.analysis_history.st.markdown")
    @patch("components.analysis_history.os.remove")
    @patch("components.analysis_history.st.success")
    @patch("components.analysis_history.st.rerun")
    def test_render_delete_analysis(
        self,
        mock_rerun,
        mock_success,
        mock_remove,
        mock_markdown,
        mock_caption,
        mock_columns,
        mock_button,
        mock_download,
        mock_open_file,
        mock_getmtime,
        mock_localtime,
        mock_strftime,
        mock_expander,
        mock_text_input,
        mock_get_files,
    ):
        mock_get_files.return_value = ["analysis.md"]
        mock_text_input.return_value = ""
        mock_button.return_value = True
        mock_getmtime.return_value = 123456
        mock_localtime.return_value = time.localtime(123456)
        mock_strftime.return_value = "2026-07-30 09:00"

        col1 = MagicMock()
        col2 = MagicMock()
        mock_columns.return_value = (col1, col2)

        expander = MagicMock()
        expander.__enter__.return_value = expander
        expander.__exit__.return_value = False
        mock_expander.return_value = expander

        col1.__enter__.return_value = col1
        col1.__exit__.return_value = False
        col2.__enter__.return_value = col2
        col2.__exit__.return_value = False

        AnalysisHistory.render()

        expected_path = os.path.join(
            AnalysisHistory.ANALYSIS_FOLDER,
            "analysis.md",
        )

        mock_remove.assert_called_once_with(expected_path)
        mock_success.assert_called_once_with(
            "Analysis Deleted"
        )
        mock_rerun.assert_called_once()

    @patch.object(AnalysisHistory, "get_files")
    @patch("components.analysis_history.st.text_input")
    @patch("components.analysis_history.st.expander")
    def test_render_search_filters_files(
        self,
        mock_expander,
        mock_text_input,
        mock_get_files,
    ):
        mock_get_files.return_value = [
            "python.md",
            "java.md",
        ]
        mock_text_input.return_value = "python"

        expander = MagicMock()
        expander.__enter__.return_value = expander
        expander.__exit__.return_value = False
        mock_expander.return_value = expander

        with patch(
            "components.analysis_history.os.path.getmtime",
            return_value=1,
        ), patch(
            "components.analysis_history.time.localtime",
            return_value=time.localtime(1),
        ), patch(
            "components.analysis_history.time.strftime",
            return_value="date",
        ), patch(
            "builtins.open",
            mock_open(read_data="content"),
        ), patch(
            "components.analysis_history.st.caption",
        ), patch(
            "components.analysis_history.st.markdown",
        ), patch(
            "components.analysis_history.st.download_button",
        ), patch(
            "components.analysis_history.st.button",
            return_value=False,
        ), patch(
            "components.analysis_history.st.columns",
            return_value=(MagicMock(), MagicMock()),
        ):
            col1, col2 = (
                MagicMock(),
                MagicMock(),
            )
            col1.__enter__.return_value = col1
            col1.__exit__.return_value = False
            col2.__enter__.return_value = col2
            col2.__exit__.return_value = False

            with patch(
                "components.analysis_history.st.columns",
                return_value=(col1, col2),
            ):
                AnalysisHistory.render()

        mock_expander.assert_called_once_with("python.md")