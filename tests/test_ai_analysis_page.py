from unittest.mock import MagicMock, mock_open, patch


from pages.ai_analysis import (
    TRANSCRIPT_FOLDER,
    get_transcripts,
    show_ai_analysis,
)


class TestGetTranscripts:

    @patch("pages.ai_analysis.os.path.exists")
    def test_folder_not_exists(self, mock_exists):
        mock_exists.return_value = False

        assert get_transcripts() == []

    @patch("pages.ai_analysis.os.listdir")
    @patch("pages.ai_analysis.os.path.exists")
    def test_get_transcripts(self, mock_exists, mock_listdir):
        mock_exists.return_value = True

        mock_listdir.return_value = [
            "b.txt",
            "a.txt",
            "video.mp4",
            "notes.pdf",
            "c.txt",
        ]

        result = get_transcripts()

        assert result == [
            "c.txt",
            "b.txt",
            "a.txt",
        ]

        mock_listdir.assert_called_once_with(
            TRANSCRIPT_FOLDER
        )


class TestShowAIAnalysisValidation:

    @patch("pages.ai_analysis.st.warning")
    @patch("pages.ai_analysis.st.title")
    @patch("pages.ai_analysis.get_transcripts")
    def test_no_transcripts(
        self,
        mock_get,
        mock_title,
        mock_warning,
    ):
        mock_get.return_value = []

        show_ai_analysis()

        mock_title.assert_called_once_with(
            "🧠 AI Video Analysis"
        )

        mock_warning.assert_called_once_with(
            "No transcripts found."
        )

    @patch("pages.ai_analysis.st.error")
    @patch("pages.ai_analysis.st.title")
    @patch("pages.ai_analysis.get_transcripts")
    @patch("pages.ai_analysis.st.session_state", {})
    def test_provider_model_missing(
        self,
        mock_get,
        mock_title,
        mock_error,
    ):
        mock_get.return_value = [
            "sample.txt"
        ]

        show_ai_analysis()

        mock_error.assert_called_once_with(
            "Please select a Provider and Model from the sidebar."
        )

    @patch("pages.ai_analysis.st.error")
    @patch("pages.ai_analysis.st.title")
    @patch("pages.ai_analysis.get_transcripts")
    @patch(
        "pages.ai_analysis.st.session_state",
        {"provider": "ollama"},
    )
    def test_model_missing(
        self,
        mock_get,
        mock_title,
        mock_error,
    ):
        mock_get.return_value = [
            "sample.txt"
        ]

        show_ai_analysis()

        mock_error.assert_called_once_with(
            "Please select a Provider and Model from the sidebar."
        )

    @patch("pages.ai_analysis.st.error")
    @patch("pages.ai_analysis.st.title")
    @patch("pages.ai_analysis.get_transcripts")
    @patch(
        "pages.ai_analysis.st.session_state",
        {"model": "llama3.1"},
    )
    def test_provider_missing(
        self,
        mock_get,
        mock_title,
        mock_error,
    ):
        mock_get.return_value = [
            "sample.txt"
        ]

        show_ai_analysis()

        mock_error.assert_called_once_with(
            "Please select a Provider and Model from the sidebar."
        )

class TestGetTranscripts:

    @patch("pages.ai_analysis.os.path.exists")
    def test_folder_not_exists(self, mock_exists):
        mock_exists.return_value = False

        assert get_transcripts() == []

    @patch("pages.ai_analysis.os.listdir")
    @patch("pages.ai_analysis.os.path.exists")
    def test_get_transcripts(self, mock_exists, mock_listdir):
        mock_exists.return_value = True

        mock_listdir.return_value = [
            "b.txt",
            "a.txt",
            "video.mp4",
            "notes.pdf",
            "c.txt",
        ]

        result = get_transcripts()

        assert result == [
            "c.txt",
            "b.txt",
            "a.txt",
        ]

        mock_listdir.assert_called_once_with(
            TRANSCRIPT_FOLDER
        )


