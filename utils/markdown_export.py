from __future__ import annotations

import os


def export_markdown(report: str, filename: str) -> None:
    """
    Export report as Markdown.
    """

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)