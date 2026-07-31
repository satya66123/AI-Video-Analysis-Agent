import json
import os
from unittest.mock import mock_open, patch

from utils.chat_history import ChatHistory


class TestChatHistoryUtils:

    @patch("utils.chat_history.os.makedirs")
    def test_init(
        self,
        mock_makedirs,
    ):
        history = ChatHistory()

        assert history.folder == "chat_history"

        mock_makedirs.assert_called_once_with(
            "chat_history",
            exist_ok=True,
        )

    @patch("utils.chat_history.os.listdir")
    @patch("utils.chat_history.os.makedirs")
    def test_list_sessions(
        self,
        mock_makedirs,
        mock_listdir,
    ):
        mock_listdir.return_value = [
            "session1.json",
            "session3.json",
            "session2.json",
        ]

        history = ChatHistory()

        result = history.list_sessions()

        assert result == [
            "session3.json",
            "session2.json",
            "session1.json",
        ]

        mock_listdir.assert_called_once_with(
            "chat_history"
        )

    @patch("utils.chat_history.json.load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.chat_history.os.makedirs")
    def test_load(
        self,
        mock_makedirs,
        mock_file,
        mock_json_load,
    ):
        expected = [
            {
                "user": "Hello",
                "assistant": "Hi",
            }
        ]

        mock_json_load.return_value = expected

        history = ChatHistory()

        result = history.load(
            "chat.json"
        )

        assert result == expected

        mock_file.assert_called_once_with(
            os.path.join(
                "chat_history",
                "chat.json",
            ),
            encoding="utf-8",
        )

        mock_json_load.assert_called_once()

    @patch("utils.chat_history.json.dump")
    @patch("builtins.open", new_callable=mock_open)
    @patch("utils.chat_history.os.makedirs")
    def test_save(
        self,
        mock_makedirs,
        mock_file,
        mock_json_dump,
    ):
        data = [
            {
                "user": "Hello",
                "assistant": "Hi",
            }
        ]

        history = ChatHistory()

        history.save(
            "chat.json",
            data,
        )

        mock_file.assert_called_once_with(
            os.path.join(
                "chat_history",
                "chat.json",
            ),
            "w",
            encoding="utf-8",
        )

        mock_json_dump.assert_called_once_with(
            data,
            mock_file(),
            indent=4,
        )

    @patch("utils.chat_history.os.remove")
    @patch("utils.chat_history.os.path.exists")
    @patch("utils.chat_history.os.makedirs")
    def test_delete_success(
        self,
        mock_makedirs,
        mock_exists,
        mock_remove,
    ):
        mock_exists.return_value = True

        history = ChatHistory()

        history.delete(
            "chat.json"
        )

        mock_remove.assert_called_once_with(
            os.path.join(
                "chat_history",
                "chat.json",
            )
        )

    @patch("utils.chat_history.os.remove")
    @patch("utils.chat_history.os.path.exists")
    @patch("utils.chat_history.os.makedirs")
    def test_delete_file_not_found(
        self,
        mock_makedirs,
        mock_exists,
        mock_remove,
    ):
        mock_exists.return_value = False

        history = ChatHistory()

        history.delete(
            "chat.json"
        )

        mock_remove.assert_not_called()