class TestShowAIAnalysisValidation:

    @patch("pages.ai_analysis.st.warning")
    @patch("pages.ai_analysis.st.title")
    @patch("pages.ai_analysis.get_transcripts")
    def test_no_transcripts(
        self,
        mock_get,
        mock_title,
        mock_warning,
    ):
        mock_get.return_value = []

        show_ai_analysis()

        mock_title.assert_called_once_with(
            "🧠 AI Video Analysis"
        )

        mock_warning.assert_called_once_with(
            "No transcripts found."
        )

    @patch("pages.ai_analysis.st.error")
    @patch("pages.ai_analysis.st.title")
    @patch("pages.ai_analysis.get_transcripts")
    @patch("pages.ai_analysis.st.session_state", {})
    def test_provider_model_missing(
        self,
        mock_get,
        mock_title,
        mock_error,
    ):
        mock_get.return_value = [
            "sample.txt"
        ]

        show_ai_analysis()

        mock_error.assert_called_once_with(
            "Please select a Provider and Model from the sidebar."
        )

    @patch("pages.ai_analysis.st.error")
    @patch("pages.ai_analysis.st.title")
    @patch("pages.ai_analysis.get_transcripts")
    @patch(
        "pages.ai_analysis.st.session_state",
        {"provider": "ollama"},
    )
    def test_model_missing(
        self,
        mock_get,
        mock_title,
        mock_error,
    ):
        mock_get.return_value = [
            "sample.txt"
        ]

        show_ai_analysis()

        mock_error.assert_called_once_with(
            "Please select a Provider and Model from the sidebar."
        )

    @patch("pages.ai_analysis.st.error")
    @patch("pages.ai_analysis.st.title")
    @patch("pages.ai_analysis.get_transcripts")
    @patch(
        "pages.ai_analysis.st.session_state",
        {"model": "llama3.1"},
    )
    def test_provider_missing(
        self,
        mock_get,
        mock_title,
        mock_error,
    ):
        mock_get.return_value = [
            "sample.txt"
        ]

        show_ai_analysis()

        mock_error.assert_called_once_with(
            "Please select a Provider and Model from the sidebar."
        )


@patch("pages.ai_analysis.AnalysisHistory.render")
@patch("pages.ai_analysis.st.divider")
@patch("pages.ai_analysis.st.download_button")
@patch("pages.ai_analysis.st.markdown")
@patch("pages.ai_analysis.st.success")
@patch("pages.ai_analysis.AIAnalysisService.save_analysis")
@patch("pages.ai_analysis.AIAnalysisService.analyze")
@patch("pages.ai_analysis.st.spinner")
@patch("pages.ai_analysis.st.button")
@patch("pages.ai_analysis.st.text_area")
@patch("pages.ai_analysis.st.subheader")
@patch("pages.ai_analysis.st.selectbox")
@patch("builtins.open", new_callable=mock_open, read_data="sample transcript")
@patch("pages.ai_analysis.get_transcripts")
@patch(
    "pages.ai_analysis.st.session_state",
    {
        "provider": "ollama",
        "model": "llama3.1",
    },
)
def test_show_ai_analysis_success(
    mock_get_transcripts,
    mock_file,
    mock_selectbox,
    mock_subheader,
    mock_text_area,
    mock_button,
    mock_spinner,
    mock_analyze,
    mock_save,
    mock_success,
    mock_markdown,
    mock_download,
    mock_divider,
    mock_render,
):
    mock_get_transcripts.return_value = [
        "sample.txt"
    ]

    mock_selectbox.side_effect = [
        "sample.txt",
        "Summary",
    ]

    mock_button.return_value = True

    spinner = MagicMock()
    spinner.__enter__.return_value = spinner
    spinner.__exit__.return_value = False

    mock_spinner.return_value = spinner

    mock_analyze.return_value = "# Summary Result"

    show_ai_analysis()

    mock_analyze.assert_called_once_with(
        provider_name="ollama",
        model_name="llama3.1",
        transcript="sample transcript",
        prompt=mock_analyze.call_args.kwargs["prompt"],
    )

    mock_save.assert_called_once_with(
        filename="sample",
        analysis_type="Summary",
        content="# Summary Result",
    )

    mock_success.assert_called_once_with(
        "✅ Analysis Completed"
    )

    mock_markdown.assert_called_once_with(
        "# Summary Result"
    )

    mock_download.assert_called_once_with(
        label="📥 Download Markdown",
        data="# Summary Result",
        file_name="Summary.md",
        mime="text/markdown",
        use_container_width=True,
    )

    mock_render.assert_called_once()


