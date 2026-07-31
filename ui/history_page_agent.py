"""
history_page_agent.py

History Page Agent
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from services.video_agent_service import VideoService
from services.audio_agent_service import AudioService
from services.speech_agent_service import SpeechService
from services.ai_analysis_agent_service import AIAnalysisService
from services.ai_chat_agent_service import AIChatService
from services.report_agent_service import ReportService
from services.export_agent_service import ExportService

from .header_agent import HeaderAgent
from .footer_agent import FooterAgent


class HistoryPageAgent:

    ICONS = {

        "video": "🎥",

        "audio": "🎵",

        "transcript": "📝",

        "analysis": "🧠",

        "chat": "💬",

        "report": "📑",

        "export": "📤",

    }

    def render(self):

        HeaderAgent.render(
            "📚 Project History"
        )

        #######################################################
        # Load Saved Files
        #######################################################

        videos = VideoService.list_videos()

        audios = AudioService.list_audio()

        transcripts = SpeechService.list_transcripts()

        analyses = AIAnalysisService.list_analysis()

        chats = AIChatService.list_chats()

        reports = ReportService.list_reports()

        exports = ExportService.list_history_exports()

        #######################################################
        # Statistics
        #######################################################

        st.subheader(
            "📊 Project Statistics"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Videos",
                len(videos),
            )

        with c2:

            st.metric(
                "Audio",
                len(audios),
            )

        with c3:

            st.metric(
                "Transcripts",
                len(transcripts),
            )

        with c4:

            st.metric(
                "Analysis",
                len(analyses),
            )

        c5, c6, c7 = st.columns(3)

        with c5:

            st.metric(
                "Chats",
                len(chats),
            )

        with c6:

            st.metric(
                "Reports",
                len(reports),
            )

        with c7:

            st.metric(
                "Exports",
                len(exports),
            )

        st.divider()

        #######################################################
        # Navigation
        #######################################################

        history_section = st.radio(

            "Browse",

            [

                "Videos",

                "Audio",

                "Transcripts",

                "Analysis",

                "Chats",

                "Reports",

                "Exports",

            ],

            horizontal=True,

        )

        st.divider()

        #######################################################
        # Videos
        #######################################################

        if history_section == "Videos":

            st.subheader(
                "🎥 Uploaded Videos"
            )

            search = st.text_input(

                "Search Videos",

                placeholder="Search video...",

            )

            filtered = []

            for video in videos:

                if (
                    not search
                    or search.lower()
                    in video.lower()
                ):

                    filtered.append(video)

            st.success(
                f"{len(filtered)} video(s) found."
            )

            if not filtered:

                st.info(
                    "No videos available."
                )

            else:

                for video in filtered:

                    with st.expander(
                        f"🎥 {video}",
                        expanded=False,
                    ):

                        ##################################################
                        # Metadata
                        ##################################################

                        try:

                            metadata = VideoService.load_metadata(
                                video
                            )

                        except Exception:

                            metadata = None

                        if metadata:

                            c1, c2 = st.columns(2)

                            with c1:

                                st.write(
                                    f"**Filename:** {metadata.get('filename','N/A')}"
                                )

                                st.write(
                                    f"**Duration:** {metadata.get('duration','N/A')}"
                                )

                                st.write(
                                    f"**Resolution:** {metadata.get('resolution','N/A')}"
                                )

                            with c2:

                                st.write(
                                    f"**FPS:** {metadata.get('fps','N/A')}"
                                )

                                st.write(
                                    f"**Format:** {metadata.get('format','N/A')}"
                                )

                                st.write(
                                    f"**Size:** {metadata.get('size','N/A')}"
                                )

                        else:

                            st.warning(
                                "Metadata not available."
                            )

                    ##################################################
                     # Actions
                    ##################################################

                    col1, col2 = st.columns(2)

                    with col1:

                            video_path = Path(
                                VideoService.UPLOAD_FOLDER
                            ) / video

                            with open(
                                video_path,
                                "rb",
                            ) as file:

                                st.download_button(

                                    "📥 Download",

                                    data=file.read(),

                                    file_name=video,

                                    mime="video/mp4",

                                    key=f"video_download_{video}",

                                    use_container_width=True,

                                )

                    with col2:

                            if st.button(

                                "🗑 Delete",

                                key=f"video_delete_{video}",

                                use_container_width=True,

                            ):

                                VideoService.delete_video(
                                    video
                                )

                                try:

                                    VideoService.delete_metadata(
                                        video
                                    )

                                except Exception:

                                    pass

                                st.success(
                                    "Video deleted."
                                )

                                st.rerun()



        #######################################################
        # Audio
        #######################################################

        elif history_section == "Audio":



                st.subheader(
                    "🎵 Extracted Audio"
                )

                search = st.text_input(

                    "Search Audio",

                    placeholder="Search audio...",

                    key="audio_search",

                )

                filtered = []

                for audio in audios:

                    if (
                            not search
                            or search.lower()
                            in audio.lower()
                    ):
                        filtered.append(audio)

                st.success(
                    f"{len(filtered)} audio file(s) found."
                )

                if not filtered:

                    st.info(
                        "No audio files available."
                    )

                else:

                    for audio in filtered:

                        with st.expander(
                                f"🎵 {audio}",
                                expanded=False,
                        ):

                            ##################################################
                            # Metadata
                            ##################################################

                            try:

                                metadata = AudioService.load_metadata(
                                    audio
                                )

                            except Exception:

                                metadata = None

                            if metadata:

                                col1, col2 = st.columns(2)

                                with col1:

                                    st.write(
                                        f"**Filename:** {metadata.get('filename', 'N/A')}"
                                    )

                                    st.write(
                                        f"**Duration:** {metadata.get('duration', 'N/A')}"
                                    )

                                    st.write(
                                        f"**Channels:** {metadata.get('channels', 'N/A')}"
                                    )

                                with col2:

                                    st.write(
                                        f"**Sample Rate:** {metadata.get('sample_rate', 'N/A')}"
                                    )

                                    st.write(
                                        f"**Format:** {metadata.get('format', 'N/A')}"
                                    )

                                    st.write(
                                        f"**Size:** {metadata.get('size', 'N/A')}"
                                    )

                            else:

                                st.warning(
                                    "Audio metadata not available."
                                )

                            ##################################################
                            # Audio Player
                            ##################################################

                            audio_path = (
                                    Path(
                                        AudioService.AUDIO_FOLDER
                                    )
                                    / audio
                            )

                            if audio_path.exists():
                                st.audio(
                                    str(audio_path)
                                )

                            ##################################################
                            # Actions
                            ##################################################

                            col1, col2 = st.columns(2)

                            with col1:

                                with open(
                                        audio_path,
                                        "rb",
                                ) as file:
                                    st.download_button(

                                        "📥 Download",

                                        data=file.read(),

                                        file_name=audio,

                                        mime="audio/mpeg",

                                        key=f"audio_download_{audio}",

                                        use_container_width=True,

                                    )

                            with col2:

                                if st.button(

                                        "🗑 Delete",

                                        key=f"audio_delete_{audio}",

                                        use_container_width=True,

                                ):

                                    AudioService.delete_audio(
                                        audio
                                    )

                                    try:

                                        AudioService.delete_metadata(
                                            audio
                                        )

                                    except Exception:

                                        pass

                                    st.success(
                                        "Audio deleted successfully."
                                    )

                                    st.rerun()



        #######################################################
        # Transcripts
        #######################################################

        elif history_section == "Transcripts":



                    st.subheader(
                        "📝 Saved Transcripts"
                    )

                    search = st.text_input(

                        "Search Transcript",

                        placeholder="Search transcript...",

                        key="transcript_search",

                    )

                    filtered = []

                    for transcript in transcripts:

                        name = transcript["name"]

                        if (
                                not search
                                or search.lower() in name.lower()
                        ):
                            filtered.append(transcript)

                    st.success(
                        f"{len(filtered)} transcript(s) found."
                    )

                    if not filtered:

                        st.info(
                            "No transcripts available."
                        )

                    else:

                        for transcript in filtered:

                            filename = transcript["name"]

                            with st.expander(
                                    f"📝 {filename}",
                                    expanded=False,
                            ):

                                ##################################################
                                # Information
                                ##################################################

                                col1, col2 = st.columns(2)

                                with col1:

                                    st.write(
                                        f"**Size:** {transcript['size']:,} bytes"
                                    )

                                with col2:

                                    st.write(
                                        f"**Modified:** {transcript['modified']}"
                                    )

                                ##################################################
                                # Preview
                                ##################################################

                                content = SpeechService.load_transcript(
                                    filename
                                )

                                preview = content[:3000]

                                st.text_area(

                                    "Transcript Preview",

                                    value=preview,

                                    height=250,

                                    disabled=True,

                                    key=f"preview_{filename}",

                                )

                                ##################################################
                                # Statistics
                                ##################################################

                                words = len(
                                    content.split()
                                )

                                chars = len(
                                    content
                                )

                                c1, c2 = st.columns(2)

                                with c1:

                                    st.metric(
                                        "Words",
                                        words,
                                    )

                                with c2:

                                    st.metric(
                                        "Characters",
                                        chars,
                                    )

                                ##################################################
                                # Actions
                                ##################################################

                                col1, col2, col3, col4 = st.columns(4)

                                with col1:

                                    st.download_button(

                                        "📥 Download",

                                        data=content,

                                        file_name=filename,

                                        mime="text/plain",

                                        key=f"download_{filename}",

                                        use_container_width=True,

                                    )

                                with col2:

                                    if st.button(

                                            "💬 Use In Chat",

                                            key=f"chat_{filename}",

                                            use_container_width=True,

                                    ):
                                        st.session_state[
                                            "transcript"
                                        ] = content

                                        st.session_state[
                                            "current_page"
                                        ] = "AI Chat"

                                        st.success(
                                            "Transcript loaded for chat."
                                        )

                                with col3:

                                    if st.button(

                                            "📑 Generate Report",

                                            key=f"report_{filename}",

                                            use_container_width=True,

                                    ):
                                        st.session_state[
                                            "selected_transcript"
                                        ] = filename

                                        st.session_state[
                                            "current_page"
                                        ] = "Report"

                                        st.success(
                                            "Transcript selected for report generation."
                                        )

                                with col4:

                                    if st.button(

                                            "🗑 Delete",

                                            key=f"delete_{filename}",

                                            use_container_width=True,

                                    ):
                                        SpeechService.delete_transcript(
                                            filename
                                        )

                                        st.success(
                                            "Transcript deleted."
                                        )

                                        st.rerun()



        #######################################################
        # Analysis
        #######################################################

        elif history_section == "Analysis":


                        st.subheader(
                            "🧠 AI Analysis"
                        )

                        search = st.text_input(

                            "Search Analysis",

                            placeholder="Search analysis...",

                            key="analysis_search",

                        )

                        filtered = []

                        for analysis in analyses:

                            name = analysis["name"]

                            if (
                                    not search
                                    or search.lower() in name.lower()
                            ):
                                filtered.append(
                                    analysis
                                )

                        st.success(
                            f"{len(filtered)} analysis file(s) found."
                        )

                        if not filtered:

                            st.info(
                                "No analysis available."
                            )

                        else:

                            for analysis in filtered:

                                filename = analysis["name"]

                                with st.expander(

                                        f"🧠 {filename}",

                                        expanded=False,

                                ):

                                    ##################################################
                                    # Information
                                    ##################################################

                                    col1, col2 = st.columns(2)

                                    with col1:

                                        st.write(

                                            f"**Size:** {analysis['size']:,} bytes"

                                        )

                                    with col2:

                                        st.write(

                                            f"**Modified:** {analysis['modified']}"

                                        )

                                    ##################################################
                                    # Load Analysis
                                    ##################################################

                                    content = AIAnalysisService.load_analysis(
                                        filename
                                    )

                                    ##################################################
                                    # Preview
                                    ##################################################

                                    st.text_area(

                                        "Analysis Preview",

                                        value=content,

                                        height=300,

                                        disabled=True,

                                        key=f"analysis_preview_{filename}",

                                    )

                                    ##################################################
                                    # Statistics
                                    ##################################################

                                    words = len(
                                        content.split()
                                    )

                                    characters = len(
                                        content
                                    )

                                    c1, c2 = st.columns(2)

                                    with c1:

                                        st.metric(
                                            "Words",
                                            words,
                                        )

                                    with c2:

                                        st.metric(
                                            "Characters",
                                            characters,
                                        )

                                    ##################################################
                                    # Actions
                                    ##################################################

                                    col1, col2, col3, col4 = st.columns(4)

                                    with col1:

                                        st.download_button(

                                            "📥 Download",

                                            data=content,

                                            file_name=filename,

                                            mime="text/markdown",

                                            key=f"analysis_download_{filename}",

                                            use_container_width=True,

                                        )

                                    with col2:

                                        if st.button(

                                                "📑 Use In Report",

                                                key=f"analysis_report_{filename}",

                                                use_container_width=True,

                                        ):
                                            st.session_state[
                                                "selected_analysis"
                                            ] = filename

                                            st.success(
                                                "Analysis selected for report generation."
                                            )

                                    with col3:

                                        if st.button(

                                                "🔄 Regenerate",

                                                key=f"analysis_regenerate_{filename}",

                                                use_container_width=True,

                                        ):
                                            st.info(
                                                "Open the Analysis page to regenerate this analysis."
                                            )

                                    with col4:

                                        if st.button(

                                                "🗑 Delete",

                                                key=f"analysis_delete_{filename}",

                                                use_container_width=True,

                                        ):
                                            AIAnalysisService.delete_analysis(
                                                filename
                                            )

                                            st.success(
                                                "Analysis deleted."
                                            )

                                            st.rerun()



        #######################################################
        # Chat History
        #######################################################

        elif history_section == "Chats":

                            st.subheader(
                                "💬 AI Chat History"
                            )

                            search = st.text_input(

                                "Search Chat History",

                                placeholder="Search chat...",

                                key="chat_search",

                            )

                            filtered = []

                            for chat in chats:

                                name = chat.name

                                if (
                                        not search
                                        or search.lower() in name.lower()
                                ):
                                    filtered.append(chat)

                            st.success(
                                f"{len(filtered)} chat file(s) found."
                            )

                            if not filtered:

                                st.info(
                                    "No chat history available."
                                )

                            else:

                                for chat in filtered:

                                    filename = chat.name

                                    with st.expander(

                                            f"💬 {filename}",

                                            expanded=False,

                                    ):

                                        ##################################################
                                        # Load Chat
                                        ##################################################

                                        history = AIChatService.load_chat(
                                            filename
                                        )

                                        ##################################################
                                        # Information
                                        ##################################################

                                        st.write(
                                            f"**Messages:** {len(history)}"
                                        )

                                        st.write(
                                            f"**Filename:** {filename}"
                                        )

                                        ##################################################
                                        # Preview
                                        ##################################################

                                        preview = ""

                                        for item in history[:5]:
                                            preview += (
                                                f"👤 User:\n"
                                                f"{item.get('user', '')}\n\n"
                                                f"🤖 Assistant:\n"
                                                f"{item.get('assistant', '')}\n\n"
                                                "---------------------------------\n"
                                            )

                                        st.text_area(

                                            "Chat Preview",

                                            value=preview,

                                            height=300,

                                            disabled=True,

                                            key=f"chat_preview_{filename}",

                                        )

                                        ##################################################
                                        # Statistics
                                        ##################################################

                                        total_words = sum(

                                            len(
                                                (
                                                        item.get("user", "")
                                                        + " "
                                                        + item.get("assistant", "")
                                                ).split()
                                            )

                                            for item in history

                                        )

                                        col1, col2 = st.columns(2)

                                        with col1:

                                            st.metric(

                                                "Messages",

                                                len(history),

                                            )

                                        with col2:

                                            st.metric(

                                                "Words",

                                                total_words,

                                            )

                                        ##################################################
                                        # Actions
                                        ##################################################

                                        col1, col2, col3 = st.columns(3)

                                        with col1:

                                            st.download_button(

                                                "📥 Download",

                                                data=str(history),

                                                file_name=filename,

                                                mime="application/json",

                                                key=f"chat_download_{filename}",

                                                use_container_width=True,

                                            )

                                        with col2:

                                            if st.button(

                                                    "▶ Continue Chat",

                                                    key=f"continue_chat_{filename}",

                                                    use_container_width=True,

                                            ):
                                                st.session_state[
                                                    "chat_history"
                                                ] = history

                                                st.session_state[
                                                    "current_page"
                                                ] = "AI Chat"

                                                st.success(
                                                    "Chat loaded."
                                                )

                                        with col3:

                                            if st.button(

                                                    "🗑 Delete",

                                                    key=f"chat_delete_{filename}",

                                                    use_container_width=True,

                                            ):
                                                AIChatService.delete_chat(
                                                    filename
                                                )

                                                st.success(
                                                    "Chat deleted."
                                                )

                                                st.rerun()



        #######################################################
        # Reports
        #######################################################

        elif history_section == "Reports":

                                st.subheader(
                                    "📑 Saved Reports"
                                )

                                search = st.text_input(

                                    "Search Reports",

                                    placeholder="Search report...",

                                    key="report_search",

                                )

                                filtered = []

                                for report in reports:

                                    name = report["name"]

                                    if (
                                            not search
                                            or search.lower() in name.lower()
                                    ):
                                        filtered.append(report)

                                st.success(
                                    f"{len(filtered)} report(s) found."
                                )

                                if not filtered:

                                    st.info(
                                        "No reports available."
                                    )

                                else:

                                    for report in filtered:

                                        filename = report["name"]

                                        report_type = report["type"]

                                        with st.expander(

                                                f"📑 {filename}",

                                                expanded=False,

                                        ):

                                            ##################################################
                                            # Information
                                            ##################################################

                                            col1, col2 = st.columns(2)

                                            with col1:

                                                st.write(

                                                    f"**Format:** {report_type.upper()}"

                                                )

                                                st.write(

                                                    f"**Size:** {report['size']:,} bytes"

                                                )

                                            with col2:

                                                st.write(

                                                    f"**Modified:** {report['modified']}"

                                                )

                                                st.write(

                                                    f"**Folder:** {report_type}"

                                                )

                                            ##################################################
                                            # Load Report
                                            ##################################################

                                            content = ReportService.load_report(

                                                report_type,

                                                filename,

                                            )

                                            ##################################################
                                            # Preview
                                            ##################################################

                                            if report_type == "md":

                                                st.markdown(content)

                                            elif report_type == "html":

                                                tab1, tab2 = st.tabs(
                                                    [
                                                        "Preview",
                                                        "Source",
                                                    ]
                                                )

                                                with tab1:

                                                    st.components.v1.html(

                                                        content,

                                                        height=400,

                                                        scrolling=True,

                                                    )

                                                with tab2:

                                                    st.code(
                                                        content,
                                                        language="html",
                                                    )

                                            elif report_type == "json":

                                                st.json(content)

                                            elif report_type == "pdf":

                                                st.info(
                                                    "PDF preview is unavailable."
                                                )

                                            else:

                                                st.text_area(

                                                    "Preview",

                                                    str(content),

                                                    height=300,

                                                    disabled=True,

                                                    key=f"report_preview_{filename}",

                                                )

                                            ##################################################
                                            # Actions
                                            ##################################################

                                            report_path = Path(
                                                report["path"]
                                            )

                                            col1, col2, col3 = st.columns(3)

                                            with col1:

                                                with open(
                                                        report_path,
                                                        "rb",
                                                ) as file:
                                                    st.download_button(

                                                        "📥 Download",

                                                        data=file.read(),

                                                        file_name=filename,

                                                        mime="application/octet-stream",

                                                        key=f"report_download_{filename}",

                                                        use_container_width=True,

                                                    )

                                            with col2:

                                                if st.button(

                                                        "📂 Open Report",

                                                        key=f"report_open_{filename}",

                                                        use_container_width=True,

                                                ):
                                                    st.session_state[
                                                        "selected_report"
                                                    ] = report

                                                    st.success(
                                                        "Report selected."
                                                    )

                                            with col3:

                                                if st.button(

                                                        "🗑 Delete",

                                                        key=f"report_delete_{filename}",

                                                        use_container_width=True,

                                                ):
                                                    ReportService.delete_report(

                                                        report_type,

                                                        filename,

                                                    )

                                                    st.success(
                                                        "Report deleted."
                                                    )

                                                    st.rerun()



        #######################################################
        # Exports
        #######################################################

        elif history_section == "Exports":

                                    st.subheader(
                                        "📤 Exported Files"
                                    )

                                    search = st.text_input(

                                        "Search Exports",

                                        placeholder="Search exported files...",

                                        key="export_search",

                                    )

                                    filtered = []

                                    for export in exports:

                                        filename = export["name"]

                                        if (
                                                not search
                                                or search.lower() in filename.lower()
                                        ):
                                            filtered.append(export)

                                    st.success(
                                        f"{len(filtered)} export(s) found."
                                    )

                                    if not filtered:

                                        st.info(
                                            "No exported files available."
                                        )

                                    else:

                                        for export in filtered:

                                            filename = export["name"]

                                            export_type = export["type"]

                                            export_path = Path(
                                                export["path"]
                                            )

                                            with st.expander(

                                                    f"📤 {filename}",

                                                    expanded=False,

                                            ):

                                                ##################################################
                                                # Information
                                                ##################################################

                                                col1, col2 = st.columns(2)

                                                with col1:

                                                    st.write(
                                                        f"**Format:** {export_type.upper()}"
                                                    )

                                                    st.write(
                                                        f"**Size:** {export['size']:,} bytes"
                                                    )

                                                with col2:

                                                    st.write(
                                                        f"**Modified:** {export['modified']}"
                                                    )

                                                    st.write(
                                                        f"**Folder:** {export_type}"
                                                    )

                                                ##################################################
                                                # Preview
                                                ##################################################

                                                if export_type in [
                                                    "md",
                                                    "txt",
                                                    "html",
                                                    "json",
                                                ]:

                                                    try:

                                                        content = ExportService.load_export(

                                                            export_type,

                                                            filename,

                                                        )

                                                        if export_type == "md":

                                                            st.markdown(
                                                                content
                                                            )

                                                        elif export_type == "html":

                                                            tab1, tab2 = st.tabs(
                                                                [
                                                                    "Preview",
                                                                    "Source",
                                                                ]
                                                            )

                                                            with tab1:

                                                                st.components.v1.html(

                                                                    content,

                                                                    height=350,

                                                                    scrolling=True,

                                                                )

                                                            with tab2:

                                                                st.code(
                                                                    content,
                                                                    language="html",
                                                                )

                                                        elif export_type == "json":

                                                            st.json(
                                                                content
                                                            )

                                                        else:

                                                            st.text_area(

                                                                "Preview",

                                                                value=str(content),

                                                                height=250,

                                                                disabled=True,

                                                                key=f"export_preview_{filename}",

                                                            )

                                                    except Exception as e:

                                                        st.warning(str(e))

                                                else:

                                                    st.info(
                                                        "Preview not available."
                                                    )

                                                ##################################################
                                                # Actions
                                                ##################################################

                                                col1, col2 = st.columns(2)

                                                with col1:

                                                    with open(
                                                            export_path,
                                                            "rb",
                                                    ) as file:
                                                        st.download_button(

                                                            "📥 Download",

                                                            data=file.read(),

                                                            file_name=filename,

                                                            mime="application/octet-stream",

                                                            key=f"export_download_{filename}",

                                                            use_container_width=True,

                                                        )

                                                with col2:

                                                    if st.button(

                                                            "🗑 Delete",

                                                            key=f"export_delete_{filename}",

                                                            use_container_width=True,

                                                    ):
                                                        ExportService.delete_export(

                                                            export_type,

                                                            filename,

                                                        )

                                                        st.success(
                                                            "Export deleted."
                                                        )

                                                        st.rerun()

        #######################################################
        # Project Explorer
        #######################################################

        st.divider()

        st.subheader(
            "📁 Project Explorer"
        )

        project_folders = [

            ("🎥 Uploads", Path(VideoService.UPLOAD_FOLDER)),

            ("🎵 Audio", Path(AudioService.AUDIO_FOLDER)),

            ("📝 Transcripts", Path(SpeechService.TRANSCRIPT_FOLDER)),

            ("🧠 Analysis", Path(AIAnalysisService.ANALYSIS_FOLDER)),

            ("💬 Chat History", Path(AIChatService.CHAT_FOLDER)),

            ("📑 Reports", Path(ReportService.REPORT_FOLDER)),

            ("📤 Exports", Path(ExportService.EXPORT_FOLDER)),

            ("🎥 Video Metadata", Path("metadata/video")),

            ("🎵 Audio Metadata", Path("metadata/audio")),

        ]

        explorer = []

        total_files = 0

        total_size = 0

        #######################################################
        # Scan folders
        #######################################################

        for title, folder in project_folders:
            folder.mkdir(
                parents=True,
                exist_ok=True,
            )

            files = list(folder.glob("*"))

            file_count = len(files)

            folder_size = sum(
                f.stat().st_size
                for f in files
                if f.is_file()
            )

            total_files += file_count

            total_size += folder_size

            explorer.append(
                {
                    "Folder": title,
                    "Files": file_count,
                    "Storage (KB)": round(
                        folder_size / 1024,
                        2,
                    ),
                    "Path": str(folder),
                }
            )

        #######################################################
        # Explorer Table
        #######################################################

        st.dataframe(
            explorer,
            hide_index=True,
            use_container_width=True,
        )

        st.divider()

        #######################################################
        # Project Summary
        #######################################################

        st.subheader(
            "📊 Project Summary"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Files",
                total_files,
            )

        with col2:

            st.metric(
                "Total Storage",
                f"{total_size / (1024 * 1024):.2f} MB",
            )

        st.divider()

        #######################################################
        # Folder Browser
        #######################################################

        folder_names = [
            title
            for title, _ in project_folders
        ]

        selected_folder = st.selectbox(
            "Browse Folder",
            folder_names,
            key="history_folder_browser",
        )

        folder_path = dict(project_folders)[selected_folder]

        files = sorted(
            folder_path.glob("*")
        )

        if not files:

            st.info(
                "Folder is empty."
            )

        else:

            for file in files:
                st.write(
                    f"📄 {file.name}"
                )

        st.divider()

        #######################################################
        # Project Maintenance
        #######################################################

        st.subheader(
            "🧹 Project Maintenance"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                    "🔄 Refresh",
                    use_container_width=True,
            ):
                st.rerun()

        with col2:

            if st.button(
                    "🗑 Clear Session",
                    use_container_width=True,
            ):
                keep = {
                    "orchestrator": st.session_state.get(
                        "orchestrator"
                    )
                }

                st.session_state.clear()

                st.session_state.update(keep)

                st.success(
                    "Session cleared successfully."
                )

                st.rerun()

        st.divider()

        #######################################################
        # History Summary
        #######################################################

        st.subheader(
            "📈 History Summary"
        )

        c1, c5, c2, c3, c4 ,c6 ,c7, c8 = st.columns(8)

        with c1:

            st.metric(
                "Videos",
                len(videos),
            )

        with c5:

            st.metric("audios",len(audios))

        with c2:

            st.metric(
                "Reports",
                len(reports),
            )

        with c3:

            st.metric(
                "Exports",
                len(exports),
            )

        with c6:

            st.metric(
                "Transcripts",

                len(transcripts)
                ,
            )

        with c7:

            st.metric(
                "Analysis",
                len(analyses)
,
            )

        with c8:

            st.metric(
                "Chats",
                len(chats)
            ,
            )

        with c4:

            st.metric(
                "Total Items",
                len(videos)
                + len(audios)
                + len(transcripts)
                + len(analyses)
                + len(chats)
                + len(reports)
                + len(exports),
            )

        st.divider()

        #######################################################
        # Information
        #######################################################

        st.info(
            """
        This page displays all project resources stored on disk.

        • Browse uploaded videos\n
        • Browse extracted audio\n
        • Browse transcripts\n
        • Browse AI analysis\n
        • Browse chat history\n
        • Browse reports\n
        • Browse exported files\n
        • Download files\n
        • Delete files\n
        • View project statistics\n
        """
        )



        #######################################################
        # Footer
        #######################################################


        FooterAgent.render()

