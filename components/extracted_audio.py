import os
import streamlit as st

from services.audio_service import AudioService
from utils.audio_metadata import AudioMetadata
from components.audio_metadata import show_audio_metadata


def show_extracted_audio():

    st.subheader("🎵 Extracted Audio")

    audio_files = AudioService.list_audio()

    if not audio_files:

        st.info("No extracted audio found.")

        return

    for audio in audio_files:

        filepath = os.path.join(
            "audio",
            audio
        )

        with st.container(border=True):

            st.markdown(f"### 🎵 {audio}")

            st.audio(filepath)

            metadata = AudioMetadata.get_metadata(
                filepath
            )

            if metadata:

                show_audio_metadata(metadata)

            col1, col2 = st.columns(2)

            with col1:

                with open(filepath, "rb") as f:

                    st.download_button(
                        "⬇ Download Audio",
                        data=f,
                        file_name=audio,
                        mime="audio/mpeg",
                        use_container_width=True,
                        key=f"download_{audio}"
                    )

            with col2:

                if st.button(
                    "🗑 Delete Audio",
                    key=f"delete_{audio}",
                    use_container_width=True
                ):

                    AudioService.delete_audio(audio)

                    st.success(
                        "Audio deleted successfully."
                    )

                    st.rerun()