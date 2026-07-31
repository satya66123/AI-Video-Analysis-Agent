"""
navigation_agent.py

Navigation Agent

Responsibilities
----------------
- Manage page navigation
- Store current page
- Handle page switching
"""

from __future__ import annotations

import streamlit as st


class NavigationAgent:

    PAGES = [

        "Dashboard",

        "Upload Video",

        "Transcript",

        "Analysis",

        "Report",

        "Export",

        "AI Chat",

        "History",

        "Settings",

        "About",
    ]

    @classmethod
    def current_page(cls):

        return st.session_state.get(
            "current_page",
            "Dashboard",
        )

    @classmethod
    def navigate(cls, page):

        st.session_state.current_page = page

    @classmethod
    def sidebar_navigation(cls):

        page = st.sidebar.radio(

            "Navigation",

            cls.PAGES,

            index=cls.PAGES.index(
                cls.current_page()
            ),

        )

        cls.navigate(page)

        return page

    @classmethod
    def next_page(cls):

        index = cls.PAGES.index(
            cls.current_page()
        )

        if index < len(cls.PAGES) - 1:

            cls.navigate(
                cls.PAGES[index + 1]
            )

    @classmethod
    def previous_page(cls):

        index = cls.PAGES.index(
            cls.current_page()
        )

        if index > 0:

            cls.navigate(
                cls.PAGES[index - 1]
            )

    @classmethod
    def is_page(cls, page):

        return cls.current_page() == page