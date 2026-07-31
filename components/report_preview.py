from __future__ import annotations

import json

import streamlit as st

from components.export_center import show_export_center
from services.report_service import ReportService

from pathlib import Path
from services.metadata_service import MetadataService
from services.export_service import ExportService



def show_report_preview() -> None:
    """
    Summary Report Dashboard
    """

    st.subheader("📊 Summary Report")

    st.caption(
        "Preview and generate a professional report from the processed video."
    )

    (
        video_tab,
        audio_tab,
        transcript_tab,
        analysis_tab,
        chat_tab,
        metadata_tab,
        final_tab,
        export_center_tab,
    ) = st.tabs(
        [
            "📹 Video",
            "🎵 Audio",
            "📝 Transcript",
            "🤖 AI Analysis",
            "💬 AI Chat",
            "⚙ Metadata",
            "📄 Final Report",
            "📦 Export Center",
        ]
    )

    ####################################################################
    # VIDEO
    ####################################################################

    with video_tab:

        st.subheader("📹 Video Information")


        upload_folder = Path("uploads")
        upload_folder.mkdir(exist_ok=True)

        video_files = sorted(upload_folder.glob("*.*"))

        if not video_files:

            st.warning("No videos found in uploads folder.")

        else:

            selected_video = st.selectbox(
                "Select Video",
                video_files,
                format_func=lambda x: x.name,
                key="report_video_select",
            )

            video_metadata = MetadataService.get_video_metadata(
                str(selected_video)
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**Filename :** {video_metadata['filename']}")
                st.write(f"**Duration :** {video_metadata['duration']}")
                st.write(f"**Resolution :** {video_metadata['resolution']}")

            with col2:

                st.write(f"**FPS :** {video_metadata['fps']}")
                st.write(f"**Format :** {video_metadata['format']}")
                st.write(f"**Size :** {video_metadata['size']}")

            # Store for Final Report
            st.session_state["report_video_metadata"] = video_metadata

    ####################################################################
    # AUDIO
    ####################################################################

    with audio_tab:

        st.subheader("🎵 Audio Information")

        audio_folder = Path("audio")
        audio_folder.mkdir(exist_ok=True)

        audio_files = sorted(audio_folder.glob("*.*"))

        if not audio_files:

            st.warning("No audio files found.")

        else:

            selected_audio = st.selectbox(
                "Select Audio",
                audio_files,
                format_func=lambda x: x.name,
                key="report_audio_select",
            )

            audio_metadata = MetadataService.get_audio_metadata(
                str(selected_audio)
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**Filename :** {selected_audio.name}")
                st.write(f"**Duration :** {audio_metadata['duration']}")
                st.write(f"**Channels :** {audio_metadata['channels']}")

            with col2:

                st.write(f"**Sample Rate :** {audio_metadata['sample_rate']}")
                st.write(f"**Format :** {selected_audio.suffix}")

                size = selected_audio.stat().st_size / (1024 * 1024)

                st.write(f"**Size :** {size:.2f} MB")

            # Store metadata for Final Report
            st.session_state["report_audio_metadata"] = audio_metadata
            st.session_state["report_audio_file"] = selected_audio.name

    ####################################################################
    # TRANSCRIPT
    ####################################################################

    with transcript_tab:

        st.subheader("📝 Transcript")

        transcript_folder = Path("transcripts")
        transcript_folder.mkdir(exist_ok=True)

        transcript_files = sorted(transcript_folder.glob("*.txt"))

        if not transcript_files:

            st.warning("No transcript files found.")

        else:

            selected_transcript = st.selectbox(
                "Select Transcript",
                transcript_files,
                format_func=lambda x: x.name,
                key="report_transcript_select",
            )

            transcript_text = selected_transcript.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            st.text_area(
                "Transcript",
                transcript_text,
                height=400,
                key="report_transcript_view",
            )

            st.session_state["report_transcript"] = transcript_text
            st.session_state["report_transcript_file"] = selected_transcript.name

    ####################################################################
    # AI ANALYSIS
    ####################################################################

    with analysis_tab:

        st.subheader("🤖 AI Analysis")

        analysis_folder = Path("analysis")
        analysis_folder.mkdir(exist_ok=True)

        analysis_files = sorted(analysis_folder.glob("*.md"))

        if not analysis_files:

            st.warning("No analysis reports found.")

        else:

            selected_analysis = st.selectbox(
                "Select Analysis Report",
                analysis_files,
                format_func=lambda x: x.name,
                key="report_analysis_select",
            )

            analysis_text = selected_analysis.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            st.markdown(analysis_text)

            st.session_state["report_analysis"] = analysis_text
            st.session_state["report_analysis_file"] = selected_analysis.name


    ####################################################################
    # AI CHAT
    ####################################################################

    with chat_tab:

        st.subheader("💬 AI Chat")


        chat_folder = Path("chat_history")
        chat_folder.mkdir(exist_ok=True)

        chat_files = sorted(chat_folder.glob("*.json"))

        if not chat_files:

            st.warning("No chat history found.")

        else:

            selected_chat = st.selectbox(
                "Select Chat History",
                chat_files,
                format_func=lambda x: x.name,
                key="report_chat_select",
            )

            with open(selected_chat, "r", encoding="utf-8") as f:
                chat_data = json.load(f)

            st.json(chat_data)

            st.session_state["report_chat"] = chat_data
            st.session_state["report_chat_file"] = selected_chat.name

    ####################################################################
    # METADATA
    ####################################################################

    with metadata_tab:

        st.subheader("⚙ Report Metadata")

        provider = st.session_state.get("provider", "N/A")
        model = st.session_state.get("model", "N/A")

        col1, col2 = st.columns(2)

        with col1:

            st.text_input(
                "Provider",
                provider,
                disabled=True,
                key="rp_provider",
            )

        with col2:

            st.text_input(
                "Model",
                model,
                disabled=True,
                key="rp_model",
            )



    ####################################################################
    # FINAL REPORT
    ####################################################################

    with final_tab:

        st.subheader("📄 Final Report")

        st.markdown("### Include")

        include_video = st.checkbox(
            "Video Metadata",
            value=True,
            key="rp_include_video",
        )

        include_audio = st.checkbox(
            "Audio Metadata",
            value=True,
            key="rp_include_audio",
        )

        include_transcript = st.checkbox(
            "Transcript",
            value=True,
            key="rp_include_transcript",
        )

        include_chat = st.checkbox(
            "Chat History",
            value=True,
            key="rp_include_chat",
        )

        include_metadata = st.checkbox(
            "Processing Metadata",
            value=True,
            key="rp_include_metadata",
        )

        st.divider()



        ################################################################
        # Generate
        ################################################################



        if st.button(
                "📄 Generate",
                use_container_width=True,
                type="primary",
                key="rp_generate",
            ):
                video = st.session_state.get("report_video_metadata", {})
                audio = st.session_state.get("report_audio_metadata", {})

                filename = ExportService.generate_filename(
                    video.get("filename", "video")
                )

                st.session_state["export_filename"] = filename

                report = ReportService.generate_complete_report(
                    include_video,
                    include_audio,
                    include_transcript,
                    True,
                    include_chat,
                    include_metadata,
                    {
                        "video_name": video.get("filename", ""),
                        "video_duration": video.get("duration", ""),
                        "video_resolution": video.get("resolution", ""),
                        "video_fps": video.get("fps", ""),
                        "video_format": video.get("format", ""),
                        "video_size": video.get("size", ""),

                        "audio_name": audio.get("filename", ""),
                        "audio_duration": audio.get("duration", ""),
                        "channels": audio.get("channels", ""),
                        "sample_rate": audio.get("sample_rate", ""),
                        "audio_format": audio.get("format", ""),
                        "audio_size": audio.get("size", ""),

                        "transcript": st.session_state.get("report_transcript", ""),
                        "analysis": st.session_state.get("report_analysis", ""),
                        "chat": st.session_state.get("report_chat", ""),

                        "provider": st.session_state.get("provider", ""),
                        "model": st.session_state.get("model", ""),
                    },
                )

                st.session_state["generated_report"] = report

                st.success("✅ Report generated successfully!")

                ################################################################
                # Preview Generated Report
                ################################################################

                if "generated_report" in st.session_state:

                    st.divider()

                    st.subheader("📖 Generated Report Preview")

                    st.markdown(
                        st.session_state["generated_report"]
                    )

                    st.divider()

                    ################################################################
                    # PDF
                    ################################################################

                    col2, col3, col4 = st.columns(3)

                    with col2:

                        if st.button(
                                "⬇ PDF",
                                use_container_width=True,
                                key="rp_pdf",
                        ):

                            if "generated_report" not in st.session_state:
                                st.warning("Generate report first.")

                            else:

                                pdf = ExportService.save_pdf(
                                    st.session_state["export_filename"],
                                    st.session_state["generated_report"],
                                )

                                st.success(f"✅ PDF saved successfully!")

                                st.code(str(pdf))

                    ################################################################
                    # Markdown
                    ################################################################

                    with col3:

                        if st.button(
                                "📝 Markdown",
                                use_container_width=True,
                                key="rp_markdown",
                        ):

                            if "generated_report" not in st.session_state:
                                st.warning("Generate report first.")

                            else:

                                md = ExportService.save_md(
                                    st.session_state["export_filename"],
                                    st.session_state["generated_report"],
                                )

                                st.success("✅ Markdown saved successfully!")

                                st.code(str(md))

                    ################################################################
                    # HTML
                    ################################################################

                    with col4:

                        if st.button(
                                "🌐 HTML",
                                use_container_width=True,
                                key="rp_html",
                        ):

                            if "generated_report" not in st.session_state:
                                st.warning("Generate report first.")

                            else:

                                html = ExportService.save_html(
                                    st.session_state["export_filename"],
                                    st.session_state["generated_report"],
                                )

                                st.success("✅ HTML saved successfully!")

                                st.code(str(html))

                    ################################################################
                    # TXT
                    ################################################################

                    if st.button(
                            "📃 TXT",
                            use_container_width=True,
                            key="rp_txt",
                    ):

                        if "generated_report" not in st.session_state:
                            st.warning("Generate report first.")

                        else:

                            txt = ExportService.save_txt(
                                st.session_state["export_filename"],
                                st.session_state["generated_report"],
                            )

                            st.success("✅ TXT saved successfully!")

                            st.code(str(txt))

    ####################################################################
    # EXPORT CENTER
    ####################################################################

    with export_center_tab:
        show_export_center()