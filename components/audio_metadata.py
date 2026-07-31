import streamlit as st


def show_audio_metadata(metadata):

    st.subheader("🎵 Audio Metadata")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Duration",
            f"{metadata['duration']} sec"
        )

        st.metric(
            "Bitrate",
            f"{metadata['bitrate']} kbps"
        )

        st.metric(
            "Channels",
            metadata["channels"]
        )

    with col2:

        st.metric(
            "Sample Rate",
            f"{metadata['sample_rate']} Hz"
        )

        st.metric(
            "Size",
            f"{metadata['size_mb']} MB"
        )

        st.metric(
            "Filename",
            metadata["filename"]
        )