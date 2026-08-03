import streamlit as st

from ui.navigation_agent2 import NavigationAgent


####################################################
# Current Page Default
####################################################

def test_current_page_default():

    st.session_state.clear()

    assert (
        NavigationAgent.current_page()
        == "Dashboard"
    )


####################################################
# Current Page Existing
####################################################

def test_current_page_existing():

    st.session_state.clear()

    st.session_state["current_page"] = "History"

    assert (
        NavigationAgent.current_page()
        == "History"
    )


####################################################
# Navigate
####################################################

def test_navigate():

    st.session_state.clear()

    NavigationAgent.navigate(
        "Settings"
    )

    assert (
        st.session_state["current_page"]
        == "Settings"
    )


####################################################
# Sidebar Navigation
####################################################

def test_sidebar_navigation(
    monkeypatch,
):

    st.session_state.clear()

    st.session_state["current_page"] = "Dashboard"

    monkeypatch.setattr(
        st.sidebar,
        "radio",
        lambda *args, **kwargs: "Home",
    )

    page = NavigationAgent.sidebar_navigation()

    assert page == "Home"

    assert (
        st.session_state["current_page"]
        == "Home"
    )


####################################################
# Next Page
####################################################

def test_next_page():

    st.session_state.clear()

    st.session_state["current_page"] = "Dashboard"

    NavigationAgent.next_page()

    assert (
        st.session_state["current_page"]
        == "Home"
    )


####################################################
# Next Page At End
####################################################

def test_next_page_last():

    st.session_state.clear()

    st.session_state["current_page"] = "About"

    NavigationAgent.next_page()

    assert (
        st.session_state["current_page"]
        == "About"
    )


####################################################
# Previous Page
####################################################

def test_previous_page():

    st.session_state.clear()

    st.session_state["current_page"] = "History"

    NavigationAgent.previous_page()

    assert (
        st.session_state["current_page"]
        == "Home"
    )


####################################################
# Previous Page At Beginning
####################################################

def test_previous_page_first():

    st.session_state.clear()

    st.session_state["current_page"] = "Dashboard"

    NavigationAgent.previous_page()

    assert (
        st.session_state["current_page"]
        == "Dashboard"
    )


####################################################
# Is Page True
####################################################

def test_is_page_true():

    st.session_state.clear()

    st.session_state["current_page"] = "Settings"

    assert NavigationAgent.is_page(
        "Settings"
    )


####################################################
# Is Page False
####################################################

def test_is_page_false():

    st.session_state.clear()

    st.session_state["current_page"] = "Dashboard"

    assert not NavigationAgent.is_page(
        "History"
    )