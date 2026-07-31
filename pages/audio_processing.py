import os
import streamlit as st

from services.video_service import VideoService
from services.audio_service import AudioService

from components.extracted_audio import show_extracted_audio


def show_audio_processing():

    st.title("🎵 Audio Processing")

    videos = VideoService.list_videos()

    if not videos:

        st.info("No uploaded videos found.")
        return

    selected_video = st.selectbox(
        "Select Video",
        videos
    )

    video_path = os.path.join(
        "uploads",
        selected_video
    )

    st.video(video_path)

    if st.button(
        "🎵 Extract Audio",
        type="primary",
        use_container_width=True
    ):

        progress = st.progress(0)

        status = st.empty()

        audio_path = AudioService.extract_audio(
            video_path,
            progress,
            status
        )

        if audio_path:
            st.audio(audio_path)

    st.divider()

    show_extracted_audio()