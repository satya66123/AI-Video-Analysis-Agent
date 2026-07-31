import io
import zipfile

import streamlit as st

from utils.transcript_utils import TranscriptUtils


def show_export_transcripts():

    transcripts = TranscriptUtils.list_transcripts()

    if not transcripts:
        return

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        for transcript in transcripts:

            text = TranscriptUtils.read_transcript(
                transcript
            )

            zip_file.writestr(
                transcript,
                text
            )

    st.download_button(
        label="📦 Download All Transcripts",
        data=zip_buffer.getvalue(),
        file_name="transcripts.zip",
        mime="application/zip",
        use_container_width=True
    )
"""
Transcript Reports Component
"""


def show_transcript_reports() -> None:
    """Render Transcript Reports tab."""

    st.subheader("📑 Transcript Reports")

    transcript = st.session_state.get("transcript", "")

    if not transcript:
        st.info("No transcript available.")
        return

    st.text_area(
        "Transcript",
        transcript,
        height=350,
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Words",
            len(transcript.split())
        )

    with col2:
        st.metric(
            "Characters",
            len(transcript)
        )

    with col3:
        st.metric(
            "Lines",
            len(transcript.splitlines())
        )

    st.divider()

    st.download_button(
        "⬇ Download TXT",
        transcript,
        file_name="transcript.txt",
        mime="text/plain",
        use_container_width=True,
    )