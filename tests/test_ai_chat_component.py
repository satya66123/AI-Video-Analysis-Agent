from unittest.mock import MagicMock, mock_open, patch

from components.ai_chat import get_transcripts, TRANSCRIPT_DIR


class FakeSessionState(dict):
    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        self[name] = value


class TestAIChatComponent:

    @patch("components.ai_chat.st")
    @patch("components.ai_chat.get_transcripts")
    def test_no_transcripts(
        self,
        mock_transcripts,
        mock_st,
    ):
        from components.ai_chat import show_ai_chat_component

        mock_transcripts.return_value = []

        show_ai_chat_component()

        mock_st.warning.assert_called_once_with(
            "No transcripts found. Please generate a transcript first."
        )

    @patch("builtins.open", new_callable=mock_open, read_data="hello")
    @patch("components.ai_chat.os.path.join")
    @patch("components.ai_chat.get_transcripts")
    @patch("components.ai_chat.st")
    def test_provider_not_selected(
        self,
        mock_st,
        mock_get,
        mock_join,
        mock_file,
    ):
        from components.ai_chat import show_ai_chat_component

        mock_get.return_value = ["demo.txt"]
        mock_join.return_value = "demo.txt"

        session = FakeSessionState()
        session["provider"] = None
        session["model"] = None

        mock_st.session_state = session

        mock_st.selectbox.return_value = "demo.txt"

        mock_col = MagicMock()
        mock_st.columns.return_value = [mock_col, mock_col]

        show_ai_chat_component()

        mock_st.error.assert_called_once_with(
            "Please select an AI provider and model."
        )

    @patch("components.ai_chat.os.path.exists")
    def test_directory_not_exists(self, mock_exists):
        mock_exists.return_value = False

        assert get_transcripts() == []

    @patch("components.ai_chat.os.listdir")
    @patch("components.ai_chat.os.path.exists")
    def test_returns_only_txt_files(
        self,
        mock_exists,
        mock_listdir,
    ):
        mock_exists.return_value = True

        mock_listdir.return_value = [
            "a.txt",
            "b.txt",
            "c.pdf",
            "d.mp4",
        ]

        files = get_transcripts()

        assert files == ["b.txt", "a.txt"]

    @patch("components.ai_chat.os.listdir")
    @patch("components.ai_chat.os.path.exists")
    def test_empty_directory(
        self,
        mock_exists,
        mock_listdir,
    ):
        mock_exists.return_value = True
        mock_listdir.return_value = []

        assert get_transcripts() == []

    def test_transcript_directory_constant(self):
        assert TRANSCRIPT_DIR == "transcripts"


class TestAIChatComponent:

    @patch("components.ai_chat.st")
    @patch("components.ai_chat.get_transcripts")
    def test_no_transcripts(
        self,
        mock_transcripts,
        mock_st,
    ):
        from components.ai_chat import (
            show_ai_chat_component,
        )

        mock_transcripts.return_value = []

        show_ai_chat_component()

        mock_st.warning.assert_called_once()


    @patch("builtins.open", new_callable=mock_open, read_data="hello")
    @patch("components.ai_chat.os.path.join")
    @patch("components.ai_chat.get_transcripts")
    @patch("components.ai_chat.st")
    def test_provider_not_selected(
            self,
            mock_st,
            mock_get,
            mock_join,
            mock_file,
    ):
        from components.ai_chat import show_ai_chat_component

        mock_get.return_value = ["demo.txt"]
        mock_join.return_value = "demo.txt"

        session = FakeSessionState()
        session["provider"] = None
        session["model"] = None

        mock_st.session_state = session

        mock_st.selectbox.return_value = "demo.txt"

        mock_col = MagicMock()
        mock_st.columns.return_value = [mock_col, mock_col]

        show_ai_chat_component()

        mock_st.error.assert_called_once_with(
            "Please select an AI provider and model."
        )

    @patch("components.ai_chat.chat_service")
    def test_chat_service_exists(
        self,
        mock_service,
    ):
        assert mock_service is not None

    @patch("components.ai_chat.chat_export")
    def test_chat_export_exists(
        self,
        mock_export,
    ):
        assert mock_export is not None

    @patch("components.ai_chat.title_generator")
    def test_title_generator_exists(
        self,
        mock_title,
    ):
        assert mock_title is not None

    @patch("components.ai_chat.pdf_export")
    def test_pdf_export_exists(
        self,
        mock_pdf,
    ):
        assert mock_pdf is not None

    @patch("components.ai_chat.txt_export")
    def test_txt_export_exists(
        self,
        mock_txt,
    ):
        assert mock_txt is not None