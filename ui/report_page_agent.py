"""
report_page_agent.py

Report Page Agent

Responsibilities
----------------
- Generate reports from saved project files
- Browse reports
- Preview reports
- Download reports
- Delete reports
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from providers.model_manager import ModelManager

from services.video_agent_service import VideoService
from services.audio_agent_service import AudioService
from services.speech_agent_service import SpeechService
from services.ai_analysis_agent_service import AIAnalysisService
from services.ai_chat_agent_service import AIChatService
from services.report_agent_service import ReportService

from .header_agent import HeaderAgent
from .footer_agent import FooterAgent


class ReportPageAgent:

    MIME_TYPES = {

        "pdf": "application/pdf",

        "html": "text/html",

        "md": "text/markdown",

        "txt": "text/plain",

        "json": "application/json",

    }

    ICONS = {

        "pdf": "📄",

        "html": "🌐",

        "md": "📝",

        "txt": "📃",

        "json": "🗂️",

    }

    CHAT_FOLDER = Path("chat_history")

    def render(self):

        HeaderAgent.render(
            "📑 Report Generator"
        )

        #######################################################
        # Load Existing Project Files
        #######################################################

        videos = VideoService.list_videos()

        audios = AudioService.list_audio()

        transcripts = SpeechService.list_transcripts()

        analyses = AIAnalysisService.list_analysis()

        chats = AIChatService.list_chats()

        st.subheader(
            "Generate Report From Existing Files"
        )

        #######################################################
        # Video
        #######################################################

        video_names = sorted(videos)

        selected_video = st.selectbox(

            "Video",

            video_names,

            index=None,

            placeholder="Select a video",

        )

        #######################################################
        # Audio
        #######################################################

        audio_names = audios

        selected_audio = st.selectbox(

            "Audio",

            audio_names,

            index=None,

            placeholder="Select audio",

        )

        #######################################################
        # Transcript
        #######################################################

        transcript_names = [
            item["name"]
            for item in transcripts
        ] if transcripts else []

        selected_transcript = st.selectbox(

            "Transcript",

            transcript_names,

            index=None,

            placeholder="Select transcript",

        )

        #######################################################
        # Analysis
        #######################################################

        analysis_names = [
            item["name"]
            for item in analyses
        ] if analyses else []

        selected_analysis = st.selectbox(

            "Analysis",

            analysis_names,

            index=None,

            placeholder="Select analysis",

        )

        #######################################################
        # Chat
        #######################################################

        chat_names = [
            file.name
            for file in chats
        ] if chats else []

        selected_chat = st.selectbox(

            "Chat History",

            chat_names,

            index=None,

            placeholder="Select chat history",

        )

        st.divider()

        #######################################################
        # AI Provider
        #######################################################

        provider_name = st.selectbox(

            "AI Provider",

            [
                "Ollama",
                "OpenAI",
                "Anthropic",
            ],

        )

        #######################################################
        # Model
        #######################################################

        models = ModelManager.get_models(
            provider_name
        )

        model_name = st.selectbox(

            "Model",

            models,

        )

        st.divider()

        #######################################################
        # Generate Report
        #######################################################

        if st.button(

            "🚀 Generate Report",

            use_container_width=True,

        ):

            if not all(

                [

                    selected_video,

                    selected_audio,

                    selected_transcript,

                    selected_analysis,

                    selected_chat,

                ]

            ):

                st.warning(

                    "Please select all required files."

                )

            else:

                with st.spinner(

                    "Generating report..."

                ):

                    ##################################################
                    # Load Files
                    ##################################################

                    video_metadata = (
                        VideoService.load_metadata(
                            selected_video
                        )
                    )

                    audio_metadata = (
                        AudioService.load_metadata(
                            selected_audio
                        )
                    )

                    transcript = (
                        SpeechService.load_transcript(
                            selected_transcript
                        )
                    )

                    analysis = (
                        AIAnalysisService.load_analysis(
                            selected_analysis
                        )
                    )

                    chat = (
                        AIChatService.load_chat(
                            self,
                            selected_chat
                        )
                    )

                    ##################################################
                    # Build Report
                    ##################################################

                    report = (
                        ReportService.build_report_from_files(

                            video_metadata=
                                video_metadata,

                            audio_metadata=
                                audio_metadata,

                            transcript=
                                transcript,

                            analysis=
                                analysis,

                            chat=
                                chat,

                            provider=
                                provider_name,

                            model=
                                model_name,

                        )
                    )

                    ##################################################
                    # Save All Formats
                    ##################################################

                    filename = (
                        ReportService.generate_filename(

                            video_metadata.get(
                                "filename",
                                "video",
                            ),

                            "report",

                        )
                    )

                    ReportService.save_all_reports(

                        filename=
                            filename,

                        content=
                            report,

                        data={

                            "video_name":
                                video_metadata.get("filename"),

                            "video_duration":
                                video_metadata.get("duration"),

                            "video_resolution":
                                video_metadata.get("resolution"),

                            "video_fps":
                                video_metadata.get("fps"),

                            "video_format":
                                video_metadata.get("format"),

                            "video_size":
                                video_metadata.get("size"),

                            "audio_name":
                                audio_metadata.get("filename"),

                            "audio_duration":
                                audio_metadata.get("duration"),

                            "channels":
                                audio_metadata.get("channels"),

                            "sample_rate":
                                audio_metadata.get("sample_rate"),

                            "audio_format":
                                audio_metadata.get("format"),

                            "audio_size":
                                audio_metadata.get("size"),

                            "transcript":
                                transcript,

                            "analysis":
                                analysis,

                            "chat":
                                chat,

                            "provider":
                                provider_name,

                            "model":
                                model_name,

                        },

                    )

                    st.success(

                        "✅ Report generated successfully."

                    )

                    st.rerun()

        st.divider()

        #######################################################
        # Saved Reports
        #######################################################

        st.subheader(
            "📂 Saved Reports"
        )

        reports = ReportService.list_reports()

        if not reports:

            st.info(
                "No reports available."
            )

            FooterAgent.render()

            return

        report_options = [

            f"{report['type'].upper()} • {report['name']}"

            for report in reports

        ]

        selected_report = st.selectbox(

            "Select Report",

            report_options,

        )

        report_index = report_options.index(
            selected_report
        )

        report = reports[
            report_index
        ]

        report_type = report["type"]

        filename = report["name"]

        path = Path(
            report["path"]
        )

        st.divider()

        #######################################################
        # Report Details
        #######################################################

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(

                "Format",

                report_type.upper(),

            )

        with c2:

            st.metric(

                "Size",

                f"{report['size']:,} B",

            )

        with c3:

            st.metric(

                "Modified",

                report["modified"],

            )

        with c4:

            st.metric(

                "Filename",

                filename,

            )

        st.divider()

        #######################################################
        # Preview
        #######################################################

        st.subheader(
            "👁 Report Preview"
        )

        report_content = ReportService.load_report(

            report_type,

            filename,

        )

        #######################################################
        # Markdown
        #######################################################

        if report_type == "md":

            st.markdown(
                report_content
            )

        #######################################################
        # TXT
        #######################################################

        elif report_type == "txt":

            st.text_area(

                "Text",

                report_content,

                height=600,

                disabled=True,

            )

        #######################################################
        # HTML
        #######################################################

        elif report_type == "html":

            tab1, tab2 = st.tabs(

                [

                    "Rendered",

                    "Source",

                ]

            )

            with tab1:

                st.components.v1.html(

                    report_content,

                    height=650,

                    scrolling=True,

                )

            with tab2:

                st.code(

                    report_content,

                    language="html",

                )

        #######################################################
        # JSON
        #######################################################

        elif report_type == "json":

            st.json(
                report_content
            )

        #######################################################
        # PDF
        #######################################################

        elif report_type == "pdf":

            st.info(

                "PDF preview is unavailable."

            )

            st.write(

                "Use Download below."

            )

        else:

            st.warning(

                "Unknown report type."

            )

        st.divider()

        #######################################################
        # Report Actions
        #######################################################

        st.subheader(
            "⚡ Report Actions"
        )

        col1, col2, col3 = st.columns(3)

        #######################################################
        # Download
        #######################################################

        with col1:

            with open(
                path,
                "rb",
            ) as file:

                st.download_button(

                    label="📥 Download",

                    data=file.read(),

                    file_name=filename,

                    mime=self.MIME_TYPES.get(
                        report_type,
                        "application/octet-stream",
                    ),

                    key=f"download_{filename}",

                    use_container_width=True,

                )

        #######################################################
        # Delete
        #######################################################

        with col2:

            if st.button(

                "🗑 Delete",

                key=f"delete_{filename}",

                use_container_width=True,

            ):

                ReportService.delete_report(

                    report_type,

                    filename,

                )

                st.success(
                    "Report deleted successfully."
                )

                st.rerun()

        #######################################################
        # Refresh
        #######################################################

        with col3:

            if st.button(

                "🔄 Refresh",

                use_container_width=True,

            ):

                st.rerun()

        st.divider()

        #######################################################
        # Report Statistics
        #######################################################

        st.subheader(
            "📊 Report Statistics"
        )

        counts = ReportService.report_count()

        storage = ReportService.report_storage()

        row1 = st.columns(5)

        with row1[0]:

            st.metric(
                "PDF",
                counts.get(
                    "pdf",
                    0,
                ),
            )

        with row1[1]:

            st.metric(
                "HTML",
                counts.get(
                    "html",
                    0,
                ),
            )

        with row1[2]:

            st.metric(
                "Markdown",
                counts.get(
                    "md",
                    0,
                ),
            )

        with row1[3]:

            st.metric(
                "TXT",
                counts.get(
                    "txt",
                    0,
                ),
            )

        with row1[4]:

            st.metric(
                "JSON",
                counts.get(
                    "json",
                    0,
                ),
            )

        st.divider()

        #######################################################
        # Storage Usage
        #######################################################

        st.subheader(
            "💾 Storage Usage"
        )

        storage_table = [

            {

                "Format": "PDF",

                "Size (KB)": round(
                    storage.get(
                        "pdf",
                        0,
                    ) / 1024,
                    2,
                ),

            },

            {

                "Format": "HTML",

                "Size (KB)": round(
                    storage.get(
                        "html",
                        0,
                    ) / 1024,
                    2,
                ),

            },

            {

                "Format": "Markdown",

                "Size (KB)": round(
                    storage.get(
                        "md",
                        0,
                    ) / 1024,
                    2,
                ),

            },

            {

                "Format": "TXT",

                "Size (KB)": round(
                    storage.get(
                        "txt",
                        0,
                    ) / 1024,
                    2,
                ),

            },

            {

                "Format": "JSON",

                "Size (KB)": round(
                    storage.get(
                        "json",
                        0,
                    ) / 1024,
                    2,
                ),

            },

        ]

        st.dataframe(

            storage_table,

            hide_index=True,

            use_container_width=True,

        )

        st.divider()

        #######################################################
        # Search & Filter
        #######################################################

        st.subheader(
            "🔍 Search Reports"
        )

        col1, col2 = st.columns(2)

        with col1:

            search_text = st.text_input(

                "Search by filename",

                placeholder="meeting, lecture, report...",

            )

        with col2:

            selected_format = st.selectbox(

                "Filter Format",

                [

                    "All",

                    "PDF",

                    "HTML",

                    "Markdown",

                    "TXT",

                    "JSON",

                ],

            )

        #######################################################
        # Apply Filter
        #######################################################

        filtered_reports = []

        for item in reports:

            if search_text:

                if search_text.lower() not in item[
                    "name"
                ].lower():

                    continue

            if selected_format != "All":

                if (
                    item["type"].lower()
                    != selected_format.lower()
                ):

                    continue

            filtered_reports.append(item)

        st.success(

            f"{len(filtered_reports)} report(s) found."

        )

        #######################################################
        # Browse Reports
        #######################################################

        st.subheader(
            "📂 Available Reports"
        )

        if not filtered_reports:

            st.info(
                "No reports match your filter."
            )

        else:

            for report in filtered_reports:

                icon = self.ICONS.get(

                    report["type"],

                    "📄",

                )

                with st.expander(

                    f"{icon} {report['name']}",

                    expanded=False,

                ):

                    c1, c2 = st.columns(
                        [4, 1]
                    )

                    with c1:

                        st.write(

                            f"**Format:** {report['type'].upper()}"

                        )

                        st.write(

                            f"**Modified:** {report['modified']}"

                        )

                        st.write(

                            f"**Size:** {report['size']:,} bytes"

                        )

                    with c2:

                        if st.button(

                            "Open",

                            key=f"open_{report['type']}_{report['name']}",

                            use_container_width=True,

                        ):

                            st.session_state[
                                "selected_report"
                            ] = report

                            st.rerun()

        st.divider()

        #######################################################
        # Report Folder Explorer
        #######################################################

        st.subheader(
            "📁 Report Folder Explorer"
        )

        folder_map = {

            "📄 PDF":
                "pdf",

            "🌐 HTML":
                "html",

            "📝 Markdown":
                "md",

            "📃 TXT":
                "txt",

            "🗂 JSON":
                "json",

        }

        tabs = st.tabs(
            list(folder_map.keys())
        )

        for tab, (title, report_type) in zip(
            tabs,
            folder_map.items(),
        ):

            with tab:

                folder_reports = [

                    report

                    for report in reports

                    if report["type"] == report_type

                ]

                st.metric(

                    "Files",

                    len(folder_reports),

                )

                if not folder_reports:

                    st.info(
                        "No files found."
                    )

                    continue

                for report in folder_reports:

                    icon = self.ICONS.get(

                        report_type,

                        "📄",

                    )

                    with st.expander(

                        f"{icon} {report['name']}",

                        expanded=False,

                    ):

                        st.write(

                            f"**Filename:** {report['name']}"

                        )

                        st.write(

                            f"**Modified:** {report['modified']}"

                        )

                        st.write(

                            f"**Size:** {report['size']:,} bytes"

                        )

                        col1, col2 = st.columns(2)

                        ###################################################
                        # Download
                        ###################################################

                        with col1:

                            with open(
                                report["path"],
                                "rb",
                            ) as file:

                                st.download_button(

                                    label="📥 Download",

                                    data=file.read(),

                                    file_name=report["name"],

                                    mime=self.MIME_TYPES.get(

                                        report_type,

                                        "application/octet-stream",

                                    ),

                                    key=f"folder_download_{report_type}_{report['name']}",

                                    use_container_width=True,

                                )

                        ###################################################
                        # Delete
                        ###################################################

                        with col2:

                            if st.button(

                                "🗑 Delete",

                                key=f"folder_delete_{report_type}_{report['name']}",

                                use_container_width=True,

                            ):

                                ReportService.delete_report(

                                    report_type,

                                    report["name"],

                                )

                                st.success(

                                    "Report deleted."

                                )

                                st.rerun()

        st.divider()

        #######################################################
        # Report Analytics Dashboard
        #######################################################

        st.subheader(
            "📊 Report Analytics"
        )

        counts = ReportService.report_count()

        storage = ReportService.report_storage()

        total_reports = counts.get(
            "total",
            0,
        )

        total_storage = storage.get(
            "total",
            0,
        )

        latest_report = None

        largest_report = None

        if reports:

            latest_report = max(
                reports,
                key=lambda x: x["modified"],
            )

            largest_report = max(
                reports,
                key=lambda x: x["size"],
            )

        #######################################################
        # Summary Metrics
        #######################################################

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Total Reports",
                total_reports,
            )

        with c2:

            st.metric(
                "Storage (MB)",
                round(
                    total_storage / (1024 * 1024),
                    2,
                ),
            )

        with c3:

            st.metric(
                "PDF Files",
                counts.get(
                    "pdf",
                    0,
                ),
            )

        with c4:

            st.metric(
                "JSON Files",
                counts.get(
                    "json",
                    0,
                ),
            )

        st.divider()

        #######################################################
        # Latest Report
        #######################################################

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "🕒 Latest Report"
            )

            if latest_report:

                st.write(
                    f"**Name:** {latest_report['name']}"
                )

                st.write(
                    f"**Format:** {latest_report['type']}"
                )

                st.write(
                    f"**Modified:** {latest_report['modified']}"
                )

                st.write(
                    f"**Size:** {latest_report['size']:,} bytes"
                )

            else:

                st.info(
                    "No reports available."
                )

        #######################################################
        # Largest Report
        #######################################################

        with col2:

            st.subheader(
                "📦 Largest Report"
            )

            if largest_report:

                st.write(
                    f"**Name:** {largest_report['name']}"
                )

                st.write(
                    f"**Format:** {largest_report['type']}"
                )

                st.write(
                    f"**Size:** {largest_report['size']:,} bytes"
                )

                st.write(
                    f"**Modified:** {largest_report['modified']}"
                )

            else:

                st.info(
                    "No reports available."
                )

        st.divider()

        #######################################################
        # Recent Reports
        #######################################################

        st.subheader(
            "📝 Recent Reports"
        )

        recent_reports = sorted(
            reports,
            key=lambda x: x["modified"],
            reverse=True,
        )[:10]

        if recent_reports:

            table = []

            for report in recent_reports:

                table.append(
                    {
                        "Name": report["name"],
                        "Format": report["type"].upper(),
                        "Size (KB)": round(
                            report["size"] / 1024,
                            2,
                        ),
                        "Modified": report["modified"],
                    }
                )

            st.dataframe(
                table,
                hide_index=True,
                use_container_width=True,
            )

        else:

            st.info(
                "No recent reports found."
            )

        st.divider()

        #######################################################
        # Compare Reports
        #######################################################

        st.subheader(
            "⚖️ Compare Reports"
        )

        if len(reports) < 2:

            st.info(
                "At least two reports are required."
            )

        else:

            report_names = [

                f"{r['type'].upper()} • {r['name']}"

                for r in reports

            ]

            col1, col2 = st.columns(2)

            with col1:

                left_selection = st.selectbox(

                    "First Report",

                    report_names,

                    key="compare_left",

                )

            with col2:

                right_selection = st.selectbox(

                    "Second Report",

                    report_names,

                    index=1,

                    key="compare_right",

                )

            left = reports[
                report_names.index(
                    left_selection
                )
            ]

            right = reports[
                report_names.index(
                    right_selection
                )
            ]

            left_content = ReportService.load_report(

                left["type"],

                left["name"],

            )

            right_content = ReportService.load_report(

                right["type"],

                right["name"],

            )

            st.divider()

            c1, c2 = st.columns(2)

            ###################################################
            # Left Report
            ###################################################

            with c1:

                st.markdown(
                    "### 📄 Report A"
                )

                st.write(
                    f"**Name:** {left['name']}"
                )

                st.write(
                    f"**Format:** {left['type'].upper()}"
                )

                st.write(
                    f"**Size:** {left['size']:,} bytes"
                )

                st.write(
                    f"**Modified:** {left['modified']}"
                )

                if left["type"] == "json":

                    st.json(
                        left_content
                    )

                elif left["type"] == "html":

                    st.components.v1.html(

                        left_content,

                        height=400,

                        scrolling=True,

                    )

                elif left["type"] == "pdf":

                    st.info(
                        "PDF preview unavailable."
                    )

                else:

                    st.text_area(

                        "Report A",

                        str(left_content),

                        height=400,

                        disabled=True,

                        key="left_report",

                    )

            ###################################################
            # Right Report
            ###################################################

            with c2:

                st.markdown(
                    "### 📄 Report B"
                )

                st.write(
                    f"**Name:** {right['name']}"
                )

                st.write(
                    f"**Format:** {right['type'].upper()}"
                )

                st.write(
                    f"**Size:** {right['size']:,} bytes"
                )

                st.write(
                    f"**Modified:** {right['modified']}"
                )

                if right["type"] == "json":

                    st.json(
                        right_content
                    )

                elif right["type"] == "html":

                    st.components.v1.html(

                        right_content,

                        height=400,

                        scrolling=True,

                    )

                elif right["type"] == "pdf":

                    st.info(
                        "PDF preview unavailable."
                    )

                else:

                    st.text_area(

                        "Report B",

                        str(right_content),

                        height=400,

                        disabled=True,

                        key="right_report",

                    )

            st.divider()

            ###################################################
            # Comparison Summary
            ###################################################

            st.subheader(
                "📋 Comparison Summary"
            )

            comparison = {

                "Attribute": [
                    "Filename",
                    "Format",
                    "Size (Bytes)",
                    "Modified",
                ],

                "Report A": [

                    left["name"],

                    left["type"].upper(),

                    left["size"],

                    left["modified"],

                ],

                "Report B": [

                    right["name"],

                    right["type"].upper(),

                    right["size"],

                    right["modified"],

                ],

            }

            st.dataframe(

                comparison,

                hide_index=True,

                use_container_width=True,

            )

        st.divider()

        #######################################################
        # Favorites / Bulk Operations
        #######################################################

        st.subheader(
            "⭐ Favorites & Bulk Operations"
        )

        if "favorite_reports" not in st.session_state:

            st.session_state.favorite_reports = []

        report_options = [

            f"{r['type'].upper()} • {r['name']}"

            for r in reports

        ]

        selected_reports = st.multiselect(

            "Select Reports",

            report_options,

        )

        col1, col2, col3 = st.columns(3)

        #######################################################
        # Add Favorites
        #######################################################

        with col1:

            if st.button(

                "⭐ Add To Favorites",

                use_container_width=True,

            ):

                for report in selected_reports:

                    if report not in st.session_state.favorite_reports:

                        st.session_state.favorite_reports.append(
                            report
                        )

                st.success(
                    "Favorite list updated."
                )

        #######################################################
        # Bulk Download
        #######################################################

        with col2:

            if st.button(

                "📥 Prepare Downloads",

                use_container_width=True,

            ):

                if not selected_reports:

                    st.warning(
                        "No reports selected."
                    )

                else:

                    st.success(
                        f"{len(selected_reports)} report(s) selected."
                    )

        #######################################################
        # Bulk Delete
        #######################################################

        with col3:

            if st.button(

                "🗑 Delete Selected",

                use_container_width=True,

            ):

                deleted = 0

                for selection in selected_reports:

                    report_type, filename = selection.split(
                        " • ",
                        1,
                    )

                    if ReportService.delete_report(

                        report_type.lower(),

                        filename,

                    ):

                        deleted += 1

                st.success(
                    f"{deleted} report(s) deleted."
                )

                st.rerun()

        st.divider()

        #######################################################
        # Favorite Reports
        #######################################################

        st.subheader(
            "⭐ Favorite Reports"
        )

        if not st.session_state.favorite_reports:

            st.info(
                "No favorite reports."
            )

        else:

            for favorite in st.session_state.favorite_reports:

                st.write(
                    f"⭐ {favorite}"
                )

        st.divider()

        #######################################################
        # Export Summary
        #######################################################

        st.subheader(
            "📦 Report Summary"
        )

        summary = {

            "Total Reports":
                counts.get(
                    "total",
                    0,
                ),

            "PDF":
                counts.get(
                    "pdf",
                    0,
                ),

            "HTML":
                counts.get(
                    "html",
                    0,
                ),

            "Markdown":
                counts.get(
                    "md",
                    0,
                ),

            "TXT":
                counts.get(
                    "txt",
                    0,
                ),

            "JSON":
                counts.get(
                    "json",
                    0,
                ),

            "Storage (MB)":
                round(
                    storage.get(
                        "total",
                        0,
                    ) / (1024 * 1024),
                    2,
                ),

        }

        st.json(summary)

        st.divider()

        #######################################################
        # Maintenance
        #######################################################

        st.subheader(
            "🧹 Report Maintenance"
        )

        col1, col2 = st.columns(2)

        #######################################################
        # Refresh
        #######################################################

        with col1:

            if st.button(

                "🔄 Refresh Reports",

                use_container_width=True,

            ):

                st.rerun()

        #######################################################
        # Clear All Reports
        #######################################################

        with col2:

            if st.button(

                "🗑 Clear All Reports",

                type="primary",

                use_container_width=True,

            ):

                ReportService.clear_reports()

                st.success(
                    "All reports deleted successfully."
                )

                st.rerun()

        st.divider()

        #######################################################
        # Dashboard Summary
        #######################################################

        st.subheader(
            "📈 Dashboard Summary"
        )

        summary1, summary2, summary3, summary4 = st.columns(4)

        with summary1:

            st.metric(

                "Total",

                counts.get(
                    "total",
                    0,
                ),

            )

        with summary2:

            st.metric(

                "Formats",

                len(
                    ReportService.FORMAT_FOLDERS
                ),

            )

        with summary3:

            st.metric(

                "Storage",

                f"{storage.get('total',0)/(1024*1024):.2f} MB",

            )

        with summary4:

            latest_name = (

                latest_report["name"]

                if latest_report

                else "None"

            )

            st.metric(

                "Latest",

                latest_name,

            )

        st.divider()

        #######################################################
        # Folder Statistics
        #######################################################

        st.subheader(
            "📂 Folder Statistics"
        )

        folder_stats = []

        for report_type, folder in ReportService.FORMAT_FOLDERS.items():

            files = list(
                folder.glob("*.*")
            )

            folder_stats.append(

                {

                    "Folder": folder.name,

                    "Files": len(files),

                    "Storage (KB)": round(

                        sum(
                            f.stat().st_size
                            for f in files
                        ) / 1024,

                        2,

                    ),

                }

            )

        st.dataframe(

            folder_stats,

            hide_index=True,

            use_container_width=True,

        )

        st.divider()

        #######################################################
        # Footer
        #######################################################

        FooterAgent.render()