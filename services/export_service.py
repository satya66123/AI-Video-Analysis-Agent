from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime





class ExportService:

    EXPORT_FOLDER = Path("exports")

    @classmethod
    def create_export_folder(cls):
        cls.EXPORT_FOLDER.mkdir(exist_ok=True)

    @classmethod
    def save_txt(cls, filename, report):

        cls.create_export_folder()

        path = cls.EXPORT_FOLDER / f"{filename}.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(report)

        return path

    @classmethod
    def save_md(cls, filename, report):

        cls.create_export_folder()

        path = cls.EXPORT_FOLDER / f"{filename}.md"

        with open(path, "w", encoding="utf-8") as f:
            f.write(report)

        return path

    @classmethod
    def save_html(cls, filename, report):

        cls.create_export_folder()

        path = cls.EXPORT_FOLDER / f"{filename}.html"

        html = f"""
        <html>
        <head>
            <title>AI Video Analyzer Report</title>
        </head>
        <body>
        <pre>
{report}
        </pre>
        </body>
        </html>
        """

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

        return path

    @classmethod
    def save_pdf(cls, filename, report):

        cls.create_export_folder()

        path = cls.EXPORT_FOLDER / f"{filename}.pdf"

        doc = SimpleDocTemplate(str(path))

        styles = getSampleStyleSheet()

        story = []

        for line in report.split("\n"):

            story.append(
                Paragraph(line.replace(" ", "&nbsp;"), styles["BodyText"])
            )

        doc.build(story)

        return path


    @classmethod
    def generate_filename(cls, video_name: str):
        video_name = Path(video_name).stem

        video_name = video_name.replace(" ", "_")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        return f"{video_name}_video_report_{timestamp}"