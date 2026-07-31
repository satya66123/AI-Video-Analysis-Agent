import os
import streamlit as st

from utils.transcript_utils import TranscriptUtils
from utils.transcript_metadata import TranscriptMetadata
from components.transcript_metadata import show_transcript_metadata
from utils.transcript_validator import TranscriptValidator


def show_transcripts():

    transcripts = TranscriptUtils.list_transcripts()

    # Step 29 - Sorting
    sort_option = st.selectbox(
        "Sort By",
        [
            "Newest",
            "Oldest",
            "A-Z",
            "Z-A"
        ]
    )

    if sort_option == "Oldest":

        transcripts.reverse()

    elif sort_option == "A-Z":

        transcripts = sorted(transcripts)

    elif sort_option == "Z-A":

        transcripts = sorted(
            transcripts,
            reverse=True
        )

    # Step 30 - Filter
    filter_text = st.text_input(
        "🔍 Filter Transcripts"
    )

    if filter_text:

        transcripts = [

            t for t in transcripts

            if filter_text.lower() in t.lower()

        ]

    if not transcripts:

        st.info(
            "📄 No transcripts found.\n\nGenerate a transcript first."
        )
        return

    st.subheader("📄 Saved Transcripts")

    st.caption(
        f"{len(transcripts)} transcript(s) available"
    )

    for transcript in transcripts:

        with st.container(border=True):

            st.markdown(
                f"### 📄 {transcript.replace('.txt','')}"
            )

            # Rename
            new_name = st.text_input(
                "Rename Transcript",
                value=transcript.replace(".txt", ""),
                key=f"rename_{transcript}"
            )

            if st.button(
                "✏ Rename",
                key=f"rename_btn_{transcript}",
                use_container_width=True
            ):

                success = TranscriptUtils.rename_transcript(
                    transcript,
                    new_name
                )

                if success:

                    st.success(
                        "Transcript renamed."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Transcript already exists."
                    )

            path = os.path.join(
                "transcripts",
                transcript
            )

            if not TranscriptValidator.validate(path):
                st.error(
                    "Transcript is corrupted."
                )

                continue

            text = TranscriptUtils.read_transcript(
                transcript
            )

            # Preview
            preview = text[:250]

            if len(text) > 250:
                preview += "..."

            st.caption(preview)

            metadata = TranscriptMetadata.get_metadata(
                os.path.join(
                    "transcripts",
                    transcript
                )
            )

            show_transcript_metadata(metadata)

            # Step 31 - Created Date
            st.caption(
                f"📅 Created : {metadata['Created']}"
            )

            st.info(
                f"""
📄 File : {transcript}

📝 Words : {metadata['Words']}

🔤 Characters : {metadata['Characters']}

⏱ Reading Time : {metadata['Reading Time']}
"""
            )

            # Step 32 - Transcript Length Badge
            words = len(text.split())

            if words < 200:

                st.success(
                    "🟢 Short Transcript"
                )

            elif words < 1000:

                st.info(
                    "🟡 Medium Transcript"
                )

            else:

                st.warning(
                    "🔴 Long Transcript"
                )

            # Search
            search = st.text_input(
                "Search Transcript",
                key=f"search_{transcript}"
            )

            if search:

                filtered = "\n".join(

                    line

                    for line in text.splitlines()

                    if search.lower() in line.lower()

                )

            else:

                filtered = text

            with st.expander(
                "View Transcript"
            ):

                st.text_area(
                    "Transcript",
                    filtered,
                    height=250,
                    disabled=True,
                    key=transcript
                )

                st.code(
                    filtered,
                    language="text"
                )

            col1, col2 = st.columns(2)

            with col1:

                st.download_button(
                    label="⬇ Download Transcript",
                    data=text,
                    file_name=transcript,
                    mime="text/plain",
                    use_container_width=True
                )

            with col2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{transcript}",
                    use_container_width=True
                ):

                    TranscriptUtils.delete_transcript(
                        transcript
                    )

                    st.success(
                        "Transcript deleted."
                    )

                    st.rerun()