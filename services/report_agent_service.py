"""
report_agent_service.py

Report Service

Responsibilities
----------------
- Build reports
- Save reports
- Save all formats
- Browse reports
- Load reports
- Delete reports
"""

from __future__ import annotations

import json

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate


class ReportService:

    REPORT_FOLDER = Path("reports")

    FORMAT_FOLDERS = {

        "pdf": REPORT_FOLDER / "pdf",

        "html": REPORT_FOLDER / "html",

        "md": REPORT_FOLDER / "markdown",

        "txt": REPORT_FOLDER / "txt",

        "json": REPORT_FOLDER / "json",

    }




    ############################################################
    # Folder Creation
    ############################################################

    @classmethod
    def ensure_folders(cls):

        cls.REPORT_FOLDER.mkdir(
            exist_ok=True,
        )

        for folder in cls.FORMAT_FOLDERS.values():

            folder.mkdir(
                parents=True,
                exist_ok=True,
            )

    ############################################################
    # Timestamp
    ############################################################

    @classmethod
    def timestamp(cls):

        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    ############################################################
    # Filename
    ############################################################

    @classmethod
    def generate_filename(

        cls,

        video_name,

        report_type="report",

    ):

        video_name = Path(
            video_name
        ).stem

        video_name = video_name.replace(
            " ",
            "_",
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        return (
            f"{video_name}_{report_type}_{timestamp}"
        )

    ############################################################
    # Build Report
    ############################################################

    @classmethod
    def build_report(

        cls,

        data: Dict[str, Any],

    ) -> str:

        report = []

        report.append(
            "# 🎥 AI Video Analysis Report\n"
        )

        report.append(
            f"Generated : {cls.timestamp()}\n"
        )

        report.append(
            "---\n"
        )

        ########################################################
        # Video
        ########################################################

        report.append(
            "## 📹 Video Information\n"
        )

        report.append(
            f"Filename : {data.get('video_name','N/A')}"
        )

        report.append(
            f"Duration : {data.get('video_duration','N/A')}"
        )

        report.append(
            f"Resolution : {data.get('video_resolution','N/A')}"
        )

        report.append(
            f"FPS : {data.get('video_fps','N/A')}"
        )

        report.append(
            f"Format : {data.get('video_format','N/A')}"
        )

        report.append(
            f"Size : {data.get('video_size','N/A')}"
        )

        report.append("\n---\n")

        ########################################################
        # Audio
        ########################################################

        report.append(
            "## 🎵 Audio Information\n"
        )

        report.append(
            f"Filename : {data.get('audio_name','N/A')}"
        )

        report.append(
            f"Duration : {data.get('audio_duration','N/A')}"
        )

        report.append(
            f"Channels : {data.get('channels','N/A')}"
        )

        report.append(
            f"Sample Rate : {data.get('sample_rate','N/A')}"
        )

        report.append(
            f"Format : {data.get('audio_format','N/A')}"
        )

        report.append(
            f"Size : {data.get('audio_size','N/A')}"
        )

        report.append("\n---\n")

        ########################################################
        # Transcript
        ########################################################

        report.append(
            "## 📝 Transcript\n"
        )

        report.append(
            data.get(
                "transcript",
                "Transcript not available.",
            )
        )

        report.append("\n---\n")

        ########################################################
        # Analysis
        ########################################################

        report.append(
            "## 🤖 AI Analysis\n"
        )

        report.append(
            str(
                data.get(
                    "analysis",
                    "Analysis not available.",
                )
            )
        )

        report.append("\n---\n")

        ########################################################
        # Chat
        ########################################################

        report.append(
            "## 💬 Chat History\n"
        )

        chat = data.get(
            "chat",
            [],
        )

        if isinstance(
            chat,
            (list, dict),
        ):

            chat = json.dumps(
                chat,
                indent=4,
                ensure_ascii=False,
            )

        report.append(chat)

        report.append("\n---\n")

        ########################################################
        # Metadata
        ########################################################

        report.append(
            "## ⚙ Metadata\n"
        )

        report.append(
            f"Provider : {data.get('provider','N/A')}"
        )

        report.append(
            f"Model : {data.get('model','N/A')}"
        )

        report.append(
            f"Generated : {cls.timestamp()}"
        )

        report.append("\n---\n")

        report.append(
            "Generated by AI Video Analysis Agent"
        )

        return "\n".join(report)

    ############################################################
    # Save TXT
    ############################################################

    @classmethod
    def save_txt(
        cls,
        filename: str,
        content: str,
    ) -> Path:

        cls.ensure_folders()

        path = (
            cls.FORMAT_FOLDERS["txt"]
            / f"{filename}.txt"
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        return path

    ############################################################
    # Save Markdown
    ############################################################

    @classmethod
    def save_markdown(
        cls,
        filename: str,
        content: str,
    ) -> Path:

        cls.ensure_folders()

        path = (
            cls.FORMAT_FOLDERS["md"]
            / f"{filename}.md"
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        return path

    ############################################################
    # Save HTML
    ############################################################

    @classmethod
    def save_html(
        cls,
        filename: str,
        content: str,
    ) -> Path:

        cls.ensure_folders()

        path = (
            cls.FORMAT_FOLDERS["html"]
            / f"{filename}.html"
        )

        html = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<title>AI Video Analysis Report</title>

<style>

body{{
    font-family:Arial,sans-serif;
    margin:40px;
    line-height:1.6;
}}

pre{{
    white-space:pre-wrap;
    word-wrap:break-word;
}}

h1,h2,h3{{
    color:#1f77b4;
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

    ############################################################
    # Save JSON
    ############################################################

    @classmethod
    def save_json(
        cls,
        filename: str,
        data: Dict[str, Any],
    ) -> Path:

        cls.ensure_folders()

        path = (
            cls.FORMAT_FOLDERS["json"]
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

    ############################################################
    # Save PDF
    ############################################################

    @classmethod
    def save_pdf(
        cls,
        filename: str,
        content: str,
    ) -> Path:

        cls.ensure_folders()

        path = (
            cls.FORMAT_FOLDERS["pdf"]
            / f"{filename}.pdf"
        )

        doc = SimpleDocTemplate(
            str(path)
        )

        styles = getSampleStyleSheet()

        story = []

        for line in content.splitlines():

            if not line.strip():

                line = " "

            line = (
                line.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
            )

            story.append(
                Paragraph(
                    line,
                    styles["BodyText"],
                )
            )

        doc.build(story)

        return path

    ############################################################
    # Save All Report Formats
    ############################################################

    @classmethod
    def save_all_reports(
        cls,
        filename: str,
        content: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:

        cls.ensure_folders()

        saved = {}

        txt = cls.save_txt(
            filename,
            content,
        )

        saved["txt"] = {
            "path": str(txt),
            "filename": txt.name,
        }

        md = cls.save_markdown(
            filename,
            content,
        )

        saved["md"] = {
            "path": str(md),
            "filename": md.name,
        }

        html = cls.save_html(
            filename,
            content,
        )

        saved["html"] = {
            "path": str(html),
            "filename": html.name,
        }

        pdf = cls.save_pdf(
            filename,
            content,
        )

        saved["pdf"] = {
            "path": str(pdf),
            "filename": pdf.name,
        }

        json_file = cls.save_json(
            filename,
            data,
        )

        saved["json"] = {
            "path": str(json_file),
            "filename": json_file.name,
        }

        return saved

    ############################################################
    # List Reports
    ############################################################

    @classmethod
    def list_reports(
        cls,
    ) -> List[Dict]:

        cls.ensure_folders()

        reports = []

        for report_type, folder in cls.FORMAT_FOLDERS.items():

            for file in sorted(
                folder.glob("*.*"),
                reverse=True,
            ):

                reports.append(
                    {
                        "name": file.name,
                        "type": report_type,
                        "path": str(file),
                        "size": file.stat().st_size,
                        "modified": datetime.fromtimestamp(
                            file.stat().st_mtime
                        ).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                )

        reports.sort(
            key=lambda x: x["modified"],
            reverse=True,
        )

        return reports

    ############################################################
    # Load Report
    ############################################################

    @classmethod
    def load_report(
        cls,
        report_type: str,
        filename: str,
    ):

        cls.ensure_folders()

        folder = cls.FORMAT_FOLDERS.get(
            report_type.lower()
        )

        if folder is None:

            raise ValueError(
                f"Unsupported report type: {report_type}"
            )

        path = folder / filename

        if not path.exists():

            raise FileNotFoundError(path)

        suffix = path.suffix.lower()

        if suffix == ".json":

            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            return file.read()

    ############################################################
    # Delete Report
    ############################################################

    @classmethod
    def delete_report(
        cls,
        report_type: str,
        filename: str,
    ) -> bool:

        cls.ensure_folders()

        folder = cls.FORMAT_FOLDERS.get(
            report_type.lower()
        )

        if folder is None:

            return False

        path = folder / filename

        if path.exists():

            path.unlink()

            return True

        return False

    ############################################################
    # Report Exists
    ############################################################

    @classmethod
    def report_exists(
        cls,
        report_type: str,
        filename: str,
    ) -> bool:

        cls.ensure_folders()

        folder = cls.FORMAT_FOLDERS.get(
            report_type.lower()
        )

        if folder is None:

            return False

        return (
            folder / filename
        ).exists()

    ############################################################
    # Clear Reports
    ############################################################

    @classmethod
    def clear_reports(cls):

        cls.ensure_folders()

        for folder in cls.FORMAT_FOLDERS.values():

            for file in folder.glob("*.*"):

                try:

                    file.unlink()

                except Exception:

                    pass

    ############################################################
    # Report Count
    ############################################################

    @classmethod
    def report_count(cls) -> Dict[str, int]:

        cls.ensure_folders()

        counts = {}

        total = 0

        for report_type, folder in cls.FORMAT_FOLDERS.items():

            count = len(
                list(folder.glob("*.*"))
            )

            counts[report_type] = count

            total += count

        counts["total"] = total

        return counts

    ############################################################
    # Report Storage
    ############################################################

    @classmethod
    def report_storage(cls) -> Dict[str, int]:

        cls.ensure_folders()

        storage = {}

        total = 0

        for report_type, folder in cls.FORMAT_FOLDERS.items():

            size = sum(

                file.stat().st_size

                for file in folder.glob("*.*")

                if file.is_file()

            )

            storage[report_type] = size

            total += size

        storage["total"] = total

        return storage

    ############################################################
    # Build Report From Files
    ############################################################

    @classmethod
    def build_report_from_files(

        cls,

        video_metadata: Dict[str, Any],

        audio_metadata: Dict[str, Any],

        transcript: str,

        analysis: str,

        chat: List[Dict],

        provider: str,

        model: str,

    ) -> str:

        data = {

            "video_name":
                video_metadata.get("filename"),

            "video_duration":
                video_metadata.get("duration"),

            "video_resolution":
                video_metadata.get("resolution"),

            "video_fps":
                video_metadata.get("fps"),

            "video_format":
                video_metadata.get("format"),

            "video_size":
                video_metadata.get("size"),

            "audio_name":
                audio_metadata.get("filename"),

            "audio_duration":
                audio_metadata.get("duration"),

            "channels":
                audio_metadata.get("channels"),

            "sample_rate":
                audio_metadata.get("sample_rate"),

            "audio_format":
                audio_metadata.get("format"),

            "audio_size":
                audio_metadata.get("size"),

            "transcript":
                transcript,

            "analysis":
                analysis,

            "chat":
                chat,

            "provider":
                provider,

            "model":
                model,

        }

        return cls.build_report(
            data
        )

    ############################################################
    # Generate Complete Report
    ############################################################

    @classmethod
    def generate_complete_report(

        cls,

        include_video: bool,

        include_audio: bool,

        include_transcript: bool,

        include_analysis: bool,

        include_chat: bool,

        include_metadata: bool,

        data: Dict[str, Any],

    ) -> str:

        return cls.build_report(
            data
        )

    ############################################################
    # Save Complete Report
    ############################################################

    @classmethod
    def generate_and_save(

        cls,

        filename: str,

        data: Dict[str, Any],

    ) -> Dict[str, Any]:

        report = cls.build_report(
            data
        )

        return cls.save_all_reports(

            filename=filename,

            content=report,

            data=data,

        )

    ############################################################
    # Folder Statistics
    ############################################################

    @classmethod
    def statistics(cls):

        return {

            "counts":
                cls.report_count(),

            "storage":
                cls.report_storage(),

            "reports":
                cls.list_reports(),

        }

