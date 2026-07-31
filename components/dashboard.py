import streamlit as st

from components.dashboard_cards import show_dashboard_cards


def show_dashboard():

    st.header("📊 Dashboard")

    show_dashboard_cards()

    st.divider()

    st.info("Project Overview")