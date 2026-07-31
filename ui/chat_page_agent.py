"""
chat_page_agent.py

Chat Page Agent

Responsibilities
----------------
- Browse transcripts folder
- Select transcript
- Load transcript
- Load chat history
- Chat with AI
- Save/Delete/Clear chats
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from services.speech_agent_service import SpeechService
from services.ai_chat_agent_service import AIChatService

from .header_agent import HeaderAgent
from .footer_agent import FooterAgent


class ChatPageAgent:

    def __init__(self):

        self.chat_service = AIChatService()

    def render(self):

        HeaderAgent.render("💬 AI Chat")

        orchestrator = st.session_state.get(
            "orchestrator"
        )

        if orchestrator is None:

            st.error(
                "AI Orchestrator is unavailable."
            )

            FooterAgent.render()

            return

        ####################################################
        # Transcript Selection
        ####################################################

        transcripts = SpeechService.list_transcripts()

        if not transcripts:

            st.warning(
                "No transcripts found. Please analyze a video first."
            )

            FooterAgent.render()

            return

        transcript_names = [
            item["name"]
            for item in transcripts
        ]

        selected_transcript = st.selectbox(
            "Select Transcript",
            transcript_names,
        )

        transcript = SpeechService.load_transcript(
            selected_transcript
        )

        ####################################################
        # Provider
        ####################################################

        provider_name = st.session_state.get(
            "provider_name"
        )

        model_name = st.session_state.get(
            "model_name"
        )

        if not provider_name:

            st.warning(
                "Please select an AI provider."
            )

            FooterAgent.render()

            return

        if not model_name:

            st.warning(
                "Please select an AI model."
            )

            FooterAgent.render()

            return

        ####################################################
        # Chat File
        ####################################################

        video_name = Path(
            selected_transcript
        ).stem

        chat_filename = (
            f"{video_name}_chat.json"
        )

        history = self.chat_service.load_chat(
            chat_filename
        )

        ####################################################
        # Toolbar
        ####################################################

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "🔄 Reload",
                use_container_width=True,
            ):

                st.rerun()

        with col2:

            if st.button(
                "🧹 Clear Chat",
                use_container_width=True,
            ):

                history = []

                self.chat_service.save_chat(
                    chat_filename,
                    history,
                )

                st.success(
                    "Chat cleared."
                )

                st.rerun()

        with col3:

            if st.button(
                "🗑 Delete Chat",
                use_container_width=True,
            ):

                self.chat_service.delete_chat(
                    chat_filename
                )

                st.success(
                    "Chat deleted."
                )

                st.rerun()

        st.divider()

        ####################################################
        # Conversation
        ####################################################

        if history:

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

        else:

            st.info(
                "Start chatting with the selected transcript."
            )

        ####################################################
        # Chat Input
        ####################################################

        prompt = st.chat_input(
            "Ask about the transcript..."
        )

        if not prompt:
            FooterAgent.render()
            return

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.spinner(
            "Thinking..."
        ):
            context = {
                "transcript": transcript,
                "question": prompt,
                "provider_name": provider_name,
                "model_name": model_name,
                "chat_history": history,
                "video": video_name,
            }

            try:

                result = orchestrator.run_chat(
                    context
                )

                answer = result.get(
                    "chat_answer",
                    "No response generated."
                )

                history = result.get(
                    "chat_history",
                    history,
                )

            except Exception as e:

                answer = f"Error: {e}"

            ####################################################
            # Show Response
            ####################################################

        with st.chat_message(
                "assistant"
        ):

            st.markdown(
                answer
            )

            ####################################################
            # Save Chat
            ####################################################

        self.chat_service.save_chat(
            chat_filename,
            history,
        )

        st.success(
            "Chat saved successfully."
        )

        ####################################################
        # Chat Information
        ####################################################

        st.divider()

        with st.expander(
                "ℹ Chat Information",
                expanded=False,
        ):

            st.write(
                f"**Transcript:** {selected_transcript}"
            )

            st.write(
                f"**Provider:** {provider_name}"
            )

            st.write(
                f"**Model:** {model_name}"
            )

            st.write(
                f"**Messages:** {len(history)}"
            )

            st.write(
                f"**Chat File:** {chat_filename}"
            )

        ####################################################
        # Footer
        ####################################################

        FooterAgent.render()