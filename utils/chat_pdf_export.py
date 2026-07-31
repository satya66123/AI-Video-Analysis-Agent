import os
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


class ChatPDFExport:

    @staticmethod
    def export(
            history,
        transcript_name,
        provider,
        model,
        filename,
    ):

        os.makedirs("exports", exist_ok=True)

        path = os.path.join(
            "exports",
            filename + ".pdf",
        )

        doc = SimpleDocTemplate(path)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph("<b>AI Video Analyzer</b>", styles["Title"])
        )

        story.append(
            Paragraph(
                f"Generated: {datetime.now()}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Transcript: {transcript_name}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Provider: {provider}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                f"Model: {model}",
                styles["Normal"],
            )
        )

        story.append(
            Paragraph("<br/>", styles["Normal"])
        )

        for index, chat in enumerate(history, start=1):

            story.append(
                Paragraph(
                    f"<b>User {index}</b>",
                    styles["Heading2"],
                )
            )

            story.append(
                Paragraph(
                    chat["user"],
                    styles["BodyText"],
                )
            )

            story.append(
                Paragraph(
                    f"<b>Assistant {index}</b>",
                    styles["Heading2"],
                )
            )

            story.append(
                Paragraph(
                    chat["assistant"],
                    styles["BodyText"],
                )
            )

            story.append(
                Paragraph("<br/>", styles["BodyText"])
            )

        doc.build(story)

        return path