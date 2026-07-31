"""
footer_agent.py

Footer Agent

Responsibilities
----------------
- Render application footer
- Display version
- Display copyright
- Display application status
"""

from __future__ import annotations

import streamlit as st


class FooterAgent:

    VERSION = "1.0.0"

    @classmethod
    def render(cls):

        st.divider()

        col1, col2, col3 = st.columns(
            3
        )

        with col1:

            st.caption(
                "🎥 AI Video Analysis Agent"
            )

        with col2:

            st.caption(
                f"Version {cls.VERSION}"
            )

        with col3:

            st.caption(
                "© 2026"
            )