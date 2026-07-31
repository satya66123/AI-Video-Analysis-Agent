"""
header_agent.py

Header Agent

Responsibilities
----------------
- Display page title
- Display provider
- Display model
- Display workflow status
"""

from __future__ import annotations

import streamlit as st


class HeaderAgent:

    @classmethod
    def render(
        cls,
        title: str,
    ):

        col1, col2 = st.columns(
            [3, 1]
        )

        with col1:

            st.title(title)

        with col2:

            st.caption(
                f"Provider: "
                f"{st.session_state.provider}"
            )

            st.caption(
                f"Model: "
                f"{st.session_state.model}"
            )

        st.divider()