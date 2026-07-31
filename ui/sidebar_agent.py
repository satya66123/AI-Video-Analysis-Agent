"""
sidebar_agent.py

Sidebar Agent

Responsibilities
----------------
- Render sidebar
- Navigation
- Provider selection
- Model selection
- Quick actions
"""

from __future__ import annotations

import streamlit as st

from providers.model_manager import ModelManager
from providers.provider_factory import ProviderFactory
from .navigation_agent import NavigationAgent


class SidebarAgent:

    @classmethod
    def render(cls):

        with st.sidebar:

            st.title("🎥 AI Video Analyzer")

            st.divider()

            page = NavigationAgent.sidebar_navigation()

            st.divider()

            st.subheader("AI")

            provider_name = st.sidebar.selectbox(
                "Provider",
                [
                    "Ollama",
                    "OpenAI",
                    "Anthropic"
                ]
            )

            provider = ProviderFactory.get_provider(
                provider_name
            )

            models = ModelManager.get_models(
                provider_name
            )

            selected_model = st.sidebar.selectbox(
                "Model",
                models
            )

            st.session_state["provider_name"] = provider_name
            st.session_state["model_name"] = selected_model

            if provider.health_check():
                st.sidebar.success("Provider Connected")
            else:
                st.sidebar.error("Provider Not Available")

            st.divider()

            st.subheader("Workflow")

            st.metric(
                "Progress",
                f"{st.session_state.workflow_progress}%",
            )

            st.write(
                f"Current Agent: "
                f"{st.session_state.current_agent}"
            )

            st.divider()

            if st.button(
                "🧹 Clear Session",
                use_container_width=True,
            ):

                st.session_state.clear()

                st.rerun()

            return page