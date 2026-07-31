import os
import streamlit as st

from services.audio_service import AudioService
from services.speech_service import SpeechService
from components.transcript import show_transcripts
from components.transcript_stats import show_transcript_stats
from components.transcript_dashboard import show_transcript_dashboard
from components.export_transcripts import show_export_transcripts
from utils.transcript_utils import TranscriptUtils


def show_speech_to_text():

    st.title("🎤 Speech To Text")

    model_name = st.selectbox(
        "Whisper Model",
        [
            "tiny",
            "base",
            "small",
            "medium",
            "large"
        ],
        index=1
    )

    audio_files = AudioService.list_audio()
    transcripts = TranscriptUtils.list_transcripts()

    total_words = 0

    for transcript in transcripts:
        text = TranscriptUtils.read_transcript(transcript)

        total_words += len(text.split())

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🎵 Audio Files",
        len(audio_files)
    )

    col2.metric(
        "📄 Transcripts",
        len(transcripts)
    )

    col3.metric(
        "📝 Total Words",
        total_words
    )

    st.divider()

    show_transcript_dashboard()

    st.divider()

    audio_files = AudioService.list_audio()

    if not audio_files:

        st.info("No extracted audio found.")
        return

    selected_audio = st.selectbox(
        "Select Audio",
        audio_files
    )

    audio_path = os.path.join(
        "audio",
        selected_audio
    )

    if audio_path and os.path.exists(audio_path):
        st.audio(audio_path)

    if st.button(
        "📝 Transcribe",
        type="primary",
        use_container_width=True
    ):

        progress = st.progress(0)

        status = st.empty()

        transcript = SpeechService.transcribe(
            audio_path,
            progress,
            status,
            model_name
        )

        if transcript:

            st.success("Transcript generated.")

            st.text_area(
                "Transcript",
                transcript,
                height=300
            )


    st.divider()

    show_transcript_stats()

    st.divider()

    show_export_transcripts()

    st.divider()

    show_transcripts()