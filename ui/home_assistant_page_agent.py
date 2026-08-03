from pathlib import Path

from agents.integrated_analysis_agent import (
    IntegratedAnalysisAgent,
)
from services.report_agent_service import ReportService

from services.video_service import VideoService
from services.ai_chat_agent_service  import AIChatService
from ui.footer_agent import FooterAgent
from ui.header_agent import HeaderAgent
import streamlit as st



class HomeAssistantPageAgent:

    def __init__(self):

        self.video_service = VideoService()

        self.chat_service = AIChatService()

        self.integrated_agent = (
            IntegratedAnalysisAgent()
        )

    def render(self):
        HeaderAgent.render(
            "🎥 AI Video Analysis Assistant"
        )

        self.video_section()

        st.divider()

        self.chat_section()

        st.divider()

        self.end_chat_section()

        st.divider()

        self.session_information()

        FooterAgent.render()

    def session_information(self):

        st.divider()

        st.subheader("📋 Session Information")

        if not st.session_state.get(
                "assistant_ready",
                False,
        ):
            st.info(
                "No video has been loaded."
            )

            return

        video = st.session_state.get(
            "assistant_video",
            "-"
        )

        video_metadata = st.session_state.get(
            "assistant_video_metadata",
            {}
        )

        audio_metadata = st.session_state.get(
            "assistant_audio_metadata",
            {}
        )

        transcript = st.session_state.get(
            "assistant_transcript",
            ""
        )

        analysis = st.session_state.get(
            "assistant_analysis",
            ""
        )

        chats = st.session_state.get(
            "assistant_chat_sessions",
            []
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**🎥 Video:** {video}"
            )

            st.write(
                f"**Duration:** {video_metadata.get('duration', '-')}"
            )

            st.write(
                f"**Resolution:** {video_metadata.get('resolution', '-')}"
            )

            st.write(
                f"**Size:** {video_metadata.get('size', '-')}"
            )

            st.write(
                f"**Audio Duration:** {audio_metadata.get('duration', '-')}"
            )

        with col2:

            st.write(
                f"**Transcript:** {'Loaded' if transcript else 'Not Loaded'}"
            )

            st.write(
                f"**Analysis:** {'Loaded' if analysis else 'Not Loaded'}"
            )

            st.write(
                f"**Chat Sessions:** {len(chats)}"
            )

            st.write(

                f"**Current Chat:** "

                f"{st.session_state.get('assistant_chat_id', 'New Chat')}"

            )

            st.write(
                f"**Provider:** {st.session_state.get('provider_name', '-')}"
            )

            st.write(
                f"**Model:** {st.session_state.get('model_name', '-')}"
            )

        st.success(
            "✅ Home Assistant is ready."
        )

        if st.button(
                "🔄 Reset Session",
                use_container_width=True,
        ):

            keys = [

                "assistant_ready",
                "assistant_video",
                "assistant_video_metadata",
                "assistant_audio_metadata",
                "assistant_transcript",
                "assistant_analysis",
                "assistant_chat_sessions",
                "assistant_history",
                "assistant_chat_id",

            ]

            for key in keys:
                st.session_state.pop(
                    key,
                    None,
                )

            st.rerun()

    def video_section(self):

        st.subheader("🎥 Video")

        ####################################################
        # Upload New Video
        ####################################################

        uploaded_file = st.file_uploader(
            "Upload New Video",
            type=[
                "mp4",
                "avi",
                "mov",
                "mkv",
                "webm",
            ],
            key="assistant_upload",
        )

        if uploaded_file is not None:

            if st.button(
                    "🚀 Process New Video",
                    type="primary",
                    use_container_width=True,
            ):

                progress = st.progress(0)

                status = st.empty()

                with st.spinner(
                        "Processing video..."
                ):

                    ################################################
                    # Duplicate Detection
                    ################################################

                    if self.video_service.is_duplicate(
                            uploaded_file
                    ):
                        st.warning(
                            "This video already exists."
                        )

                        st.info(
                            "Please select it from Existing Videos."
                        )

                        return

                    ################################################
                    # Standard Workflow
                    ################################################

                    context = {

                        "uploaded_file": uploaded_file,

                        "provider_name":
                            st.session_state.get(
                                "provider_name"
                            ),

                        "model_name":
                            st.session_state.get(
                                "model_name"
                            ),

                        "analysis_type":
                            st.session_state.get(
                                "analysis_type",
                                "general",
                            ),

                        "analysis_prompt":
                            st.session_state.get(
                                "analysis_prompt",
                                "Generate a comprehensive analysis.",
                            ),

                        "progress_bar":
                            progress,

                        "status_text":
                            status,

                        "workflow_log": [],

                        "status": "pending",

                    }

                    result = st.session_state.orchestrator.run(
                        context
                    )

                    ################################################
                    # Workflow Failed
                    ################################################

                    if result.get(
                            "status"
                    ) != "completed":
                        st.error(
                            result.get(
                                "error",
                                "Workflow failed.",
                            )
                        )

                        return

                    ################################################
                    # Load Newly Generated Video
                    ################################################

                    video_path = result.get(
                        "video"
                    )

                    if not video_path:
                        st.error(
                            "Workflow completed but no saved video was returned."
                        )

                        return

                    video_name = Path(
                        video_path
                    ).name

                    self.integrated_agent.load_existing_video(
                        video_name
                    )

                    ################################################
                    # Initialize Chat Session
                    ################################################

                    st.session_state[
                        "assistant_chat_id"
                    ] = None

                    st.session_state[
                        "assistant_history"
                    ] = []

                    st.success(
                        "Video processed successfully."
                    )

                    st.rerun()

        ####################################################
        # Existing Videos
        ####################################################

        st.divider()

        st.subheader(
            "📂 Existing Videos"
        )

        videos = self.video_service.list_videos()

        if not videos:
            st.info(
                "No existing videos found."
            )

            return

        selected_video = st.selectbox(
            "Select Existing Video",
            videos,
            key="assistant_selected_video",
        )

        if st.button(
                "📂 Load Existing Video",
                use_container_width=True,
        ):
            with st.spinner(
                    "Loading existing video..."
            ):
                self.integrated_agent.load_existing_video(
                    selected_video
                )

            ####################################################
            # Reset Current Chat
            ####################################################

            st.session_state[
                "assistant_chat_id"
            ] = None

            st.session_state[
                "assistant_history"
            ] = []

            st.success(
                "Existing video loaded successfully."
            )

            st.rerun()

    def chat_section(self):

        st.subheader("💬 AI Assistant")

        ####################################################
        # Video Ready?
        ####################################################

        if not st.session_state.get(
                "assistant_ready",
                False,
        ):
            st.info(
                "Load or process a video to start chatting."
            )

            return

        ####################################################
        # Current Video
        ####################################################

        video_name = st.session_state.get(
            "assistant_video"
        )

        ####################################################
        # Refresh Chat List
        ####################################################

        chats = self.chat_service.list_video_chats(
            video_name
        )

        st.session_state[
            "assistant_chat_sessions"
        ] = chats

        ####################################################
        # Existing Chats
        ####################################################

        chat_names = [
            chat.stem
            for chat in chats
        ]

        options = ["➕ New Chat"] + chat_names

        current_chat = st.session_state.get(
            "assistant_chat_id"
        )

        if current_chat in options:
            index = options.index(current_chat)
        else:
            index = 0

        selected_chat = st.selectbox(
            "Select Chat Session",
            options,
            index=index,
        )

        ####################################################
        # Load Existing Chat
        ####################################################

        if selected_chat != "➕ New Chat":

            current_chat = st.session_state.get(
                "assistant_chat_id"
            )

            if current_chat != selected_chat:
                history = self.chat_service.load_chat_by_id(
                    selected_chat
                )

                st.session_state[
                    "assistant_chat_id"
                ] = selected_chat

                st.session_state[
                    "assistant_history"
                ] = history

                st.session_state[
                    "assistant_previous_chat"
                ] = selected_chat

        ####################################################
        # New Chat
        ####################################################

        else:

            ####################################################
            # Initialize Previous Selection
            ####################################################

            if "assistant_previous_chat" not in st.session_state:
                st.session_state[
                    "assistant_previous_chat"
                ] = None

            ####################################################
            # User Switched To New Chat
            ####################################################

            if (
                    st.session_state[
                        "assistant_previous_chat"
                    ] != "➕ New Chat"
            ):
                st.session_state[
                    "assistant_chat_id"
                ] = None

                st.session_state[
                    "assistant_history"
                ] = []

            ####################################################
            # Remember Current Selection
            ####################################################

            st.session_state[
                "assistant_previous_chat"
            ] = "➕ New Chat"

            ####################################################
            # Ensure History Exists
            ####################################################

            if "assistant_history" not in st.session_state:
                st.session_state[
                    "assistant_history"
                ] = []





        ####################################################
        # Current History
        ####################################################

        history = st.session_state.get(
            "assistant_history",
            [],
        )

        ####################################################
        # Display Conversation
        ####################################################

        for message in history:
            with st.chat_message(
                    "user"
            ):
                st.markdown(
                    message.get(
                        "user",
                        "",
                    )
                )

            with st.chat_message(
                    "assistant"
            ):
                st.markdown(
                    message.get(
                        "assistant",
                        "",
                    )
                )
        ####################################################
        # Chat Input
        ####################################################

        question = st.chat_input(
                    "Ask anything about this video..."
                )

        if not question:
                    return

        ####################################################
        # Create Chat On First Message
        ####################################################

        chat_id = st.session_state.get(
                    "assistant_chat_id"
                )

        if chat_id is None:
                    chat_id = self.chat_service.create_chat(
                        video_name
                    )

                    st.session_state[
                        "assistant_chat_id"
                    ] = chat_id

        ####################################################
        # Show User Question
        ####################################################

        with st.chat_message(
                        "user"
                ):

                    st.markdown(
                        question
                    )

        ####################################################
        # Ask AI
        ####################################################

        with st.spinner(
                        "Thinking..."
                ):

                    context = {

                        "transcript":
                            st.session_state.get(
                                "assistant_transcript",
                                "",
                            ),

                        "question":
                            question,

                        "provider_name":
                            st.session_state.get(
                                "provider_name",
                            ),

                        "model_name":
                            st.session_state.get(
                                "model_name",
                            ),

                        "chat_history":
                            history,

                        "video":
                            video_name,

                    }

                    result = st.session_state.orchestrator.run_chat(
                        context
                    )

        ####################################################
        # AI Response
        ####################################################

        answer = result.get(
                    "chat_answer",
                    "No response generated."
                )

        ####################################################
        # Append Message
        ####################################################



        st.session_state[
                    "assistant_history"
                ] = history

        ####################################################
        # Auto Save Current Chat
        ####################################################

        self.chat_service.save_chat_by_id(

                    chat_id,

                    history,

                    status="Open",

                )

        ####################################################
        # Refresh Chat Sessions
        ####################################################

        chats = self.chat_service.list_video_chats(
                    video_name
                )

        st.session_state[
                    "assistant_chat_sessions"
                ] = chats

        ####################################################
        # Display AI Response
        ####################################################

        with st.chat_message(
                        "assistant"
                ):

                    st.markdown(
                        answer
                    )

                    st.rerun()

    def end_chat_section(self):

        ####################################################
        # Video Ready?
        ####################################################

        if not st.session_state.get(
                "assistant_ready",
                False,
        ):
            return

        st.subheader("🏁 Finish Chat")

        history = st.session_state.get(
            "assistant_history",
            [],
        )

        if not history:
            return

        if st.button(
                "🏁 End Chat",
                type="primary",
                use_container_width=True,
        ):

            with st.spinner(
                    "Saving chat and generating report..."
            ):

                ####################################################
                # Current Video
                ####################################################

                video_name = st.session_state.get(
                    "assistant_video"
                )

                ####################################################
                # Current Chat ID
                ####################################################

                chat_id = st.session_state.get(
                    "assistant_chat_id"
                )

                if chat_id is None:
                    chat_id = self.chat_service.create_chat(
                        video_name
                    )

                    st.session_state[
                        "assistant_chat_id"
                    ] = chat_id

                ####################################################
                # Save Chat
                ####################################################

                self.chat_service.save_chat_by_id(
                    chat_id,
                    history,
                    status="Closed",
                )

                ####################################################
                # Generate Report
                ####################################################

                report = ReportService.build_report_from_files(

                    video_metadata=
                    st.session_state.get(
                        "assistant_video_metadata",
                        {},
                    ),

                    audio_metadata=
                    st.session_state.get(
                        "assistant_audio_metadata",
                        {},
                    ),

                    transcript=
                    st.session_state.get(
                        "assistant_transcript",
                        "",
                    ),

                    analysis=
                    st.session_state.get(
                        "assistant_analysis",
                        {},
                    ),

                    chat=
                    history,

                    provider=
                    st.session_state.get(
                        "provider_name",
                        "",
                    ),

                    model=
                    st.session_state.get(
                        "model_name",
                        "",
                    ),

                )

                ####################################################
                # Generate Report Filename
                ####################################################

                filename = ReportService.generate_filename(

                    st.session_state.get(
                        "assistant_video_metadata",
                        {},
                    ).get(
                        "filename",
                        video_name,
                    ),

                    "report",

                )

                ####################################################
                # Save All Report Formats
                ####################################################

                ReportService.save_all_reports(

                    filename=
                    filename,

                    content=
                    report,

                    data={

                        "video_name":
                            st.session_state.get(
                                "assistant_video_metadata",
                                {},
                            ).get(
                                "filename"
                            ),

                        "video_duration":
                            st.session_state.get(
                                "assistant_video_metadata",
                                {},
                            ).get(
                                "duration"
                            ),

                        "video_resolution":
                            st.session_state.get(
                                "assistant_video_metadata",
                                {},
                            ).get(
                                "resolution"
                            ),

                        "video_fps":
                            st.session_state.get(
                                "assistant_video_metadata",
                                {},
                            ).get(
                                "fps"
                            ),

                        "video_format":
                            st.session_state.get(
                                "assistant_video_metadata",
                                {},
                            ).get(
                                "format"
                            ),

                        "video_size":
                            st.session_state.get(
                                "assistant_video_metadata",
                                {},
                            ).get(
                                "size"
                            ),

                        "audio_name":
                            st.session_state.get(
                                "assistant_audio_metadata",
                                {},
                            ).get(
                                "filename"
                            ),

                        "audio_duration":
                            st.session_state.get(
                                "assistant_audio_metadata",
                                {},
                            ).get(
                                "duration"
                            ),

                        "channels":
                            st.session_state.get(
                                "assistant_audio_metadata",
                                {},
                            ).get(
                                "channels"
                            ),

                        "sample_rate":
                            st.session_state.get(
                                "assistant_audio_metadata",
                                {},
                            ).get(
                                "sample_rate"
                            ),

                        "audio_format":
                            st.session_state.get(
                                "assistant_audio_metadata",
                                {},
                            ).get(
                                "format"
                            ),

                        "audio_size":
                            st.session_state.get(
                                "assistant_audio_metadata",
                                {},
                            ).get(
                                "size"
                            ),

                        "transcript":
                            st.session_state.get(
                                "assistant_transcript",
                                "",
                            ),

                        "analysis":
                            st.session_state.get(
                                "assistant_analysis",
                                {},
                            ),

                        "chat":
                            history,

                        "provider":
                            st.session_state.get(
                                "provider_name",
                                "",
                            ),

                        "model":
                            st.session_state.get(
                                "model_name",
                                "",
                            ),

                    },

                )

                ####################################################
                # Refresh Chat Sessions
                ####################################################

                chats = self.chat_service.list_video_chats(
                    video_name
                )

                st.session_state[
                    "assistant_chat_sessions"
                ] = chats

                ####################################################
                # Clear Current Chat
                ####################################################

                st.session_state[
                    "assistant_chat_id"
                ] = None

                st.session_state[
                    "assistant_history"
                ] = []

                ####################################################
                # Success Messages
                ####################################################

                st.success(
                    "✅ Chat saved successfully."
                )

                st.success(
                    "✅ Report generated successfully."
                )

                st.success(
                    "✅ Report exported successfully."
                )

                ####################################################
                # Reload UI
                ####################################################

                st.rerun()