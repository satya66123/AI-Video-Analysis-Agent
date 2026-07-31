"""
settings_page_agent.py
"""

from __future__ import annotations

import streamlit as st

from .header_agent import HeaderAgent
from .footer_agent import FooterAgent


class SettingsPageAgent:

    def render(self):

        HeaderAgent.render("⚙ Settings")

        st.subheader("AI Provider")

        provider = st.selectbox(
            "Provider",
            [
                "Ollama",
                "OpenAI",
                "Anthropic",
            ],
            index=[
                "Ollama",
                "OpenAI",
                "Anthropic",
            ].index(
                st.session_state.get(
                    "provider",
                    "Ollama",
                )
            ),
        )

        st.session_state.provider = provider

        st.subheader("Model")

        model = st.text_input(
            "Model",
            value=st.session_state.get(
                "model",
                "qwen2.5:1.5b",
            ),
        )

        st.session_state.model = model

        st.subheader("Generation")

        temperature = st.slider(
            "Temperature",
            0.0,
            2.0,
            float(
                st.session_state.get(
                    "temperature",
                    0.7,
                )
            ),
            0.1,
        )

        max_tokens = st.slider(
            "Max Tokens",
            128,
            8192,
            int(
                st.session_state.get(
                    "max_tokens",
                    2048,
                )
            ),
            128,
        )

        st.session_state.temperature = temperature
        st.session_state.max_tokens = max_tokens

        st.subheader("Application")

        auto_save = st.checkbox(
            "Auto Save Results",
            value=st.session_state.get(
                "auto_save",
                True,
            ),
        )

        dark_mode = st.checkbox(
            "Dark Mode",
            value=st.session_state.get(
                "dark_mode",
                True,
            ),
        )

        st.session_state.auto_save = auto_save
        st.session_state.dark_mode = dark_mode

        st.success(
            "Settings saved."
        )

        FooterAgent.render()