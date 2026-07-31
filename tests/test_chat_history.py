from unittest.mock import MagicMock, mock_open, patch

from components.chat_history import ChatHistory


class TestChatHistory:

    @patch("components.chat_history.os.makedirs")
    def test_init(self, mock_makedirs):
        chat = ChatHistory()

        assert chat.chat_dir == "chat_history"

        mock_makedirs.assert_called_once_with(
            "chat_history",
            exist_ok=True,
        )

    @patch("components.chat_history.os.rename")
    @patch("components.chat_history.os.path.exists")
    @patch("components.chat_history.os.path.join")
    def test_rename_success(
        self,
        mock_join,
        mock_exists,
        mock_rename,
    ):
        chat = ChatHistory()

        mock_join.side_effect = [
            "chat_history/old.json",
            "chat_history/new.json",
        ]
        mock_exists.return_value = False

        result = chat.rename(
            "old.json",
            "new",
        )

        assert result is True

        mock_rename.assert_called_once_with(
            "chat_history/old.json",
            "chat_history/new.json",
        )

    @patch("components.chat_history.os.path.exists")
    @patch("components.chat_history.os.path.join")
    def test_rename_existing_file(
        self,
        mock_join,
        mock_exists,
    ):
        chat = ChatHistory()

        mock_join.side_effect = [
            "chat_history/old.json",
            "chat_history/new.json",
        ]
        mock_exists.return_value = True

        result = chat.rename(
            "old.json",
            "new",
        )

        assert result is False

    @patch("components.chat_history.os.listdir")
    def test_get_chat_files(
        self,
        mock_listdir,
    ):
        chat = ChatHistory()

        mock_listdir.return_value = [
            "b.json",
            "a.json",
            "notes.txt",
        ]

        files = chat.get_chat_files()

        assert files == [
            "b.json",
            "a.json",
        ]

    @patch.object(ChatHistory, "get_chat_files", return_value=[])
    @patch("components.chat_history.st.info")
    @patch("components.chat_history.st.subheader")
    def test_render_no_files(
        self,
        mock_subheader,
        mock_info,
        mock_get_files,
    ):
        chat = ChatHistory()

        chat.render()

        mock_subheader.assert_called_once_with(
            "📂 Chat History"
        )

        mock_info.assert_called_once_with(
            "No saved chats found."
        )

    @patch.object(ChatHistory, "get_chat_files")
    @patch("components.chat_history.st.text_input")
    @patch("components.chat_history.st.expander")
    @patch("components.chat_history.st.columns")
    @patch("components.chat_history.st.button")
    @patch("components.chat_history.st.write")
    @patch("components.chat_history.st.caption")
    @patch("components.chat_history.st.divider")
    @patch("components.chat_history.st.success")
    @patch("components.chat_history.st.rerun")
    @patch("builtins.open", new_callable=mock_open)
    @patch("components.chat_history.json.load")
    def test_render_load_chat(
        self,
        mock_json_load,
        mock_open_file,
        mock_rerun,
        mock_success,
        mock_divider,
        mock_caption,
        mock_write,
        mock_button,
        mock_columns,
        mock_expander,
        mock_text_input,
        mock_get_files,
    ):
        chat = ChatHistory()

        mock_get_files.return_value = [
            "chat1.json",
        ]

        mock_text_input.return_value = ""

        mock_json_load.return_value = [
            {"user": "Hello World"}
        ]

        mock_button.side_effect = [
            True,
            False,
            False,
        ]

        outer = MagicMock()
        outer.__enter__.return_value = outer
        outer.__exit__.return_value = False

        rename = MagicMock()
        rename.__enter__.return_value = rename
        rename.__exit__.return_value = False

        mock_expander.side_effect = [
            outer,
            rename,
        ]

        col1 = MagicMock()
        col2 = MagicMock()
        col3 = MagicMock()

        for c in (col1, col2, col3):
            c.__enter__.return_value = c
            c.__exit__.return_value = False

        mock_columns.return_value = (
            col1,
            col2,
            col3,
        )

        with patch(
            "components.chat_history.st.session_state",
            MagicMock(),
        ):
            chat.render()

        mock_success.assert_called_with(
            "Chat loaded."
        )

        mock_rerun.assert_called()

    @patch.object(ChatHistory, "get_chat_files")
    @patch("components.chat_history.os.remove")
    @patch("components.chat_history.st.text_input")
    @patch("components.chat_history.st.expander")
    @patch("components.chat_history.st.columns")
    @patch("components.chat_history.st.button")
    @patch("builtins.open", new_callable=mock_open)
    @patch("components.chat_history.json.load")
    @patch("components.chat_history.st.success")
    @patch("components.chat_history.st.rerun")
    @patch("components.chat_history.st.write")
    @patch("components.chat_history.st.caption")
    @patch("components.chat_history.st.divider")
    def test_render_delete_chat(
        self,
        mock_divider,
        mock_caption,
        mock_write,
        mock_rerun,
        mock_success,
        mock_json_load,
        mock_open_file,
        mock_button,
        mock_columns,
        mock_expander,
        mock_text_input,
        mock_remove,
        mock_get_files,
    ):
        chat = ChatHistory()

        mock_get_files.return_value = [
            "chat1.json",
        ]

        mock_text_input.return_value = ""

        mock_json_load.return_value = [
            {"user": "Hello"}
        ]

        mock_button.side_effect = [
            False,
            True,
            False,
        ]

        outer = MagicMock()
        rename = MagicMock()

        outer.__enter__.return_value = outer
        outer.__exit__.return_value = False

        rename.__enter__.return_value = rename
        rename.__exit__.return_value = False

        mock_expander.side_effect = [
            outer,
            rename,
        ]

        cols = [MagicMock() for _ in range(3)]

        for c in cols:
            c.__enter__.return_value = c
            c.__exit__.return_value = False

        mock_columns.return_value = tuple(cols)

        chat.render()

        mock_remove.assert_called_once()

        mock_success.assert_called_with(
            "Chat deleted."
        )

        mock_rerun.assert_called()

    @patch.object(ChatHistory, "rename")
    @patch.object(ChatHistory, "get_chat_files")
    @patch("components.chat_history.st.text_input")
    @patch("components.chat_history.st.expander")
    @patch("components.chat_history.st.columns")
    @patch("components.chat_history.st.button")
    @patch("builtins.open", new_callable=mock_open)
    @patch("components.chat_history.json.load")
    @patch("components.chat_history.st.success")
    @patch("components.chat_history.st.rerun")
    @patch("components.chat_history.st.write")
    @patch("components.chat_history.st.caption")
    @patch("components.chat_history.st.divider")
    def test_render_rename_success(
        self,
        mock_divider,
        mock_caption,
        mock_write,
        mock_rerun,
        mock_success,
        mock_json_load,
        mock_open_file,
        mock_button,
        mock_columns,
        mock_expander,
        mock_text_input,
        mock_get_files,
        mock_rename,
    ):
        chat = ChatHistory()

        mock_get_files.return_value = [
            "chat1.json",
        ]

        mock_text_input.side_effect = [
            "",
            "new_chat",
        ]

        mock_json_load.return_value = [
            {"user": "Hello"}
        ]

        mock_button.side_effect = [
            False,
            False,
            True,
        ]

        mock_rename.return_value = True

        outer = MagicMock()
        rename = MagicMock()

        outer.__enter__.return_value = outer
        outer.__exit__.return_value = False

        rename.__enter__.return_value = rename
        rename.__exit__.return_value = False

        mock_expander.side_effect = [
            outer,
            rename,
        ]

        cols = [MagicMock() for _ in range(3)]

        for c in cols:
            c.__enter__.return_value = c
            c.__exit__.return_value = False

        mock_columns.return_value = tuple(cols)

        chat.render()

        mock_rename.assert_called_once_with(
            "chat1.json",
            "new_chat",
        )

        mock_success.assert_called_with(
            "✅ Chat renamed successfully."
        )

    @patch.object(ChatHistory, "rename", return_value=False)
    @patch.object(ChatHistory, "get_chat_files")
    @patch("components.chat_history.st.error")
    @patch("components.chat_history.st.text_input")
    @patch("components.chat_history.st.expander")
    @patch("components.chat_history.st.columns")
    @patch("components.chat_history.st.button")
    @patch("builtins.open", new_callable=mock_open)
    @patch("components.chat_history.json.load")
    @patch("components.chat_history.st.write")
    @patch("components.chat_history.st.caption")
    @patch("components.chat_history.st.divider")
    def test_render_rename_failure(
        self,
        mock_divider,
        mock_caption,
        mock_write,
        mock_json_load,
        mock_open_file,
        mock_button,
        mock_columns,
        mock_expander,
        mock_text_input,
        mock_error,
        mock_get_files,
        mock_rename,
    ):
        chat = ChatHistory()

        mock_get_files.return_value = [
            "chat1.json",
        ]

        mock_text_input.side_effect = [
            "",
            "existing",
        ]

        mock_json_load.return_value = [
            {"user": "Hello"}
        ]

        mock_button.side_effect = [
            False,
            False,
            True,
        ]

        outer = MagicMock()
        rename = MagicMock()

        outer.__enter__.return_value = outer
        outer.__exit__.return_value = False

        rename.__enter__.return_value = rename
        rename.__exit__.return_value = False

        mock_expander.side_effect = [
            outer,
            rename,
        ]

        cols = [MagicMock() for _ in range(3)]

        for c in cols:
            c.__enter__.return_value = c
            c.__exit__.return_value = False

        mock_columns.return_value = tuple(cols)

        chat.render()

        mock_error.assert_called_once_with(
            "❌ Chat name already exists."
        )