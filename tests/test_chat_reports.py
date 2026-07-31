from unittest.mock import MagicMock, patch

from components.chat_reports import show_chat_reports


class TestChatReports:

    @patch("components.chat_reports.st.subheader")
    @patch("components.chat_reports.show_file_browser")
    def test_show_chat_reports_no_file(
        self,
        mock_show_file_browser,
        mock_subheader,
    ):
        mock_show_file_browser.return_value = None

        show_chat_reports()

        mock_subheader.assert_called_once_with(
            "💬 Chat Reports"
        )

        mock_show_file_browser.assert_called_once_with(
            folder="chat_history",
            extension=".json",
            key="chat_browser",
        )

    @patch("components.chat_reports.st.download_button")
    @patch("components.chat_reports.st.json")
    @patch("components.chat_reports.st.subheader")
    @patch("components.chat_reports.show_file_browser")
    def test_show_chat_reports_with_file(
        self,
        mock_show_file_browser,
        mock_subheader,
        mock_json,
        mock_download_button,
    ):
        mock_file = MagicMock()
        mock_file.name = "chat.json"
        mock_file.read_text.return_value = (
            '{"messages":[{"user":"Hello"}]}'
        )

        mock_show_file_browser.return_value = mock_file

        show_chat_reports()

        mock_subheader.assert_called_once_with(
            "💬 Chat Reports"
        )

        mock_show_file_browser.assert_called_once_with(
            folder="chat_history",
            extension=".json",
            key="chat_browser",
        )

        assert mock_file.read_text.call_count == 2
        mock_file.read_text.assert_called_with(
            encoding="utf-8"
        )

        mock_json.assert_called_once_with(
            '{"messages":[{"user":"Hello"}]}'
        )

        mock_download_button.assert_called_once_with(
            "⬇ Download Chat",
            '{"messages":[{"user":"Hello"}]}',
            file_name="chat.json",
            mime="application/json",
            use_container_width=True,
        )