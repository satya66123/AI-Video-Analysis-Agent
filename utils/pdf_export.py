"""
PDF Export Utility
Exports reports as professional PDF documents.
"""

from __future__ import annotations

import os

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


def export_pdf(report: str, filename: str) -> None:
    """
    Export report text to a PDF file.

    Parameters
    ----------
    report : str
        Report content.
    filename : str
        Output PDF filename.
    """

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    document = SimpleDocTemplate(
        filename,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    story.append(Paragraph("AI Video Analyzer Report", title_style))
    story.append(Spacer(1, 0.25 * inch))

    lines = report.splitlines()

    for line in lines:

        text = line.strip()

        if not text:
            story.append(Spacer(1, 0.12 * inch))
            continue

        if text.startswith("# "):
            story.append(
                Paragraph(text.replace("# ", ""), title_style)
            )

        elif text.startswith("## "):
            story.append(
                Paragraph(text.replace("## ", ""), heading_style)
            )

        else:
            story.append(
                Paragraph(text, body_style)
            )

    document.build(story)