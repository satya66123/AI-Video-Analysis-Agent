import streamlit as st


def show_about():

    st.header("ℹ️ About AI Video Analyzer")

    st.write("""
AI Video Analyzer is an AI-powered application that helps users upload,
process, analyze, and interact with video content using multiple Large
Language Models (LLMs).

The application supports local and cloud AI providers for intelligent
video understanding, transcription, summarization, and conversational
analysis.
""")

    st.divider()

    st.subheader("🎯 Features")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
- 📤 Video Upload
- 🎵 Audio Extraction
- 📝 Speech-to-Text
- 🤖 AI Video Analysis
- 💬 AI Chat with Video
""")

    with col2:

        st.markdown("""
- 📄 Export Reports
- 📊 Video Metadata
- ⚡ Multi AI Providers
- 🔒 Local Processing Support
- 🎯 User-Friendly Interface
""")

    st.divider()

    st.subheader("🧠 Supported AI Providers")

    st.markdown("""
- 🦙 Ollama (Local)
- 🤖 OpenAI
- 🧠 Anthropic Claude
""")

    st.divider()

    st.subheader("🛠 Technology Stack")

    st.markdown("""
- Python
- Streamlit
- OpenCV
- MoviePy
- FFmpeg
- Whisper
- Ollama
- OpenAI API
- Anthropic API
""")

    st.divider()

    st.subheader("🚀 Project Roadmap")

    roadmap = [
        ("✅", "General Setup"),
        ("✅", "Provider Management"),
        ("✅", "Video Upload & Management"),
        ("⬜", "Audio Processing"),
        ("⬜", "Speech-to-Text"),
        ("⬜", "AI Video Analysis"),
        ("⬜", "AI Chat"),
        ("⬜", "Export & Reports"),
        ("⬜", "Testing"),
        ("⬜", "Documentation & Release"),
    ]

    for status, phase in roadmap:
        st.write(f"{status} {phase}")

    st.divider()

    st.subheader("📌 Version Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Version", "v1.0.0")

    with col2:
        st.metric("Status", "Development")

    st.divider()

    st.caption("© 2026 AI Video Analyzer | Built with ❤️ using Python & Streamlit")