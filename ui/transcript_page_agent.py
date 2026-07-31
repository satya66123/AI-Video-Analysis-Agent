"""
transcript_page_agent.py

Transcript Page Agent
"""

from __future__ import annotations

import streamlit as st

from services.speech_agent_service  import SpeechService

from .header_agent import HeaderAgent
from .footer_agent import FooterAgent


class TranscriptPageAgent:

    def __init__(self):
        pass

    def render(self):

        HeaderAgent.render("📝 Transcripts")

        transcripts = SpeechService.list_transcripts()

        if not transcripts:

            st.info(
                "No transcripts found."
            )

            FooterAgent.render()

            return

        st.success(
            f"{len(transcripts)} transcript(s) found."
        )

        for transcript in transcripts:

            filename = transcript["name"]

            with st.expander(
                f"📄 {filename}",
                expanded=False,
            ):

                st.caption(
                    f"Size: {transcript['size']:,} bytes"
                )

                content = SpeechService.load_transcript(
                    filename
                )

                st.text_area(
                    "Transcript",
                    value=content,
                    height=350,
                    disabled=True,
                    key=f"preview_{filename}",
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.download_button(
                        label="💾 Download",
                        data=content,
                        file_name=filename,
                        mime="text/plain",
                        key=f"download_{filename}",
                        use_container_width=True,
                    )

                with col2:

                    if st.button(
                        "💬 Chat",
                        key=f"chat_{filename}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            "selected_transcript"
                        ] = filename

                        st.switch_page(
                            "Chat"
                        )

                with col3:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{filename}",
                        use_container_width=True,
                    ):

                        SpeechService.delete_transcript(
                            filename
                        )

                        st.success(
                            "Transcript deleted successfully."
                        )

                        st.rerun()

        FooterAgent.render()