import os
from unittest.mock import MagicMock, patch

import pytest

from components.transcript import show_transcripts


# ==========================================================
# Fixtures
# ==========================================================

@pytest.fixture
def sample_transcript():
    return "d5241d3e-adac-40fd-ad7b-b4de56136f67.txt"


@pytest.fixture
def sample_text():
    return (
        "This is a sample transcript.\n"
        "Second line.\n"
        "Third line."
    )


@pytest.fixture
def sample_metadata():
    return {
        "Created": "2026-07-30",
        "Words": 8,
        "Characters": 45,
        "Reading Time": "1 min",
    }


# ==========================================================
# No transcript
# ==========================================================

@patch("components.transcript.st.info")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
@patch("components.transcript.TranscriptUtils.list_transcripts")
def test_show_transcript_no_transcript(
    mock_list,
    mock_selectbox,
    mock_text_input,
    mock_info,
):
    mock_list.return_value = []

    mock_selectbox.return_value = "Newest"

    mock_text_input.return_value = ""

    show_transcripts()

    mock_info.assert_called_once_with(
        "📄 No transcripts found.\n\nGenerate a transcript first."
    )




# ==========================================================
# Sort A-Z
# ==========================================================

@patch("components.transcript.st.container")
@patch("components.transcript.st.columns")
@patch("components.transcript.st.expander")
@patch("components.transcript.st.info")
@patch("components.transcript.st.caption")
@patch("components.transcript.st.subheader")
@patch("components.transcript.st.markdown")
@patch("components.transcript.st.code")
@patch("components.transcript.st.text_area")
@patch("components.transcript.st.download_button")
@patch("components.transcript.st.button")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
@patch("components.transcript.show_transcript_metadata")
@patch("components.transcript.TranscriptMetadata.get_metadata")
@patch("components.transcript.TranscriptUtils.read_transcript")
@patch("components.transcript.TranscriptValidator.validate")
@patch("components.transcript.TranscriptUtils.list_transcripts")
def test_show_transcript_sort_az(
    mock_list,
    mock_validate,
    mock_read,
    mock_metadata,
    mock_show_metadata,
    mock_selectbox,
    mock_text_input,
    mock_button,
    mock_download,
    mock_text_area,
    mock_code,
    mock_markdown,
    mock_subheader,
    mock_caption,
    mock_info,
    mock_expander,
    mock_columns,
    mock_container,
    sample_metadata,
    sample_text,
):
    mock_list.return_value = [
        "b.txt",
        "a.txt",
    ]

    mock_validate.return_value = True

    mock_read.return_value = sample_text

    mock_metadata.return_value = sample_metadata

    mock_selectbox.return_value = "A-Z"

    mock_text_input.return_value = ""

    mock_button.return_value = False

    mock_container.return_value.__enter__.return_value = MagicMock()
    mock_container.return_value.__exit__.return_value = False

    mock_expander.return_value.__enter__.return_value = MagicMock()
    mock_expander.return_value.__exit__.return_value = False

    mock_columns.return_value = (
        MagicMock(),
        MagicMock(),
    )

    show_transcripts()

    mock_subheader.assert_called_once_with(
        "📄 Saved Transcripts"
    )

    mock_caption.assert_any_call(
        "2 transcript(s) available"
    )
    
# ==========================================================
# Rename Success
# ==========================================================

