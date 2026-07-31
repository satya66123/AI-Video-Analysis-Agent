"""
theme_agent.py

Theme Agent

Responsibilities
----------------
- Manage application themes
- Apply custom CSS
- Handle theme switching
- Provide color palette
"""

from __future__ import annotations

import streamlit as st


class ThemeAgent:

    THEMES = {

        "Dark": {

            "background": "#0E1117",

            "secondary": "#1E1E1E",

            "primary": "#00C8FF",

            "text": "#FFFFFF",

            "success": "#00CC66",

            "warning": "#FFC107",

            "danger": "#FF4B4B",
        },

        "Light": {

            "background": "#FFFFFF",

            "secondary": "#F5F5F5",

            "primary": "#1976D2",

            "text": "#000000",

            "success": "#4CAF50",

            "warning": "#FF9800",

            "danger": "#F44336",
        }

    }

    @classmethod
    def available_themes(cls):

        return list(cls.THEMES.keys())

    @classmethod
    def get_theme(cls, name="Dark"):

        return cls.THEMES.get(
            name,
            cls.THEMES["Dark"],
        )

    @classmethod
    def apply(cls, name="Dark"):

        theme = cls.get_theme(name)

        css = f"""
        <style>

        .stApp{{
            background:{theme['background']};
            color:{theme['text']};
        }}

        section[data-testid="stSidebar"]{{
            background:{theme['secondary']};
        }}

        .block-container{{
            padding-top:1rem;
            padding-bottom:2rem;
        }}

        .main-title{{
            font-size:34px;
            font-weight:bold;
            color:{theme['primary']};
        }}

        .section-title{{
            font-size:24px;
            font-weight:600;
            margin-top:15px;
            color:{theme['primary']};
        }}

        .card{{
            background:{theme['secondary']};
            padding:15px;
            border-radius:10px;
            margin-bottom:10px;
            border:1px solid #444;
        }}

        .success-box{{
            padding:10px;
            border-radius:8px;
            background:{theme['success']};
            color:white;
        }}

        .warning-box{{
            padding:10px;
            border-radius:8px;
            background:{theme['warning']};
            color:black;
        }}

        .danger-box{{
            padding:10px;
            border-radius:8px;
            background:{theme['danger']};
            color:white;
        }}

        

        </style>
        """

        st.markdown(
            css,
            unsafe_allow_html=True,
        )

    @classmethod
    def title(cls, text):

        st.markdown(
            f'<div class="main-title">{text}</div>',
            unsafe_allow_html=True,
        )

    @classmethod
    def heading(cls, text):

        st.markdown(
            f'<div class="section-title">{text}</div>',
            unsafe_allow_html=True,
        )

    @classmethod
    def card(cls, title, body):

        st.markdown(
            f"""
            <div class="card">
                <h4>{title}</h4>
                <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )