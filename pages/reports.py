from __future__ import annotations

import streamlit as st


from components.transcript_reports import show_transcript_reports
from components.analysis_reports import show_analysis_reports
from components.chat_reports import show_chat_reports
from components.report_preview import show_report_preview
from components.download_reports import show_download_center


def show_reports() -> None:
    """
    Reports Page
    """

    st.title("📄 Reports")

    st.caption(
        "View, manage and export transcripts, AI analysis, chat history and reports."
    )

    st.divider()

    (
        transcript_tab,
        analysis_tab,
        chat_tab,
        summary_tab,
        export_tab,
    ) = st.tabs(
        [
            "📑 Transcript Reports",
            "🤖 AI Analysis Reports",
            "💬 Chat Reports",
            "📊 Summary Report",
            "📥 Export Center",
        ]
    )

    ###############################################################
    # Transcript Reports
    ###############################################################

    with transcript_tab:

        show_transcript_reports()

    ###############################################################
    # AI Analysis Reports
    ###############################################################

    with analysis_tab:

        show_analysis_reports()

    ###############################################################
    # Chat Reports
    ###############################################################

    with chat_tab:

        show_chat_reports()

    ###############################################################
    # Summary Report
    ###############################################################

    with summary_tab:

        show_report_preview()

    ###############################################################
    # Export Center
    ###############################################################

    with export_tab:

        show_download_center()