@patch("components.transcript.st.rerun")
@patch("components.transcript.st.success")
@patch("components.transcript.st.columns")
@patch("components.transcript.st.expander")
@patch("components.transcript.st.container")
@patch("components.transcript.show_transcript_metadata")
@patch("components.transcript.TranscriptMetadata.get_metadata")
@patch("components.transcript.TranscriptValidator.validate")
@patch("components.transcript.TranscriptUtils.read_transcript")
@patch("components.transcript.TranscriptUtils.rename_transcript")
@patch("components.transcript.TranscriptUtils.list_transcripts")
@patch("components.transcript.st.download_button")
@patch("components.transcript.st.code")
@patch("components.transcript.st.text_area")
@patch("components.transcript.st.caption")
@patch("components.transcript.st.info")
@patch("components.transcript.st.markdown")
@patch("components.transcript.st.subheader")
@patch("components.transcript.st.button")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
def test_show_transcript_rename_success(
    mock_selectbox,
    mock_text_input,
    mock_button,
    mock_subheader,
    mock_markdown,
    mock_info,
    mock_caption,
    mock_text_area,
    mock_code,
    mock_download,
    mock_list,
    mock_rename,
    mock_read,
    mock_validate,
    mock_metadata,
    mock_show_metadata,
    mock_container,
    mock_expander,
    mock_columns,
    mock_success,
    mock_rerun,
    sample_text,
    sample_metadata,
):
    mock_list.return_value = ["sample.txt"]

    mock_selectbox.return_value = "Newest"

    mock_text_input.side_effect = [
        "",
        "sample",
        "",
    ]

    def button_side_effect(*args, **kwargs):
        return kwargs.get("key") == "rename_btn_sample.txt"

    mock_button.side_effect = button_side_effect

    mock_rename.return_value = True

    mock_validate.return_value = True

    mock_read.return_value = sample_text

    mock_metadata.return_value = sample_metadata

    mock_container.return_value.__enter__.return_value = MagicMock()
    mock_container.return_value.__exit__.return_value = False

    mock_expander.return_value.__enter__.return_value = MagicMock()
    mock_expander.return_value.__exit__.return_value = False

    mock_columns.return_value = (
        MagicMock(),
        MagicMock(),
    )

    show_transcripts()

    mock_rename.assert_called_once_with(
        "sample.txt",
        "sample",
    )

    mock_success.assert_any_call(
        "Transcript renamed."
    )

    mock_rerun.assert_called_once()


# ==========================================================
# Rename Failure
# ==========================================================

@patch("components.transcript.st.error")
@patch("components.transcript.st.columns")
@patch("components.transcript.st.expander")
@patch("components.transcript.st.container")
@patch("components.transcript.show_transcript_metadata")
@patch("components.transcript.TranscriptMetadata.get_metadata")
@patch("components.transcript.TranscriptValidator.validate")
@patch("components.transcript.TranscriptUtils.read_transcript")
@patch("components.transcript.TranscriptUtils.rename_transcript")
@patch("components.transcript.TranscriptUtils.list_transcripts")
@patch("components.transcript.st.download_button")
@patch("components.transcript.st.code")
@patch("components.transcript.st.text_area")
@patch("components.transcript.st.caption")
@patch("components.transcript.st.info")
@patch("components.transcript.st.markdown")
@patch("components.transcript.st.subheader")
@patch("components.transcript.st.button")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
def test_show_transcript_rename_failure(
    mock_selectbox,
    mock_text_input,
    mock_button,
    mock_subheader,
    mock_markdown,
    mock_info,
    mock_caption,
    mock_text_area,
    mock_code,
    mock_download,
    mock_list,
    mock_rename,
    mock_read,
    mock_validate,
    mock_metadata,
    mock_show_metadata,
    mock_container,
    mock_expander,
    mock_columns,
    mock_error,
    sample_text,
    sample_metadata,
):
    mock_list.return_value = ["sample.txt"]

    mock_selectbox.return_value = "Newest"

    mock_text_input.side_effect = [
        "",
        "sample",
        "",
    ]

    def button_side_effect(*args, **kwargs):
        return kwargs.get("key") == "rename_btn_sample.txt"

    mock_button.side_effect = button_side_effect

    mock_rename.return_value = False

    mock_validate.return_value = True

    mock_read.return_value = sample_text

    mock_metadata.return_value = sample_metadata

    mock_container.return_value.__enter__.return_value = MagicMock()
    mock_container.return_value.__exit__.return_value = False

    mock_expander.return_value.__enter__.return_value = MagicMock()
    mock_expander.return_value.__exit__.return_value = False

    mock_columns.return_value = (
        MagicMock(),
        MagicMock(),
    )

    show_transcripts()

    mock_error.assert_any_call(
        "Transcript already exists."
    )


# ==========================================================
# Corrupted Transcript
# ==========================================================

@patch("components.transcript.st.error")
@patch("components.transcript.st.container")
@patch("components.transcript.TranscriptValidator.validate")
@patch("components.transcript.TranscriptUtils.list_transcripts")
@patch("components.transcript.st.button")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
@patch("components.transcript.st.markdown")
@patch("components.transcript.st.subheader")
@patch("components.transcript.st.caption")
def test_show_transcript_invalid_transcript(
    mock_caption,
    mock_subheader,
    mock_markdown,
    mock_selectbox,
    mock_text_input,
    mock_button,
    mock_list,
    mock_validate,
    mock_container,
    mock_error,
):
    mock_list.return_value = ["sample.txt"]

    mock_selectbox.return_value = "Newest"

    mock_text_input.side_effect = [
        "",
        "sample",
    ]

    mock_button.return_value = False

    mock_validate.return_value = False

    mock_container.return_value.__enter__.return_value = MagicMock()
    mock_container.return_value.__exit__.return_value = False

    show_transcripts()

    mock_error.assert_any_call(
        "Transcript is corrupted."
    )


