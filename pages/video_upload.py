import streamlit as st

from components.uploader import show_uploader
from components.uploaded_videos import show_uploaded_videos


def show_video_upload():

    st.header("📤 Video Upload")

    st.write(
        "Upload videos, preview them, and manage your video library."
    )

    st.divider()

    show_uploader()

    st.divider()

    show_uploaded_videos()