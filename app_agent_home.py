"""
app.py

AI Video Analysis Agent
Main Streamlit Application
"""

from __future__ import annotations

import streamlit as st

from agents.ai_orchestrator import AIOrchestrator
from ui.dashboard_page_agent import DashboardPageAgent

from ui.session_agent import SessionAgent
from ui.theme_agent import ThemeAgent
from ui.sidebar_agent2 import SidebarAgent
from ui.navigation_agent2 import NavigationAgent

from ui.home_assistant_page_agent import HomeAssistantPageAgent
from ui.history_page_agent import HistoryPageAgent
from ui.settings_page_agent import SettingsPageAgent
from ui.about_page_agent import AboutPageAgent


APP_TITLE = "AI Video Analysis Agent"
VERSION = "1.0.0"


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)


class AppAgent:

    def __init__(self):

        SessionAgent.initialize()

        from services.video_agent_service import VideoService
        from services.audio_agent_service import AudioService
        from services.speech_agent_service import SpeechService
        from services.ai_analysis_agent_service import AIAnalysisService
        from services.report_agent_service import ReportService
        from services.export_agent_service import ExportService
        from services.ai_chat_agent_service import AIChatService

        if "orchestrator" not in st.session_state:
            st.session_state.orchestrator = AIOrchestrator(
                video_service=VideoService(),
                audio_service=AudioService(),
                speech_service=SpeechService(),
                analysis_service=AIAnalysisService(),
                report_service=ReportService(),
                export_service=ExportService(),
                chat_service=AIChatService(),
            )

        ThemeAgent.apply()

        self.orchestrator = st.session_state.orchestrator

        self.pages = {
            "Dashboard": DashboardPageAgent(),
            "Home": HomeAssistantPageAgent(),
            "History": HistoryPageAgent(),
            "Settings": SettingsPageAgent(),
            "About": AboutPageAgent(),

        }

    def render(self):

        SidebarAgent.render()

        page = NavigationAgent.current_page()

        page_agent = self.pages.get(page)

        if page_agent is None:

            st.error(
                f"Unknown page: {page}"
            )

            return

        page_agent.render()


def initialize_defaults():

    defaults = {

        "provider": "Ollama",

        "model": "qwen2.5:1.5b",

        "temperature": 0.7,

        "max_tokens": 2048,

        "workflow_progress": 0,

        "workflow_running": False,

        "current_agent": "Idle",

        "video_history": [],

        "report_history": [],

        "chat_history": [],

        "export_history": [],

        "notifications": [],

        "transcript": "",

        "analysis": {},

        "report": "",

        "exports": {},

        "last_result": None,

        "current_page": "Dashboard",

    }

    for key, value in defaults.items():

        st.session_state.setdefault(
            key,
            value,
        )


def main():

    initialize_defaults()

    app = AppAgent()

    app.render()


if __name__ == "__main__":

    main()