# ==========================================================
# Filter removes all transcript
# ==========================================================

@patch("components.transcript.st.info")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
@patch("components.transcript.TranscriptUtils.list_transcripts")
def test_show_transcript_filter_no_match(
    mock_list,
    mock_selectbox,
    mock_text_input,
    mock_info,
):
    mock_list.return_value = [
        "sample.txt"
    ]

    mock_selectbox.return_value = "Newest"

    mock_text_input.return_value = "xyz"

    show_transcripts()

    mock_info.assert_called_once()
    
# ==========================================================
# Short Transcript Badge
# ==========================================================

@patch("components.transcript.st.success")
@patch("components.transcript.st.columns")
@patch("components.transcript.st.expander")
@patch("components.transcript.st.container")
@patch("components.transcript.show_transcript_metadata")
@patch("components.transcript.TranscriptMetadata.get_metadata")
@patch("components.transcript.TranscriptValidator.validate")
@patch("components.transcript.TranscriptUtils.read_transcript")
@patch("components.transcript.TranscriptUtils.list_transcripts")
@patch("components.transcript.st.download_button")
@patch("components.transcript.st.code")
@patch("components.transcript.st.text_area")
@patch("components.transcript.st.caption")
@patch("components.transcript.st.info")
@patch("components.transcript.st.markdown")
@patch("components.transcript.st.subheader")
@patch("components.transcript.st.button")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
def test_show_transcripts_short_badge(
    mock_selectbox,
    mock_text_input,
    mock_button,
    mock_subheader,
    mock_markdown,
    mock_info,
    mock_caption,
    mock_text_area,
    mock_code,
    mock_download,
    mock_list,
    mock_read,
    mock_validate,
    mock_metadata,
    mock_show_metadata,
    mock_container,
    mock_expander,
    mock_columns,
    mock_success,
    sample_metadata,
):
    mock_list.return_value = ["sample.txt"]

    mock_selectbox.return_value = "Newest"

    mock_text_input.side_effect = [
        "",
        "sample",
        "",
    ]

    mock_button.return_value = False

    mock_validate.return_value = True

    mock_read.return_value = "word " * 100

    mock_metadata.return_value = sample_metadata

    mock_container.return_value.__enter__.return_value = MagicMock()
    mock_container.return_value.__exit__.return_value = False

    mock_expander.return_value.__enter__.return_value = MagicMock()
    mock_expander.return_value.__exit__.return_value = False

    mock_columns.return_value = (
        MagicMock(),
        MagicMock(),
    )

    show_transcripts()

    mock_success.assert_any_call(
        "🟢 Short Transcript"
    )


# ==========================================================
# Medium Transcript Badge
# ==========================================================

@patch("components.transcript.st.info")
@patch("components.transcript.st.columns")
@patch("components.transcript.st.expander")
@patch("components.transcript.st.container")
@patch("components.transcript.show_transcript_metadata")
@patch("components.transcript.TranscriptMetadata.get_metadata")
@patch("components.transcript.TranscriptValidator.validate")
@patch("components.transcript.TranscriptUtils.read_transcript")
@patch("components.transcript.TranscriptUtils.list_transcripts")
@patch("components.transcript.st.download_button")
@patch("components.transcript.st.code")
@patch("components.transcript.st.text_area")
@patch("components.transcript.st.caption")
@patch("components.transcript.st.markdown")
@patch("components.transcript.st.subheader")
@patch("components.transcript.st.button")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
def test_show_transcripts_medium_badge(
    mock_selectbox,
    mock_text_input,
    mock_button,
    mock_subheader,
    mock_markdown,
    mock_caption,
    mock_text_area,
    mock_code,
    mock_download,
    mock_list,
    mock_read,
    mock_validate,
    mock_metadata,
    mock_show_metadata,
    mock_container,
    mock_expander,
    mock_columns,
    mock_info,
    sample_metadata,
):
    mock_list.return_value = ["sample.txt"]

    mock_selectbox.return_value = "Newest"

    mock_text_input.side_effect = [
        "",
        "sample",
        "",
    ]

    mock_button.return_value = False

    mock_validate.return_value = True

    mock_read.return_value = "word " * 500

    mock_metadata.return_value = sample_metadata

    mock_container.return_value.__enter__.return_value = MagicMock()
    mock_container.return_value.__exit__.return_value = False

    mock_expander.return_value.__enter__.return_value = MagicMock()
    mock_expander.return_value.__exit__.return_value = False

    mock_columns.return_value = (
        MagicMock(),
        MagicMock(),
    )

    show_transcripts()

    mock_info.assert_any_call(
        "🟡 Medium Transcript"
    )


