import os
import streamlit as st

from services.video_service import VideoService


def show_dashboard_cards():

    videos = VideoService.list_videos()

    total_size = 0

    for video in videos:

        path = os.path.join(
            VideoService.UPLOAD_FOLDER,
            video
        )

        total_size += os.path.getsize(path)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Videos",
            len(videos)
        )

    with col2:

        st.metric(
            "Storage",
            f"{total_size/(1024*1024):.2f} MB"
        )

    with col3:

        st.metric(
            "Providers",
            3
        )