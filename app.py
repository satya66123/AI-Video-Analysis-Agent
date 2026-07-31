import streamlit as st

from components.show_ai_analysis import show_ai_analysis
from components.sidebar import show_sidebar

from pages.dashboard import show_dashboard
from pages.video_upload import show_video_upload
from pages.audio_processing import show_audio_processing
from pages.speech_to_text import show_speech_to_text
from pages.ai_chat import show_ai_chat
from pages.reports import show_reports
from pages.about import show_about


st.set_page_config(
    page_title="AI Video Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# Sidebar
page, provider_name, selected_model = show_sidebar()

# Main Title
st.title("🎬 AI Video Analyzer")

# Navigation
if page == "Dashboard":

    show_dashboard(
        provider_name,
        selected_model
    )

elif page == "Video Upload":

    show_video_upload()

elif page == "Audio Processing":

    show_audio_processing()

elif page == "Speech-to-Text":

    show_speech_to_text()

elif page == "AI Analysis":

    show_ai_analysis()

elif page == "AI Chat":

    show_ai_chat()

elif page == "Reports":

    show_reports()

elif page == "About":

    show_about()