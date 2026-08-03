"""
integrated_analysis_agent.py

Integrated Analysis Agent

Phase 1
-------
Existing Video Workflow

Responsibilities
----------------
- Load video metadata
- Load audio metadata
- Load transcript
- Load analysis
- Load chat history
- Save everything into session state
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from services.video_agent_service import VideoService
from services.audio_agent_service import AudioService
from services.speech_agent_service import SpeechService
from services.ai_analysis_agent_service import AIAnalysisService
from services.ai_chat_agent_service import AIChatService


class IntegratedAnalysisAgent:

    def __init__(self):

        self.video_service = VideoService()
        self.audio_service = AudioService()
        self.analysis_service = AIAnalysisService()
        self.chat_service = AIChatService()

    ########################################################

    def load_existing_video(
        self,
        video_name: str,
    ) -> bool:

        stem = Path(video_name).stem

        ####################################################
        # Video Metadata
        ####################################################

        try:

            video_metadata = (
                self.video_service.load_metadata(
                    video_name
                )
            )

        except Exception:

            video_metadata = {}

        ####################################################
        # Audio Metadata
        ####################################################

        try:

            audio_metadata = self.audio_service.load_metadata(
                stem
            )

            print("AUDIO METADATA:", audio_metadata)

        except Exception as e:

            print("AUDIO ERROR:", e)

            audio_metadata = {}

        ####################################################
        # Transcript
        ####################################################

        try:

            transcript = (
                SpeechService.load_transcript(
                    f"{stem}.txt"
                )
            )

        except Exception:

            transcript = None

        ####################################################
        # Analysis
        ####################################################

        ####################################################
        # Analysis
        ####################################################

        try:

            analysis_file = (
                self.analysis_service.find_latest_analysis(
                    stem
                )
            )

            if analysis_file:

                analysis = (
                    self.analysis_service.load_analysis(
                        analysis_file
                    )
                )

            else:

                analysis = ""

        except Exception as e:

            print(
                "ANALYSIS ERROR:",
                e,
            )

            analysis = ""

        ####################################################
        # Chat History
        ####################################################

        try:

            history = (
                self.chat_service.load_chat(
                    f"{stem}_chat.json"
                )
            )

        except Exception:

            history = []

        ####################################################
        # Transcript Required
        ####################################################

        if transcript is None:

            return False

        ####################################################
        # Save Session
        ####################################################

        st.session_state["assistant_video"] = video_name

        st.session_state["assistant_video_metadata"] = video_metadata

        st.session_state["assistant_audio_metadata"] = audio_metadata

        st.session_state["assistant_transcript"] = transcript

        st.session_state["assistant_analysis"] = analysis

        st.session_state["assistant_history"] = history

        st.session_state["assistant_processed"] = True

        st.session_state["video_loaded"] = True

        st.session_state["assistant_ready"] = True

        return True