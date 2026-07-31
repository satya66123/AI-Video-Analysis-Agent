from __future__ import annotations


import streamlit as st

from components.file_browser import show_file_browser


def show_analysis_reports() -> None:
    """Display AI Analysis Reports."""

    st.subheader("🤖 AI Analysis Reports")

    selected_file = show_file_browser(
        folder="analysis",
        extension=".md",
        key="analysis_browser",
    )

    if selected_file is None:
        return

    content = selected_file.read_text(encoding="utf-8")

    # ------------------------------------------
    # File Information
    # ------------------------------------------

    file_size = selected_file.stat().st_size / 1024
    modified = selected_file.stat().st_mtime

    col1, col2, col3 = st.columns(3)

    col1.metric("File", selected_file.name)
    col2.metric("Size", f"{file_size:.2f} KB")
    col3.metric("Words", len(content.split()))

    st.divider()

    # ------------------------------------------
    # Preview
    # ------------------------------------------

    st.markdown("### 📖 Report Preview")

    st.markdown(content)

    st.divider()

    # ------------------------------------------
    # Download Buttons
    # ------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "⬇ Download Markdown",
            data=content,
            file_name=selected_file.name,
            mime="text/markdown",
            use_container_width=True,
        )

    with col2:

        st.download_button(
            "📄 Download TXT",
            data=content,
            file_name=selected_file.stem + ".txt",
            mime="text/plain",
            use_container_width=True,
        )