"""
about_page_agent.py
"""

from __future__ import annotations

import streamlit as st

from .header_agent import HeaderAgent
from .footer_agent import FooterAgent


class AboutPageAgent:

    VERSION = "1.0.0"

    def render(self):

        HeaderAgent.render("ℹ About")

        st.title("AI Video Analysis Agent")

        st.write(
            """
AI Video Analysis Agent is an end-to-end
AI-powered application for analyzing videos,
extracting audio, generating transcripts,
performing AI analysis, creating reports,
exporting results, and interacting with
the processed content using an AI chat assistant.
"""
        )

        st.subheader("Features")

        st.markdown(
            """
- Video Upload
- Audio Extraction
- Speech-to-Text
- AI Analysis
- Report Generation
- Export Results
- AI Chat
- Workflow Dashboard
- History Management
- Multi-Provider AI Support
"""
        )

        st.subheader("Technology Stack")

        st.markdown(
            """
- Python
- Streamlit
- Ollama
- OpenAI
- Anthropic
- Whisper
- FFmpeg
- MySQL
"""
        )

        st.subheader("Version")

        st.info(self.VERSION)

        FooterAgent.render()