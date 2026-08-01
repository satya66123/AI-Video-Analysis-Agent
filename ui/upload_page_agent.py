"""
upload_page_agent.py

Upload Page Agent
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

from services.video_service import VideoService
from utils.file_validator import FileValidator

from .footer_agent import FooterAgent
from .header_agent import HeaderAgent
from .statusbar_agent import StatusBarAgent


class UploadPageAgent:

    def __init__(self):

        self.validator = FileValidator()
        self.video_service = VideoService()
        self.orchestrator = st.session_state.orchestrator

    def recent_videos(self):

        st.divider()

        st.subheader("🎬 Recent Videos")

        videos = self.video_service.list_videos()

        if not videos:
            st.info("No uploaded videos found.")

            return

        for video in videos[-5:][::-1]:

            video_path = Path(
                self.video_service.UPLOAD_FOLDER
            ) / video

            if not video_path.exists():
                continue

            size = video_path.stat().st_size / (
                    1024 * 1024
            )

            modified = datetime.fromtimestamp(
                video_path.stat().st_mtime
            )

            with st.expander(f"📹 {video}"):

                col1, col2 = st.columns(2)

                with col1:
                    st.write(
                        f"**Filename:** {video}"
                    )

                    st.write(
                        f"**Extension:** {video_path.suffix}"
                    )

                    st.write(
                        f"**Size:** {size:.2f} MB"
                    )

                with col2:
                    st.write(
                        f"**Uploaded:** {modified:%d-%m-%Y %I:%M %p}"
                    )

                    st.write(
                        f"**Location:** {video_path.parent}"
                    )

                    st.write(
                        f"**Status:** Available"
                    )

    def render(self):

        HeaderAgent.render("📤 Upload Video")

        uploaded_file = st.file_uploader(
            "Choose Video",
            type=[
                "mp4",
                "avi",
                "mov",
                "mkv",
                "webm",
            ],
        )

        if uploaded_file is None:
            st.info("Upload a video to begin.")

            self.recent_videos()

            FooterAgent.render()

            return

        self.preview(uploaded_file)

        st.divider()

        self.metadata(uploaded_file)

        st.divider()

        if st.button(
            "🚀 Start Analysis",
            type="primary",
            use_container_width=True,
        ):

            self.start(uploaded_file)

        def render(self):

            HeaderAgent.render("📤 Upload Video")

            uploaded_file = st.file_uploader(
                "Choose Video",
                type=[
                    "mp4",
                    "avi",
                    "mov",
                    "mkv",
                    "webm",
                ],
            )

            if uploaded_file is None:

                st.info("Upload a video to begin.")

            else:

                self.preview(uploaded_file)

                st.divider()

                self.metadata(uploaded_file)

                st.divider()

                if st.button(
                        "🚀 Start Analysis",
                        type="primary",
                        use_container_width=True,
                ):
                    self.start(uploaded_file)

            # Always display recent videos
            self.recent_videos()

            StatusBarAgent.render()

            FooterAgent.render()

    def preview(self, uploaded_file):

        st.subheader("Preview")

        st.video(uploaded_file)

    def metadata(self, uploaded_file):

        st.subheader("File Details")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Filename:** {uploaded_file.name}"
            )

            st.write(
                f"**Extension:** {Path(uploaded_file.name).suffix}"
            )

        with col2:

            st.write(
                f"**Size:** {uploaded_file.size / (1024 * 1024):.2f} MB"
            )

    def start(self, uploaded_file):

        valid, message = self.validator.validate(uploaded_file)

        if not valid:
            st.error(message)
            return

        st.session_state.workflow_running = True
        st.session_state.workflow_progress = 0
        st.session_state.current_agent = "Upload Agent"

        progress = st.progress(0)
        status = st.empty()

        try:

            status.info("Starting workflow...")

            context = {
                "uploaded_file": uploaded_file,

                "provider_name": st.session_state.get("provider_name"),
                "model_name": st.session_state.get("model_name"),

                "analysis_type": st.session_state.get(
                    "analysis_type",
                    "general",
                ),

                "analysis_prompt": st.session_state.get(
                    "analysis_prompt",
                    "Generate a comprehensive analysis of this transcript.",
                ),

                "progress_bar": progress,
                "status_text": status,

                "workflow_log": [],
                "status": "pending",
                "started_at": datetime.utcnow().isoformat(),
                "expected_agents": 7,
            }

            result = self.orchestrator.run(context)

            if result.get("status") == "failed":
                st.session_state.workflow_running = False
                st.session_state.current_agent = "Failed"
                st.session_state.workflow_progress = 0

                progress.progress(0)

                status.error(result.get("error", "Workflow failed."))

                st.error(result.get("error", "Workflow failed."))

                return

            # Success
            st.session_state.workflow_progress = 100
            progress.progress(100)

            st.session_state.workflow_running = False
            st.session_state.current_agent = "Completed"

            st.session_state.last_result = result

            status.success("Workflow completed successfully.")
            st.success("Analysis finished.")

            st.session_state.last_result = result

            video_info = result.get("video_metadata", {})

            history = st.session_state.get(
                "video_history",
                [],
            )

            history.append(
                {
                    "name": video_info.get(
                        "filename",
                        uploaded_file.name,
                    ),
                    "path": result.get(
                        "video",
                        "",
                    ),
                    "status": "Completed",
                }
            )

            st.session_state.video_history = history

            status.success(
                "Workflow completed successfully."
            )

            st.success("Analysis finished.")

        except Exception as exc:

            progress.progress(0)

            status.error(
                f"❌ {exc}"
            )

            st.error(
                f"Video already uploaded.\n\n{exc}"
            )

            st.session_state.workflow_running = False

            return