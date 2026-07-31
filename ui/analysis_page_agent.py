"""
analysis_page_agent.py

Analysis Page Agent
"""

from __future__ import annotations

import streamlit as st

from services.ai_analysis_agent_service  import AIAnalysisService

from .header_agent import HeaderAgent
from .footer_agent import FooterAgent


class AnalysisPageAgent:

    def render(self):

        HeaderAgent.render("🧠 AI Analysis")

        files = AIAnalysisService.list_analysis()

        if not files:

            st.info(
                "No analysis files found."
            )

            FooterAgent.render()

            return

        st.success(
            f"{len(files)} analysis file(s) found."
        )

        for file in files:

            with st.expander(
                f"📄 {file['name']}",
                expanded=False,
            ):

                st.caption(
                    f"Size: {file['size']:,} bytes"
                )

                content = AIAnalysisService.load_analysis(
                    file["name"]
                )

                st.markdown(content)

                col1, col2 = st.columns(2)

                with col1:

                    st.download_button(
                        label="📥 Download",
                        data=content,
                        file_name=file["name"],
                        mime="text/markdown",
                        key=f"download_{file['name']}",
                        use_container_width=True,
                    )

                with col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{file['name']}",
                        use_container_width=True,
                    ):

                        AIAnalysisService.delete_analysis(
                            file["name"]
                        )

                        st.success(
                            "Analysis deleted successfully."
                        )

                        st.rerun()

        FooterAgent.render()