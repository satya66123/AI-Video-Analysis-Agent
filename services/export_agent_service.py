from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


class ExportService:
    """
    Responsible only for exporting files.

    Supported formats:
    - txt
    - md
    - html
    - pdf
    - json
    """

    EXPORT_FOLDER = Path("exports")

    FORMAT_FOLDERS = {
        "txt": "txt",
        "md": "markdown",
        "html": "html",
        "pdf": "pdf",
        "json": "json",
    }

    @classmethod
    def ensure_folders(cls) -> None:
        cls.EXPORT_FOLDER.mkdir(exist_ok=True)

        for folder in cls.FORMAT_FOLDERS.values():
            (cls.EXPORT_FOLDER / folder).mkdir(
                parents=True,
                exist_ok=True,
            )

    @classmethod
    def generate_filename(
        cls,
        video_name: str,
        report_type: str = "report",
    ) -> str:

        video_name = Path(video_name).stem
        video_name = video_name.replace(" ", "_")

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        return f"{video_name}_{report_type}_{timestamp}"

    @classmethod
    def export(
        cls,
        filename: str,
        content: str,
        export_format: str,
        data: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        cls.ensure_folders()

        export_format = export_format.lower()

        if export_format == "txt":
            path = cls.save_txt(filename, content)

        elif export_format == "md":
            path = cls.save_markdown(filename, content)

        elif export_format == "html":
            path = cls.save_html(filename, content)

        elif export_format == "pdf":
            path = cls.save_pdf(filename, content)

        elif export_format == "json":
            path = cls.save_json(
                filename,
                data if data is not None else {
                    "content": content
                },
            )

        else:
            raise ValueError(
                f"Unsupported export format: {export_format}"
            )

        return {
            "path": str(path),
            "filename": path.name,
            "format": export_format,
            "size": path.stat().st_size,
            "created": datetime.now().isoformat(),
        }

    @classmethod
    def save_txt(
        cls,
        filename: str,
        content: str,
    ) -> Path:

        path = (
            cls.EXPORT_FOLDER
            / "txt"
            / f"{filename}.txt"
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        return path

    @classmethod
    def save_markdown(
        cls,
        filename: str,
        content: str,
    ) -> Path:

        path = (
            cls.EXPORT_FOLDER
            / "markdown"
            / f"{filename}.md"
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        return path

    @classmethod
    def save_html(
        cls,
        filename: str,
        content: str,
    ) -> Path:

        path = (
            cls.EXPORT_FOLDER
            / "html"
            / f"{filename}.html"
        )

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AI Video Analyzer Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin:40px;
    line-height:1.6;
}}
pre {{
    white-space: pre-wrap;
    word-wrap: break-word;
}}
</style>
</head>
<body>
<pre>{content}</pre>
</body>
</html>
"""

        path.write_text(
            html,
            encoding="utf-8",
        )

        return path

    @classmethod
    def save_pdf(
        cls,
        filename: str,
        content: str,
    ) -> Path:

        path = (
            cls.EXPORT_FOLDER
            / "pdf"
            / f"{filename}.pdf"
        )

        doc = SimpleDocTemplate(str(path))
        styles = getSampleStyleSheet()

        story = []

        for line in content.splitlines():

            if line.strip() == "":
                line = " "

            story.append(
                Paragraph(
                    line.replace("&", "&amp;"),
                    styles["BodyText"],
                )
            )

        doc.build(story)

        return path

    @classmethod
    def list_history_exports(
            cls,
    ) -> list[dict]:

        cls.ensure_folders()

        exports = []

        for export_type, folder_name in cls.FORMAT_FOLDERS.items():

            folder = cls.EXPORT_FOLDER / folder_name

            if not folder.exists():
                continue

            for file in folder.glob("*.*"):
                exports.append(
                    {
                        "name": file.name,
                        "type": export_type,
                        "path": str(file),
                        "size": file.stat().st_size,
                        "modified": datetime.fromtimestamp(
                            file.stat().st_mtime
                        ).strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

        exports.sort(
            key=lambda x: x["modified"],
            reverse=True,
        )

        return exports

    @classmethod
    def load_export(
            cls,
            export_type: str,
            filename: str,
    ):

        folder = (
                cls.EXPORT_FOLDER
                / cls.FORMAT_FOLDERS[export_type]
        )

        path = folder / filename

        if folder is None:
            raise ValueError(
                f"Unknown export type: {export_type}"
            )

        path = folder / filename

        if not path.exists():
            raise FileNotFoundError(path)

        if export_type == "json":

            import json

            with open(
                    path,
                    "r",
                    encoding="utf-8",
            ) as file:

                return json.load(file)

        elif export_type == "pdf":

            # PDF preview isn't supported here.
            # Return the file path.
            return str(path)

        else:

            with open(
                    path,
                    "r",
                    encoding="utf-8",
            ) as file:

                return file.read()

    @classmethod
    def save_json(
        cls,
        filename: str,
        data: Dict[str, Any],
    ) -> Path:

        path = (
            cls.EXPORT_FOLDER
            / "json"
            / f"{filename}.json"
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return path

    @classmethod
    def list_exports(
        cls,
    ) -> list[Path]:

        cls.ensure_folders()

        return sorted(
            cls.EXPORT_FOLDER.rglob("*.*")
        )

    @classmethod
    def delete_export(
        cls,
        path: str | Path,
    ) -> bool:

        path = Path(path)

        if path.exists():
            path.unlink()
            return True

        return False

    @classmethod
    def clear_exports(cls) -> None:

        cls.ensure_folders()

        for file in cls.EXPORT_FOLDER.rglob("*.*"):
            file.unlink()