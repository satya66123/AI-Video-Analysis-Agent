from __future__ import annotations

from pathlib import Path
from datetime import datetime

import streamlit as st


def show_export_center():

    st.subheader("📦 Export Center")

    export_folder = Path("exports")
    export_folder.mkdir(exist_ok=True)

    files = sorted(
        export_folder.glob("*.*"),
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )

    if not files:
        st.info("No exported reports found.")
        return

    ####################################################################
    # Statistics
    ####################################################################

    pdf_count = len(list(export_folder.glob("*.pdf")))
    html_count = len(list(export_folder.glob("*.html")))
    md_count = len(list(export_folder.glob("*.md")))
    txt_count = len(list(export_folder.glob("*.txt")))

    total_size = sum(f.stat().st_size for f in files) / (1024 * 1024)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Files", len(files))
    c2.metric("PDF", pdf_count)
    c3.metric("HTML", html_count)
    c4.metric("Markdown", md_count)
    c5.metric("TXT", txt_count)

    st.caption(f"Storage Used : {total_size:.2f} MB")

    st.divider()

    ####################################################################
    # Search
    ####################################################################

    keyword = st.text_input(
        "🔍 Search",
        placeholder="Search exported reports...",
    )

    if keyword:

        files = [
            f
            for f in files
            if keyword.lower() in f.name.lower()
        ]

    if not files:

        st.warning("No matching reports.")
        return

    ####################################################################
    # File Selection
    ####################################################################

    selected = st.selectbox(
        "Select Export",
        files,
        format_func=lambda x: x.name,
    )

    st.divider()

    ####################################################################
    # Information
    ####################################################################

    st.write(f"**Filename :** {selected.name}")
    st.write(f"**Type :** {selected.suffix.upper()}")

    size = selected.stat().st_size / 1024

    st.write(f"**Size :** {size:.2f} KB")

    modified = datetime.fromtimestamp(
        selected.stat().st_mtime
    )

    st.write(
        f"**Modified :** {modified.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    st.divider()

    ####################################################################
    # Preview
    ####################################################################

    suffix = selected.suffix.lower()

    if suffix in [".txt", ".md", ".html"]:

        content = selected.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        st.text_area(
            "Preview",
            content,
            height=400,
        )

    elif suffix == ".pdf":

        st.info("PDF preview is not available.")

    st.divider()

    ####################################################################
    # Download
    ####################################################################

    with open(selected, "rb") as f:

        st.download_button(
            "⬇ Download",
            data=f,
            file_name=selected.name,
            mime="application/octet-stream",
            use_container_width=True,
        )

    st.divider()

    ####################################################################
    # Delete
    ####################################################################

    if st.button(
        "🗑 Delete Export",
        use_container_width=True,
        type="secondary",
    ):

        selected.unlink()

        st.success("Export deleted successfully.")

        st.rerun()