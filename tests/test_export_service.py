from pathlib import Path

import pytest

from services.export_service import ExportService


@pytest.fixture
def export_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(
        ExportService,
        "EXPORT_FOLDER",
        tmp_path,
    )
    return tmp_path


class TestExportService:

    def test_create_export_folder(self, export_dir):
        ExportService.create_export_folder()

        assert export_dir.exists()
        assert export_dir.is_dir()

    def test_save_txt(self, export_dir):
        path = ExportService.save_txt(
            "report",
            "Hello World",
        )

        assert path == export_dir / "report.txt"
        assert path.exists()
        assert path.read_text(encoding="utf-8") == "Hello World"

    def test_save_md(self, export_dir):
        path = ExportService.save_md(
            "report",
            "# Title",
        )

        assert path == export_dir / "report.md"
        assert path.exists()
        assert path.read_text(encoding="utf-8") == "# Title"

    def test_save_html(self, export_dir):
        path = ExportService.save_html(
            "report",
            "Sample Report",
        )

        assert path == export_dir / "report.html"

        html = path.read_text(encoding="utf-8")

        assert "<html>" in html
        assert "AI Video Analyzer Report" in html
        assert "Sample Report" in html

    def test_save_pdf(self, export_dir):
        path = ExportService.save_pdf(
            "report",
            "Line 1\nLine 2",
        )

        assert path == export_dir / "report.pdf"
        assert path.exists()
        assert path.stat().st_size > 0

    def test_generate_filename(self):
        name = ExportService.generate_filename(
            "My Video.mp4"
        )

        assert name.startswith("My_Video_video_report_")