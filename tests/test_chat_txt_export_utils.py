import os
from unittest.mock import mock_open, patch

from utils.chat_txt_export import ChatTXTExport


class TestChatTXTExportUtils:

    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.chat_txt_export.os.makedirs")
    def test_export_success(
        self,
        mock_makedirs,
        mock_file,
    ):
        history = [
            {
                "user": "Hello",
                "assistant": "Hi",
            },
            {
                "user": "How are you?",
                "assistant": "I'm fine.",
            },
        ]

        result = ChatTXTExport.export(
            history,
            "chat_history",
        )

        expected_path = os.path.join(
            "exports",
            "chat_history.txt",
        )

        assert result == expected_path

        mock_makedirs.assert_called_once_with(
            "exports",
            exist_ok=True,
        )

        mock_file.assert_called_once_with(
            expected_path,
            "w",
            encoding="utf-8",
        )

        handle = mock_file()

        expected_calls = [
            "User\n",
            "Hello",
            "\n\n",
            "Assistant\n",
            "Hi",
            "\n\n",
            "----------------------------------\n",
            "User\n",
            "How are you?",
            "\n\n",
            "Assistant\n",
            "I'm fine.",
            "\n\n",
            "----------------------------------\n",
        ]

        actual_calls = [
            call.args[0]
            for call in handle.write.call_args_list
        ]

        assert actual_calls == expected_calls

    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.chat_txt_export.os.makedirs")
    def test_export_empty_history(
        self,
        mock_makedirs,
        mock_file,
    ):
        result = ChatTXTExport.export(
            [],
            "empty_chat",
        )

        expected_path = os.path.join(
            "exports",
            "empty_chat.txt",
        )

        assert result == expected_path

        mock_file.assert_called_once_with(
            expected_path,
            "w",
            encoding="utf-8",
        )

        handle = mock_file()

        handle.write.assert_not_called()