import pytest
from unittest.mock import MagicMock, patch

from components.transcript_metadata import show_transcript_metadata


@pytest.fixture
def sample_metadata():
    return {
        "Words": 1250,
        "Characters": 7820,
        "Lines": 145,
        "Reading Time": "5 min",
        "Size": "18 KB",
    }


@patch("components.transcript_metadata.st.columns")
def test_show_transcript_metadata(
    mock_columns,
    sample_metadata,
):
    col1 = MagicMock()
    col2 = MagicMock()
    col3 = MagicMock()
    col4 = MagicMock()
    col5 = MagicMock()

    mock_columns.side_effect = [
        (col1, col2, col3),
        (col4, col5),
    ]

    show_transcript_metadata(sample_metadata)

    mock_columns.assert_any_call(3)
    mock_columns.assert_any_call(2)

    col1.metric.assert_called_once_with(
        "Words",
        1250,
    )

    col2.metric.assert_called_once_with(
        "Characters",
        7820,
    )

    col3.metric.assert_called_once_with(
        "Lines",
        145,
    )

    col4.metric.assert_called_once_with(
        "Reading Time",
        "5 min",
    )

    col5.metric.assert_called_once_with(
        "File Size",
        "18 KB",
    )