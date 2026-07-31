from unittest.mock import  patch

import pytest

from components.show_ai_analysis import (

    get_transcripts,
    show_ai_analysis,
)


# ==========================================================
# Fixtures
# ==========================================================

@pytest.fixture
def mock_session_state():
    return {
        "provider": "ollama",
        "model": "llama3.1:8b",
    }


# ==========================================================
# get_transcripts()
# ==========================================================

@patch("components.show_ai_analysis.os.path.exists")
def test_get_transcripts_folder_missing(mock_exists):
    mock_exists.return_value = False

    assert get_transcripts() == []


@patch("components.show_ai_analysis.os.listdir")
@patch("components.show_ai_analysis.os.path.exists")
def test_get_transcripts_success(
    mock_exists,
    mock_listdir,
):
    mock_exists.return_value = True

    mock_listdir.return_value = [
        "b.txt",
        "a.txt",
        "ignore.pdf",
        "video.mp4",
    ]

    result = get_transcripts()

    assert result == [
        "b.txt",
        "a.txt",
    ]


# ==========================================================
# show_ai_analysis()
# ==========================================================

@patch("components.show_ai_analysis.st.warning")
@patch("components.show_ai_analysis.st.title")
@patch("components.show_ai_analysis.get_transcripts")
def test_show_ai_analysis_no_transcripts(
    mock_get_transcripts,
    mock_title,
    mock_warning,
):
    mock_get_transcripts.return_value = []

    show_ai_analysis()

    mock_title.assert_called_once()

    mock_warning.assert_called_once_with(
        "No transcripts found."
    )


@patch("components.show_ai_analysis.st.error")
@patch("components.show_ai_analysis.st.warning")
@patch("components.show_ai_analysis.st.session_state", {})
@patch("components.show_ai_analysis.st.title")
@patch("components.show_ai_analysis.get_transcripts")
def test_show_ai_analysis_missing_provider(
    mock_get_transcripts,
    mock_title,
    mock_warning,
    mock_error,
):
    mock_get_transcripts.return_value = [
        "sample.txt"
    ]

    show_ai_analysis()

    mock_error.assert_called_once_with(
        "Please select a Provider and Model from the sidebar."
    )