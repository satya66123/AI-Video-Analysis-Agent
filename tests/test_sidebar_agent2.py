import streamlit as st

from ui.sidebar_agent2 import SidebarAgent


####################################################
# Render Success
####################################################

def test_render(
    monkeypatch,
):

    st.session_state.clear()

    st.session_state["workflow_progress"] = 50

    st.session_state["current_agent"] = "Video Agent"

    ##################################################

    class DummyProvider:

        def health_check(self):
            return True

    monkeypatch.setattr(
        "ui.sidebar_agent2.ProviderFactory.get_provider",
        lambda name: DummyProvider(),
    )

    monkeypatch.setattr(
        "ui.sidebar_agent2.ModelManager.get_models",
        lambda provider: [
            "model1",
            "model2",
        ],
    )

    monkeypatch.setattr(
        "ui.sidebar_agent2.NavigationAgent.sidebar_navigation",
        lambda: "Dashboard",
    )

    monkeypatch.setattr(
        st.sidebar,
        "selectbox",
        lambda label, options: options[0],
    )

    monkeypatch.setattr(
        st.sidebar,
        "success",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st.sidebar,
        "error",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "title",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "divider",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "metric",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "write",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "button",
        lambda *args, **kwargs: False,
    )

    SidebarAgent.render()

    assert st.session_state["provider_name"] == "Ollama"

    assert st.session_state["provider"] == "Ollama"

    assert st.session_state["model_name"] == "model1"

    assert st.session_state["model"] == "model1"


####################################################
# Provider Health Check Failed
####################################################

def test_provider_not_available(
    monkeypatch,
):

    st.session_state.clear()

    st.session_state["workflow_progress"] = 0

    st.session_state["current_agent"] = "Idle"

    class DummyProvider:

        def health_check(self):
            return False

    monkeypatch.setattr(
        "ui.sidebar_agent2.ProviderFactory.get_provider",
        lambda name: DummyProvider(),
    )

    monkeypatch.setattr(
        "ui.sidebar_agent2.ModelManager.get_models",
        lambda provider: ["model1"],
    )

    monkeypatch.setattr(
        "ui.sidebar_agent2.NavigationAgent.sidebar_navigation",
        lambda: "Dashboard",
    )

    monkeypatch.setattr(
        st.sidebar,
        "selectbox",
        lambda label, options: options[0],
    )

    monkeypatch.setattr(
        st.sidebar,
        "success",
        lambda *args, **kwargs: None,
    )

    errors = []

    monkeypatch.setattr(
        st.sidebar,
        "error",
        lambda msg: errors.append(msg),
    )

    monkeypatch.setattr(
        st,
        "title",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "divider",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "metric",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "write",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "button",
        lambda *args, **kwargs: False,
    )

    SidebarAgent.render()

    assert len(errors) == 1


####################################################
# Clear Session
####################################################

def test_clear_session(
    monkeypatch,
):

    st.session_state.clear()

    st.session_state["workflow_progress"] = 0

    st.session_state["current_agent"] = "Idle"

    class DummyProvider:

        def health_check(self):
            return True

    monkeypatch.setattr(
        "ui.sidebar_agent2.ProviderFactory.get_provider",
        lambda name: DummyProvider(),
    )

    monkeypatch.setattr(
        "ui.sidebar_agent2.ModelManager.get_models",
        lambda provider: ["model1"],
    )

    monkeypatch.setattr(
        "ui.sidebar_agent2.NavigationAgent.sidebar_navigation",
        lambda: "Dashboard",
    )

    monkeypatch.setattr(
        st.sidebar,
        "selectbox",
        lambda label, options: options[0],
    )

    monkeypatch.setattr(
        st.sidebar,
        "success",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st.sidebar,
        "error",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "title",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "divider",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "metric",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "write",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "button",
        lambda *args, **kwargs: True,
    )

    rerun_called = []

    monkeypatch.setattr(
        st,
        "rerun",
        lambda: rerun_called.append(True),
    )

    SidebarAgent.render()

    assert len(st.session_state) == 0

    assert len(rerun_called) == 1