import os
import time
import streamlit as st


class AnalysisHistory:

    ANALYSIS_FOLDER = "analysis"

    @classmethod
    def get_files(cls):

        os.makedirs(
            cls.ANALYSIS_FOLDER,
            exist_ok=True
        )

        files = [
            f for f in os.listdir(cls.ANALYSIS_FOLDER)
            if f.endswith(".md")
        ]

        files.sort(
            key=lambda f: os.path.getmtime(
                os.path.join(
                    cls.ANALYSIS_FOLDER,
                    f
                )
            ),
            reverse=True
        )

        return files

    @classmethod
    def render(cls):

        st.subheader("📁 Analysis History")

        files = cls.get_files()

        if not files:

            st.info("No analyses found.")

            return

        search = st.text_input(
            "🔍 Search",
            placeholder="Search analysis..."
        )

        if search:

            files = [
                f for f in files
                if search.lower() in f.lower()
            ]

        for file in files:

            filepath = os.path.join(
                cls.ANALYSIS_FOLDER,
                file
            )

            modified = time.strftime(
                "%Y-%m-%d %H:%M",
                time.localtime(
                    os.path.getmtime(filepath)
                )
            )

            with st.expander(file):

                st.caption(
                    f"Last Modified : {modified}"
                )

                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as f:

                    content = f.read()

                st.markdown(content)

                col1, col2 = st.columns(2)

                with col1:

                    st.download_button(
                        "⬇ Download",
                        data=content,
                        file_name=file,
                        mime="text/markdown",
                        key=f"download_{file}"
                    )

                with col2:

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{file}"
                    ):

                        os.remove(filepath)

                        st.success(
                            "Analysis Deleted"
                        )

                        st.rerun()