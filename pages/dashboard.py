import streamlit as st
from pathlib import Path


def show_dashboard(provider_name, selected_model):

    st.header("📊 Dashboard")

    ########################################################################
    # Folder Statistics
    ########################################################################

    upload_folder = Path("uploads")
    audio_folder = Path("audio")
    transcript_folder = Path("transcripts")
    analysis_folder = Path("analysis")
    chat_folder = Path("chat_history")
    export_folder = Path("exports")

    videos = list(upload_folder.glob("*.*"))
    audio = list(audio_folder.glob("*.*"))
    transcripts = list(transcript_folder.glob("*.txt"))
    analysis = list(analysis_folder.glob("*.md"))
    chats = list(chat_folder.glob("*.json"))
    exports = list(export_folder.glob("*.*"))

    ########################################################################
    # Total Storage
    ########################################################################

    folders = [
        upload_folder,
        audio_folder,
        transcript_folder,
        analysis_folder,
        chat_folder,
        export_folder,
    ]

    total_size = 0

    for folder in folders:

        if folder.exists():

            for file in folder.glob("*.*"):
                total_size += file.stat().st_size

    total_size_mb = total_size / (1024 * 1024)

    st.subheader("📊 Project Statistics")

    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

    with row1_col1:
        st.metric("📹 Videos", len(videos))

    with row1_col2:
        st.metric("🎵 Audio", len(audio))

    with row1_col3:
        st.metric("📝 Transcripts", len(transcripts))

    with row1_col4:
        st.metric("🤖 Analysis", len(analysis))

    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)

    with row2_col1:
        st.metric("💬 Chats", len(chats))

    with row2_col2:
        st.metric("📤 Exports", len(exports))

    with row2_col3:
        st.metric("💾 Storage", f"{total_size_mb:.2f} MB")

    with row2_col4:
        st.metric("🧠 Model", selected_model)


    st.divider()
    st.divider()

    col1, col2 = st.columns(2)



    ####################################################################
    # Videos
    ####################################################################

    with col1:

        st.subheader("📹 Videos")

        videos = sorted(
            Path("uploads").glob("*.*"),
            reverse=True
        )[:5]

        if videos:

            for file in videos:
                st.write(file.name+"\n")

        else:
            st.caption("No videos")

    ####################################################################
    # Audio
    ####################################################################

    with col2:

        st.subheader("🎵 Audio")

        audios = sorted(
            Path("audio").glob("*.*"),
            reverse=True
        )[:5]

        if audios:

            for file in audios:
                st.write(file.name+"\n")

        else:
            st.caption("No audio")

    st.divider()

    col3, col4 = st.columns(2)


    ####################################################################
    # Transcript
    ####################################################################

    with col3:

        st.subheader("📝 Transcript")

        transcripts = sorted(
            Path("transcripts").glob("*.txt"),
            reverse=True
        )[:5]

        if transcripts:

            for file in transcripts:
                st.write(file.name+"\n")

        else:
            st.caption("No transcripts")

    st.divider()
    col5, col6 = st.columns(2)

    ####################################################################
    # Analysis
    ####################################################################

    with col4:

        st.subheader("🤖 Analysis")

        analysis = sorted(
            Path("analysis").glob("*.md"),
            reverse=True
        )[:5]

        if analysis:

            for file in analysis:
                st.write(file.name+"\n")

        else:
            st.caption("No analysis")

    ####################################################################
    # Chats
    ####################################################################

    with col5:

        st.subheader("💬 Chats")

        chats = sorted(
            Path("chat_history").glob("*.json"),
            reverse=True
        )[:5]

        if chats:

            for file in chats:
                st.write(file.name+"\n")


        else:
            st.caption("No chats")

    ####################################################################
    # Exports
    ####################################################################

    with col6:

        st.subheader("📤 Exports")

        exports = sorted(
            Path("exports").glob("*.*"),
            reverse=True
        )[:5]

        if exports:

            for file in exports:
                st.write(file.name+"\n")


        else:
            st.caption("No exports")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📜 Version History")

        version_history = [
            ("v1.0.0", "Production Release", "Complete AI Video Analyzer with all core features."),
            ("v0.9.0", "Release Candidate", "Completed testing, documentation, and bug fixes."),
            ("v0.8.0", "Export Module", "Added TXT, Markdown, HTML, and PDF export support."),
            ("v0.7.0", "AI Chat", "Implemented AI-powered chat with transcript context."),
            ("v0.6.0", "AI Analysis", "Added video summarization, key points, and action items."),
            ("v0.5.0", "Speech-to-Text", "Integrated OpenAI Whisper transcription."),
            ("v0.4.0", "Audio Processing", "Implemented video-to-audio extraction using FFmpeg."),
            ("v0.3.0", "Video Management", "Added video upload and file management."),
            ("v0.2.0", "Provider Support", "Integrated Ollama, OpenAI, and Anthropic providers."),
            ("v0.1.0", "Initial Release", "Project initialization and Streamlit dashboard.")
        ]

        for version, title, description in version_history:
            st.markdown(
                f"""
        **{version}** — **{title}**

        - {description}

        """
            )

    with col2:

        st.subheader("🚀 Project Progress")

        progress = 100

        st.progress(progress)

        st.write(f"Project Completion: **{progress}%**")

        roadmap = [
            "✅ General Setup",
            "✅ Provider Management",
            "✅ Video Upload & Management",
            "✅ Audio Processing",
            "✅ Speech-to-Text",
            "✅ AI Video Analysis",
            "✅ AI Chat",
            "✅ Export & Reports",
            "✅ Testing",
            "✅ Documentation"
        ]

        for item in roadmap:
            st.write(item)

    st.divider()

    st.subheader("⚙ Current AI Configuration")

    config_col1, config_col2 = st.columns(2)

    with config_col1:
        st.success(f"Provider: {provider_name}")

    with config_col2:
        st.success(f"Model: {selected_model}")

    st.divider()

    st.divider()

    st.subheader("📦 Application Information")

    app_col1, app_col2, app_col3 = st.columns(3)

    with app_col1:
        st.success("📌 Version\n\nv1.0.0")

    with app_col2:
        st.success("🚀 Status\n\nProduction Ready")

    with app_col3:
        st.success("📄 License\n\nMIT")

    st.divider()

    st.subheader("🖥️ System Information")

    sys_col1, sys_col2, sys_col3 = st.columns(3)

    with sys_col1:
        st.info("🐍 Python\n\n3.11+")

    with sys_col2:
        st.info("🌐 Framework\n\nStreamlit")

    with sys_col3:
        st.info("🎤 Speech Engine\n\nOpenAI Whisper")

    sys_col4, sys_col5, sys_col6 = st.columns(3)

    with sys_col4:
        st.info("🎵 Media Engine\n\nFFmpeg")

    with sys_col5:
        st.info(f"🤖 Provider\n\n{provider_name}")

    with sys_col6:
        st.info(f"🧠 Model\n\n{selected_model}")

    st.divider()

    st.subheader("📌 Quick Tips")

    st.markdown("""
    - 📹 Upload videos in **MP4, AVI, MOV, MKV, or WEBM** format.

    - 🎵 Extract audio before generating transcripts.

    - 🎤 Generate transcripts using **OpenAI Whisper**.

    - 🤖 Select the AI provider and model before AI analysis.

    - 📝 Review transcripts before generating AI insights.

    - 📊 Analyze videos to obtain summaries, key points, and action items.

    - 📤 Export reports in **TXT, Markdown, HTML, or PDF** format.

    - ⚡ Larger videos may require additional processing time.

    - 🛠️ Ensure FFmpeg and Whisper are installed correctly.

    - 💾 Regularly back up transcripts and exported reports.
    """)

    st.divider()

    st.markdown("---")

    st.caption("🎥 AI Video Analyzer • Version **1.0.0**")

    st.caption("👨‍💻 Developed by **Nekkanti Satya Srinath**")

    st.caption("© 2026 • Powered by Python, Streamlit, Whisper, FFmpeg & Multiple AI Providers")