# ==========================================================
# Long Transcript Badge
# ==========================================================

@patch("components.transcript.st.warning")
@patch("components.transcript.st.columns")
@patch("components.transcript.st.expander")
@patch("components.transcript.st.container")
@patch("components.transcript.show_transcript_metadata")
@patch("components.transcript.TranscriptMetadata.get_metadata")
@patch("components.transcript.TranscriptValidator.validate")
@patch("components.transcript.TranscriptUtils.read_transcript")
@patch("components.transcript.TranscriptUtils.list_transcripts")
@patch("components.transcript.st.download_button")
@patch("components.transcript.st.code")
@patch("components.transcript.st.text_area")
@patch("components.transcript.st.caption")
@patch("components.transcript.st.info")
@patch("components.transcript.st.markdown")
@patch("components.transcript.st.subheader")
@patch("components.transcript.st.button")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
def test_show_transcripts_long_badge(
    mock_selectbox,
    mock_text_input,
    mock_button,
    mock_subheader,
    mock_markdown,
    mock_info,
    mock_caption,
    mock_text_area,
    mock_code,
    mock_download,
    mock_list,
    mock_read,
    mock_validate,
    mock_metadata,
    mock_show_metadata,
    mock_container,
    mock_expander,
    mock_columns,
    mock_warning,
    sample_metadata,
):
    mock_list.return_value = ["sample.txt"]

    mock_selectbox.return_value = "Newest"

    mock_text_input.side_effect = [
        "",
        "sample",
        "",
    ]

    mock_button.return_value = False

    mock_validate.return_value = True

    mock_read.return_value = "word " * 1500

    mock_metadata.return_value = sample_metadata

    mock_container.return_value.__enter__.return_value = MagicMock()
    mock_container.return_value.__exit__.return_value = False

    mock_expander.return_value.__enter__.return_value = MagicMock()
    mock_expander.return_value.__exit__.return_value = False

    mock_columns.return_value = (
        MagicMock(),
        MagicMock(),
    )

    show_transcripts()

    mock_warning.assert_any_call(
        "🔴 Long Transcript"
    )

# ==========================================================
# Delete Transcript
# ==========================================================

@patch("components.transcript.st.rerun")
@patch("components.transcript.st.success")
@patch("components.transcript.TranscriptUtils.delete_transcript")
@patch("components.transcript.st.columns")
@patch("components.transcript.st.expander")
@patch("components.transcript.st.container")
@patch("components.transcript.show_transcript_metadata")
@patch("components.transcript.TranscriptMetadata.get_metadata")
@patch("components.transcript.TranscriptValidator.validate")
@patch("components.transcript.TranscriptUtils.read_transcript")
@patch("components.transcript.TranscriptUtils.list_transcripts")
@patch("components.transcript.st.download_button")
@patch("components.transcript.st.code")
@patch("components.transcript.st.text_area")
@patch("components.transcript.st.caption")
@patch("components.transcript.st.info")
@patch("components.transcript.st.markdown")
@patch("components.transcript.st.subheader")
@patch("components.transcript.st.button")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
def test_show_transcripts_delete(
    mock_selectbox,
    mock_text_input,
    mock_button,
    mock_subheader,
    mock_markdown,
    mock_info,
    mock_caption,
    mock_text_area,
    mock_code,
    mock_download,
    mock_list,
    mock_read,
    mock_validate,
    mock_metadata,
    mock_show_metadata,
    mock_container,
    mock_expander,
    mock_columns,
    mock_delete,
    mock_success,
    mock_rerun,
    sample_text,
    sample_metadata,
):
    mock_list.return_value = ["sample.txt"]

    mock_selectbox.return_value = "Newest"

    mock_text_input.side_effect = [
        "",
        "sample",
        "",
    ]

    def button_side_effect(*args, **kwargs):
        return kwargs.get("key") == "delete_sample.txt"

    mock_button.side_effect = button_side_effect

    mock_validate.return_value = True
    mock_read.return_value = sample_text
    mock_metadata.return_value = sample_metadata

    mock_container.return_value.__enter__.return_value = MagicMock()
    mock_container.return_value.__exit__.return_value = False

    mock_expander.return_value.__enter__.return_value = MagicMock()
    mock_expander.return_value.__exit__.return_value = False

    mock_columns.return_value = (
        MagicMock(),
        MagicMock(),
    )

    show_transcripts()

    mock_delete.assert_called_once_with(
        "sample.txt"
    )

    mock_success.assert_any_call(
        "Transcript deleted."
    )

    mock_rerun.assert_called_once()


