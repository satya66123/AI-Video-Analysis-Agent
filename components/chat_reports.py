from __future__ import annotations

import streamlit as st

from components.file_browser import show_file_browser


def show_chat_reports():

    st.subheader("💬 Chat Reports")

    file = show_file_browser(
        folder="chat_history",
        extension=".json",
        key="chat_browser",
    )

    if file is None:
        return

    st.json(file.read_text(encoding="utf-8"))

    st.download_button(
        "⬇ Download Chat",
        file.read_text(encoding="utf-8"),
        file_name=file.name,
        mime="application/json",
        use_container_width=True,
    )