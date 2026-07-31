import streamlit as st

from services.video_service import VideoService
from utils.file_validator import FileValidator
from utils.video_metadata import VideoMetadata

from components.metadata import show_metadata


def show_uploader():

    uploaded_video = st.file_uploader(
        "Upload Video",
        type=[
            "mp4",
            "avi",
            "mov",
            "mkv",
            "webm"
        ],
        key="video_uploader"
    )

    if uploaded_video is None:
        return

    st.info(f"Selected File: {uploaded_video.name}")

    if st.button(
        "📤 Upload Video",
        type="primary",
        use_container_width=True
    ):

        valid, message = FileValidator.validate(
            uploaded_video
        )

        if not valid:
            st.error(message)
            return



        if VideoService.is_duplicate(uploaded_video):
            st.warning(
                "⚠ This video already exists."
            )

            return

        progress_bar = st.progress(0)

        status_text = st.empty()

        filepath = VideoService.save_video(
            uploaded_video,
            progress_bar,
            status_text
        )

        progress_bar.progress(100)

        st.success("✅ Video Uploaded Successfully")

        st.video(filepath)

        metadata = VideoMetadata.get_metadata(
            filepath
        )

        if metadata:
            show_metadata(metadata)

        st.rerun()