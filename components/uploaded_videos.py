import os
import streamlit as st

from services.video_service import VideoService
from utils.video_metadata import VideoMetadata


def show_uploaded_videos():

    st.divider()

    st.header("📁 Uploaded Videos")

    videos = VideoService.list_videos()

    if not videos:

        st.info("No uploaded videos.")

        return

    for video in videos:

        filepath = os.path.join(
            VideoService.UPLOAD_FOLDER,
            video
        )

        metadata = VideoMetadata.get_metadata(filepath)

        with st.expander(video):

            st.video(filepath)

            if metadata:

                st.json(metadata)

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{video}"
                ):

                    VideoService.delete_video(video)

                    st.rerun()

            with col2:

                st.download_button(
                    "⬇ Download",
                    data=open(filepath, "rb"),
                    file_name=video
                )