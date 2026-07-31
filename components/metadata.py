import streamlit as st


def show_metadata(metadata):

    st.subheader("📊 Video Metadata")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Resolution",
            metadata["resolution"]
        )

        st.metric(
            "FPS",
            metadata["fps"]
        )

        st.metric(
            "Duration",
            f'{metadata["duration"]:.2f} sec'
        )

    with col2:

        st.metric(
            "Frames",
            metadata["frames"]
        )

        st.metric(
            "Codec",
            metadata["codec"]
        )

        st.metric(
            "File Size",
            f'{metadata["file_size_mb"]} MB'
        )