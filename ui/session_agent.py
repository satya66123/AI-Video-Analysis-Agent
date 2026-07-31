"""
session_agent.py

Session Agent

Responsibilities
----------------
- Initialize Streamlit session state
- Store current workflow data
- Manage selected video
- Manage transcript
- Manage reports
- Manage exports
- Manage chat history
"""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st


class SessionAgent:

    DEFAULTS = {

        "current_page": "Dashboard",

        "video": None,

        "audio": None,

        "transcript": None,

        "analysis": None,

        "report": None,

        "exports": [],

        "chat_messages": [],

        "workflow_running": False,

        "workflow_progress": 0,

        "current_agent": "",

        "provider": "Ollama",

        "model": "qwen2.5:1.5b",

        "temperature": 0.3,

        "max_tokens": 2048,

        "theme": "Dark",

        "notifications": []
    }

    @classmethod
    def initialize(cls):

        for key, value in cls.DEFAULTS.items():

            if key not in st.session_state:

                st.session_state[key] = value

    @classmethod
    def get(cls, key: str, default=None):

        return st.session_state.get(
            key,
            default,
        )

    @classmethod
    def set(cls, key: str, value: Any):

        st.session_state[key] = value

    @classmethod
    def update(cls, values: Dict[str, Any]):

        for key, value in values.items():

            st.session_state[key] = value

    @classmethod
    def exists(cls, key: str):

        return key in st.session_state

    @classmethod
    def remove(cls, key: str):

        if key in st.session_state:

            del st.session_state[key]

    @classmethod
    def clear_chat(cls):

        st.session_state.chat_messages = []

    @classmethod
    def clear_workflow(cls):

        st.session_state.video = None

        st.session_state.audio = None

        st.session_state.transcript = None

        st.session_state.analysis = None

        st.session_state.report = None

        st.session_state.exports = []

        st.session_state.workflow_progress = 0

        st.session_state.workflow_running = False

        st.session_state.current_agent = ""

    @classmethod
    def reset(cls):

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        cls.initialize()