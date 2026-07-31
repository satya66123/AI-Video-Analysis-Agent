"""
statusbar_agent.py

Status Bar Agent

Responsibilities
----------------
- Display workflow status
- Display current agent
- Display progress
- Display notifications
"""

from __future__ import annotations

import streamlit as st


class StatusBarAgent:

    @classmethod
    def render(cls):

        progress = st.session_state.get(
            "workflow_progress",
            0,
        )

        current = st.session_state.get(
            "current_agent",
            "Idle",
        )

        running = st.session_state.get(
            "workflow_running",
            False,
        )

        status = (
            "Running"
            if running
            else "Ready"
        )

        st.progress(
            progress / 100
        )

        col1, col2, col3 = st.columns(
            3
        )

        with col1:

            st.metric(
                "Status",
                status,
            )

        with col2:

            st.metric(
                "Progress",
                f"{progress}%"
            )

        with col3:

            st.metric(
                "Current Agent",
                current,
            )

        notifications = st.session_state.get(
            "notifications",
            [],
        )

        if notifications:

            latest = notifications[-1]

            level = latest.get(
                "level",
                "info",
            )

            message = latest.get(
                "message",
                "",
            )

            if level == "success":

                st.success(message)

            elif level == "warning":

                st.warning(message)

            elif level == "error":

                st.error(message)

            else:

                st.info(message)