@patch("pages.ai_analysis.AnalysisHistory.render")
@patch("pages.ai_analysis.st.divider")
@patch("pages.ai_analysis.st.button")
@patch("pages.ai_analysis.st.text_area")
@patch("pages.ai_analysis.st.subheader")
@patch("pages.ai_analysis.st.selectbox")
@patch("builtins.open", new_callable=mock_open, read_data="sample transcript")
@patch("pages.ai_analysis.get_transcripts")
@patch(
    "pages.ai_analysis.st.session_state",
    {
        "provider": "ollama",
        "model": "llama3.1",
    },
)
@patch("pages.ai_analysis.AIAnalysisService.analyze")
def test_show_ai_analysis_button_not_clicked(
    mock_analyze,
    mock_get_transcripts,
    mock_file,
    mock_selectbox,
    mock_subheader,
    mock_text_area,
    mock_button,
    mock_divider,
    mock_render,
):
    mock_get_transcripts.return_value = [
        "sample.txt"
    ]

    mock_selectbox.side_effect = [
        "sample.txt",
        "Summary",
    ]

    mock_button.return_value = False

    show_ai_analysis()

    mock_analyze.assert_not_called()

    mock_render.assert_called_once()


@patch("pages.ai_analysis.AnalysisHistory.render")
@patch("pages.ai_analysis.st.divider")
@patch("pages.ai_analysis.st.download_button")
@patch("pages.ai_analysis.st.markdown")
@patch("pages.ai_analysis.st.success")
@patch("pages.ai_analysis.AIAnalysisService.save_analysis")
@patch("pages.ai_analysis.AIAnalysisService.analyze")
@patch("pages.ai_analysis.st.spinner")
@patch("pages.ai_analysis.st.button")
@patch("pages.ai_analysis.st.text_area")
@patch("pages.ai_analysis.st.subheader")
@patch("pages.ai_analysis.st.selectbox")
@patch("builtins.open", new_callable=mock_open, read_data="sample transcript")
@patch("pages.ai_analysis.get_transcripts")
@patch(
    "pages.ai_analysis.st.session_state",
    {
        "provider": "ollama",
        "model": "llama3.1",
    },
)
def test_show_ai_analysis_success(
    mock_get_transcripts,
    mock_file,
    mock_selectbox,
    mock_subheader,
    mock_text_area,
    mock_button,
    mock_spinner,
    mock_analyze,
    mock_save,
    mock_success,
    mock_markdown,
    mock_download,
    mock_divider,
    mock_render,
):
    mock_get_transcripts.return_value = [
        "sample.txt"
    ]

    mock_selectbox.side_effect = [
        "sample.txt",
        "Summary",
    ]

    mock_button.return_value = True

    spinner = MagicMock()
    spinner.__enter__.return_value = spinner
    spinner.__exit__.return_value = False

    mock_spinner.return_value = spinner

    mock_analyze.return_value = "# Summary Result"

    show_ai_analysis()

    mock_analyze.assert_called_once_with(
        provider_name="ollama",
        model_name="llama3.1",
        transcript="sample transcript",
        prompt=mock_analyze.call_args.kwargs["prompt"],
    )

    mock_save.assert_called_once_with(
        filename="sample",
        analysis_type="Summary",
        content="# Summary Result",
    )

    mock_success.assert_called_once_with(
        "✅ Analysis Completed"
    )

    mock_markdown.assert_called_once_with(
        "# Summary Result"
    )

    mock_download.assert_called_once_with(
        label="📥 Download Markdown",
        data="# Summary Result",
        file_name="Summary.md",
        mime="text/markdown",
        use_container_width=True,
    )

    mock_render.assert_called_once()


@patch("pages.ai_analysis.AnalysisHistory.render")
@patch("pages.ai_analysis.st.divider")
@patch("pages.ai_analysis.st.button")
@patch("pages.ai_analysis.st.text_area")
@patch("pages.ai_analysis.st.subheader")
@patch("pages.ai_analysis.st.selectbox")
@patch("builtins.open", new_callable=mock_open, read_data="sample transcript")
@patch("pages.ai_analysis.get_transcripts")
@patch(
    "pages.ai_analysis.st.session_state",
    {
        "provider": "ollama",
        "model": "llama3.1",
    },
)
@patch("pages.ai_analysis.AIAnalysisService.analyze")
def test_show_ai_analysis_button_not_clicked(
    mock_analyze,
    mock_get_transcripts,
    mock_file,
    mock_selectbox,
    mock_subheader,
    mock_text_area,
    mock_button,
    mock_divider,
    mock_render,
):
    mock_get_transcripts.return_value = [
        "sample.txt"
    ]

    mock_selectbox.side_effect = [
        "sample.txt",
        "Summary",
    ]

    mock_button.return_value = False

    show_ai_analysis()

    mock_analyze.assert_not_called()

    mock_render.assert_called_once()