# ==========================================================
# Download Button
# ==========================================================

@patch("components.transcript.st.download_button")
@patch("components.transcript.st.columns")
@patch("components.transcript.st.expander")
@patch("components.transcript.st.container")
@patch("components.transcript.show_transcript_metadata")
@patch("components.transcript.TranscriptMetadata.get_metadata")
@patch("components.transcript.TranscriptValidator.validate")
@patch("components.transcript.TranscriptUtils.read_transcript")
@patch("components.transcript.TranscriptUtils.list_transcripts")
@patch("components.transcript.st.code")
@patch("components.transcript.st.text_area")
@patch("components.transcript.st.caption")
@patch("components.transcript.st.info")
@patch("components.transcript.st.markdown")
@patch("components.transcript.st.subheader")
@patch("components.transcript.st.button")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
def test_show_transcripts_download(
    mock_selectbox,
    mock_text_input,
    mock_button,
    mock_subheader,
    mock_markdown,
    mock_info,
    mock_caption,
    mock_text_area,
    mock_code,
    mock_list,
    mock_read,
    mock_validate,
    mock_metadata,
    mock_show_metadata,
    mock_container,
    mock_expander,
    mock_columns,
    mock_download,
    sample_text,
    sample_metadata,
):
    mock_list.return_value = ["sample.txt"]

    mock_selectbox.return_value = "Newest"

    mock_text_input.side_effect = [
        "",
        "sample",
        "",
    ]

    mock_button.return_value = False

    mock_validate.return_value = True
    mock_read.return_value = sample_text
    mock_metadata.return_value = sample_metadata

    mock_container.return_value.__enter__.return_value = MagicMock()
    mock_container.return_value.__exit__.return_value = False

    mock_expander.return_value.__enter__.return_value = MagicMock()
    mock_expander.return_value.__exit__.return_value = False

    mock_columns.return_value = (
        MagicMock(),
        MagicMock(),
    )

    show_transcripts()

    mock_download.assert_called_once_with(
        label="⬇ Download Transcript",
        data=sample_text,
        file_name="sample.txt",
        mime="text/plain",
        use_container_width=True,
    )


# ==========================================================
# Search Transcript
# ==========================================================

@patch("components.transcript.st.code")
@patch("components.transcript.st.columns")
@patch("components.transcript.st.expander")
@patch("components.transcript.st.container")
@patch("components.transcript.show_transcript_metadata")
@patch("components.transcript.TranscriptMetadata.get_metadata")
@patch("components.transcript.TranscriptValidator.validate")
@patch("components.transcript.TranscriptUtils.read_transcript")
@patch("components.transcript.TranscriptUtils.list_transcripts")
@patch("components.transcript.st.download_button")
@patch("components.transcript.st.text_area")
@patch("components.transcript.st.caption")
@patch("components.transcript.st.info")
@patch("components.transcript.st.markdown")
@patch("components.transcript.st.subheader")
@patch("components.transcript.st.button")
@patch("components.transcript.st.text_input")
@patch("components.transcript.st.selectbox")
def test_show_transcripts_search(
    mock_selectbox,
    mock_text_input,
    mock_button,
    mock_subheader,
    mock_markdown,
    mock_info,
    mock_caption,
    mock_text_area,
    mock_download,
    mock_list,
    mock_read,
    mock_validate,
    mock_metadata,
    mock_show_metadata,
    mock_container,
    mock_expander,
    mock_columns,
    mock_code,
    sample_metadata,
):
    transcript = (
        "apple\n"
        "banana\n"
        "orange\n"
    )

    mock_list.return_value = ["sample.txt"]

    mock_selectbox.return_value = "Newest"

    mock_text_input.side_effect = [
        "",
        "sample",
        "banana",
    ]

    mock_button.return_value = False

    mock_validate.return_value = True
    mock_read.return_value = transcript
    mock_metadata.return_value = sample_metadata

    mock_container.return_value.__enter__.return_value = MagicMock()
    mock_container.return_value.__exit__.return_value = False

    mock_expander.return_value.__enter__.return_value = MagicMock()
    mock_expander.return_value.__exit__.return_value = False

    mock_columns.return_value = (
        MagicMock(),
        MagicMock(),
    )

    show_transcripts()

    mock_code.assert_called_with(
        "banana",
        language="text",
    )