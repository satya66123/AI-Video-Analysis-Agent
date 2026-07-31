import streamlit as st


def show_transcript_metadata(metadata):

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Words",
        metadata["Words"]
    )

    col2.metric(
        "Characters",
        metadata["Characters"]
    )

    col3.metric(
        "Lines",
        metadata["Lines"]
    )

    col4, col5 = st.columns(2)

    col4.metric(
        "Reading Time",
        metadata["Reading Time"]
    )

    col5.metric(
        "File Size",
        metadata["Size"]
    )