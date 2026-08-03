import streamlit as st

from app_agent_home import (
    AppAgent,
    initialize_defaults,
)

def test_initialize_defaults():

    st.session_state.clear()

    initialize_defaults()

    assert st.session_state["provider"] == "Ollama"

    assert st.session_state["model"] == "qwen2.5:1.5b"

    assert st.session_state["current_page"] == "Dashboard"

def test_initialize_defaults_existing_values():

    st.session_state.clear()

    st.session_state["provider"] = "OpenAI"

    initialize_defaults()

    assert st.session_state["provider"] == "OpenAI"

def test_appagent_init():

    st.session_state.clear()

    app = AppAgent()

    assert app.orchestrator is not None

    assert "Dashboard" in app.pages

    assert "Home" in app.pages

    assert "History" in app.pages

    assert "Settings" in app.pages

    assert "About" in app.pages

def test_render_dashboard(
    monkeypatch,
):

    app = AppAgent()

    monkeypatch.setattr(
        "app_agent_home.SidebarAgent.render",
        lambda: None,
    )

    monkeypatch.setattr(
        "app_agent_home.NavigationAgent.current_page",
        lambda: "Dashboard",
    )

    called = []

    monkeypatch.setattr(
        app.pages["Dashboard"],
        "render",
        lambda: called.append(True),
    )

    app.render()

    assert len(called) == 1

def test_render_home(
    monkeypatch,
):

    app = AppAgent()

    monkeypatch.setattr(
        "app_agent_home.SidebarAgent.render",
        lambda: None,
    )

    monkeypatch.setattr(
        "app_agent_home.NavigationAgent.current_page",
        lambda: "Home",
    )

    called = []

    monkeypatch.setattr(
        app.pages["Home"],
        "render",
        lambda: called.append(True),
    )

    app.render()

    assert len(called) == 1

def test_render_unknown_page(
    monkeypatch,
):

    app = AppAgent()

    monkeypatch.setattr(
        "app_agent_home.SidebarAgent.render",
        lambda: None,
    )

    monkeypatch.setattr(
        "app_agent_home.NavigationAgent.current_page",
        lambda: "XYZ",
    )

    errors = []

    monkeypatch.setattr(
        st,
        "error",
        lambda msg: errors.append(msg),
    )

    app.render()

    assert len(errors) == 1

def test_pages_count():

    app = AppAgent()

    assert len(app.pages) == 5

def test_orchestrator_saved_in_session():

    st.session_state.clear()

    app = AppAgent()

    assert "orchestrator" in st.session_state

    assert app.orchestrator is st.session_state["orchestrator"]
