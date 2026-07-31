"""
Transcript Reports
"""

from __future__ import annotations

import streamlit as st

from components.file_browser import show_file_browser


def show_transcript_reports():

    st.subheader("📑 Transcript Reports")

    file = show_file_browser(
        folder="transcripts",
        extension=".txt",
        key="transcript_browser",
    )

    if file is None:
        return

    transcript = file.read_text(encoding="utf-8")

    st.text_area(
        "Transcript",
        transcript,
        height=350,
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Words", len(transcript.split()))
    col2.metric("Characters", len(transcript))
    col3.metric("Lines", len(transcript.splitlines()))

    st.download_button(
        "⬇ Download TXT",
        transcript,
        file_name=file.name,
        mime="text/plain",
        use_container_width=True,
    )