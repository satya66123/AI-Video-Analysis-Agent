"""
Reusable File Browser Component
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import streamlit as st


def show_file_browser(
    folder: str,
    extension: Optional[str] = None,
    key: str = "",
) -> Optional[Path]:
    """
    Display files from a folder and return the selected file.

    Parameters
    ----------
    folder : str
    extension : str | None
    key : str

    Returns
    -------
    Path | None
    """

    directory = Path(folder)

    if not directory.exists():
        st.info(f"{folder} folder not found.")
        return None

    if extension:
        files = sorted(directory.glob(f"*{extension}"))
    else:
        files = sorted(directory.iterdir())

    if not files:
        st.info("No files available.")
        return None

    selected = st.selectbox(
        "Select File",
        files,
        format_func=lambda x: x.name,
        key=key,
    )

    return selected