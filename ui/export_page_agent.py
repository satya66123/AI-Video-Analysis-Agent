"""
export_page_agent.py

Export Page Agent
"""

from __future__ import annotations


import streamlit as st

from services.export_agent_service import ExportService

from .footer_agent import FooterAgent
from .header_agent import HeaderAgent


class ExportPageAgent:

    MIME_TYPES = {
        ".pdf": "application/pdf",
        ".html": "text/html",
        ".md": "text/markdown",
        ".txt": "text/plain",
        ".json": "application/json",
    }

    ICONS = {
        ".pdf": "📄",
        ".html": "🌐",
        ".md": "📝",
        ".txt": "📃",
        ".json": "🗂️",
    }

    def render(self):

        HeaderAgent.render("📤 Export Files")

        files = ExportService.list_exports()

        if not files:

            st.info("No exported files found.")

            FooterAgent.render()

            return

        st.success(
            f"{len(files)} exported file(s) found."
        )

        grouped = {}

        for file in files:

            folder = file.parent.name.upper()

            grouped.setdefault(
                folder,
                []
            ).append(file)

        for folder, folder_files in grouped.items():

            st.subheader(
                f"📂 {folder}"
            )

            for file in folder_files:

                suffix = file.suffix.lower()

                with st.expander(
                    f"{self.ICONS.get(suffix,'📁')} {file.name}",
                    expanded=False,
                ):

                    st.caption(
                        f"Size: {file.stat().st_size:,} bytes"
                    )

                    if suffix in (
                        ".txt",
                        ".md",
                        ".json",
                        ".html",
                    ):

                        try:

                            content = file.read_text(
                                encoding="utf-8"
                            )

                            st.text_area(
                                "Preview",
                                value=content,
                                height=250,
                                disabled=True,
                                key=f"preview_{file.name}",
                            )

                        except Exception:

                            st.warning(
                                "Preview unavailable."
                            )

                    col1, col2 = st.columns(2)

                    with col1:

                        with open(
                            file,
                            "rb",
                        ) as f:

                            st.download_button(
                                label="📥 Download",
                                data=f.read(),
                                file_name=file.name,
                                mime=self.MIME_TYPES.get(
                                    suffix,
                                    "application/octet-stream",
                                ),
                                key=f"download_{file.name}",
                                use_container_width=True,
                            )

                    with col2:

                        if st.button(
                            "🗑 Delete",
                            key=f"delete_{file.name}",
                            use_container_width=True,
                        ):

                            file.unlink()

                            st.success(
                                "File deleted successfully."
                            )

                            st.rerun()

        FooterAgent.render()