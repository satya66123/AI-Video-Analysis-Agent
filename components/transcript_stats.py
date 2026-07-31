import streamlit as st

from utils.transcript_utils import TranscriptUtils


def show_transcript_stats():

    transcripts = TranscriptUtils.list_transcripts()

    total_files = len(transcripts)

    total_words = 0
    total_characters = 0

    for transcript in transcripts:

        text = TranscriptUtils.read_transcript(
            transcript
        )

        total_words += len(text.split())
        total_characters += len(text)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Transcripts",
        total_files
    )

    col2.metric(
        "Words",
        total_words
    )

    col3.metric(
        "Characters",
        total_characters
    )