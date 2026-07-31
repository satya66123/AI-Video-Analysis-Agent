import pytest
from unittest.mock import MagicMock, patch

from components.transcript_dashboard import show_transcript_dashboard


@patch("components.transcript_dashboard.st.rerun")
@patch("components.transcript_dashboard.st.success")
@patch("components.transcript_dashboard.TranscriptUtils.delete_all_transcripts")
@patch("components.transcript_dashboard.st.button")
@patch("components.transcript_dashboard.st.columns")
@patch("components.transcript_dashboard.TranscriptUtils.get_total_statistics")
def test_show_transcript_dashboard(
    mock_stats,
    mock_columns,
    mock_button,
    mock_delete,
    mock_success,
    mock_rerun,
):
    mock_stats.return_value = {
        "files": 5,
        "words": 1200,
        "characters": 6500,
        "lines": 85,
    }

    mock_button.return_value = False

    col1 = MagicMock()
    col2 = MagicMock()
    col3 = MagicMock()
    col4 = MagicMock()

    mock_columns.side_effect = [
        (col1, col2),
        (col3, col4),
    ]

    show_transcript_dashboard()

    col1.metric.assert_called_once_with(
        "📄 Transcripts",
        5,
    )

    col2.metric.assert_called_once_with(
        "📝 Words",
        1200,
    )

    col3.metric.assert_called_once_with(
        "🔤 Characters",
        6500,
    )

    col4.metric.assert_called_once_with(
        "📑 Lines",
        85,
    )

    mock_delete.assert_not_called()
    mock_success.assert_not_called()
    mock_rerun.assert_not_called()


@patch("components.transcript_dashboard.st.rerun")
@patch("components.transcript_dashboard.st.success")
@patch("components.transcript_dashboard.TranscriptUtils.delete_all_transcripts")
@patch("components.transcript_dashboard.st.button")
@patch("components.transcript_dashboard.st.columns")
@patch("components.transcript_dashboard.TranscriptUtils.get_total_statistics")
def test_show_transcript_dashboard_delete(
    mock_stats,
    mock_columns,
    mock_button,
    mock_delete,
    mock_success,
    mock_rerun,
):
    mock_stats.return_value = {
        "files": 2,
        "words": 500,
        "characters": 3000,
        "lines": 40,
    }

    mock_button.return_value = True

    col1 = MagicMock()
    col2 = MagicMock()
    col3 = MagicMock()
    col4 = MagicMock()

    mock_columns.side_effect = [
        (col1, col2),
        (col3, col4),
    ]

    show_transcript_dashboard()

    mock_delete.assert_called_once()

    mock_success.assert_called_once_with(
        "All transcripts deleted."
    )

    mock_rerun.assert_called_once()