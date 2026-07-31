import streamlit as st

from providers.provider_factory import ProviderFactory
from providers.model_manager import ModelManager


def show_sidebar():

    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Video Upload",
            "Audio Processing",
            "Speech-to-Text",
            "AI Analysis",
            "AI Chat",
            "Reports",
            "About"
        ]
    )

    st.sidebar.title("⚙ AI Settings")

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


    st.session_state["provider"] = provider_name
    st.session_state["model"] = selected_model

    if provider.health_check():
        st.sidebar.success("Provider Connected")
    else:
        st.sidebar.error("Provider Not Available")

    return page, provider_name, selected_model