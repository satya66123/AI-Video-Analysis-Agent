from __future__ import annotations

from pathlib import Path

import streamlit as st


def show_download_center() -> None:
    """Render Export Center."""

    st.subheader("📥 Export Center")

    export_folder = Path("exports")
    export_folder.mkdir(exist_ok=True)

    if not any(export_folder.iterdir()):
        st.info("No exported reports found.")
        return

    ####################################################################
    # Latest Export Files
    ####################################################################

    pdf_files = sorted(export_folder.glob("*.pdf"))
    md_files = sorted(export_folder.glob("*.md"))
    html_files = sorted(export_folder.glob("*.html"))
    txt_files = sorted(export_folder.glob("*.txt"))

    ####################################################################
    # Export Statistics
    ####################################################################

    pdf_files = sorted(export_folder.glob("*.pdf"))
    md_files = sorted(export_folder.glob("*.md"))
    html_files = sorted(export_folder.glob("*.html"))
    txt_files = sorted(export_folder.glob("*.txt"))

    total_files = (
            len(pdf_files)
            + len(md_files)
            + len(html_files)
            + len(txt_files)
    )

    st.markdown("### 📊 Export Summary")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total", total_files)
    c2.metric("PDF", len(pdf_files))
    c3.metric("Markdown", len(md_files))
    c4.metric("HTML", len(html_files))
    c5.metric("TXT", len(txt_files))

    st.divider()

    ####################################################################
    # Download Center
    ####################################################################

    st.markdown("### ⬇ Download Exports")

    col1, col2 = st.columns(2)

    ####################################################################
    # LEFT COLUMN
    ####################################################################

    with col1:

        # PDF
        if pdf_files:

            selected_pdf = st.selectbox(
                "📄 PDF Files",
                pdf_files,
                format_func=lambda x: x.name,
                key="download_pdf",
            )

            with open(selected_pdf, "rb") as file:

                downloaded=st.download_button(
                    "⬇ Download PDF",
                    data=file,
                    file_name=selected_pdf.name,
                    mime="application/pdf",
                    use_container_width=True,
                )
                if downloaded:
                    st.success(f"✅ Successfully downloaded: {selected_pdf.name}")

        else:

            st.info("No PDF files found.")

        # Markdown
        if md_files:

            selected_md = st.selectbox(
                "📝 Markdown Files",
                md_files,
                format_func=lambda x: x.name,
                key="download_md",
            )

            with open(selected_md, "rb") as file:

                downloaded=st.download_button(
                    "⬇ Download Markdown",
                    data=file,
                    file_name=selected_md.name,
                    mime="text/markdown",
                    use_container_width=True,
                )
                if downloaded:
                    st.success(f"✅ Successfully downloaded: {selected_md.name}")

        else:

            st.info("No Markdown files found.")

    ####################################################################
    # RIGHT COLUMN
    ####################################################################

    with col2:

        # HTML
        if html_files:

            selected_html = st.selectbox(
                "🌐 HTML Files",
                html_files,
                format_func=lambda x: x.name,
                key="download_html",
            )

            with open(selected_html, "rb") as file:

                downloaded=st.download_button(
                    "⬇ Download HTML",
                    data=file,
                    file_name=selected_html.name,
                    mime="text/html",
                    use_container_width=True,
                )
                if downloaded:
                    st.success(f"✅ Successfully downloaded: {selected_html.name}")

        else:

            st.info("No HTML files found.")

        # TXT
        if txt_files:

            selected_txt = st.selectbox(
                "📃 TXT Files",
                txt_files,
                format_func=lambda x: x.name,
                key="download_txt",
            )

            with open(selected_txt, "rb") as file:

                downloaded=st.download_button(
                    "⬇ Download TXT",
                    data=file,
                    file_name=selected_txt.name,
                    mime="text/plain",
                    use_container_width=True,
                )
                if downloaded:
                    st.success(f"✅ Successfully downloaded: {selected_txt.name}")

        else:

            st.info("No TXT files found.")

