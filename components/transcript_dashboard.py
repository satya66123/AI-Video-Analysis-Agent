import streamlit as st

from utils.transcript_utils import TranscriptUtils


def show_transcript_dashboard():

    stats = TranscriptUtils.get_total_statistics()

    col1, col2 = st.columns(2)

    col1.metric(
        "📄 Transcripts",
        stats["files"]
    )

    col2.metric(
        "📝 Words",
        stats["words"]
    )

    col3, col4 = st.columns(2)

    col3.metric(
        "🔤 Characters",
        stats["characters"]
    )

    col4.metric(
        "📑 Lines",
        stats["lines"]
    )

    if st.button(
            "🗑 Clear All Transcripts",
            use_container_width=True
    ):
        TranscriptUtils.delete_all_transcripts()

        st.success(
            "All transcripts deleted."
        )

        st.rerun()