"""
tests/test_export_agent_service.py
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from services.export_agent_service import ExportService


@pytest.fixture
def export_folder(tmp_path, monkeypatch):

    monkeypatch.setattr(
        ExportService,
        "EXPORT_FOLDER",
        tmp_path,
    )

    ExportService.ensure_folders()

    return tmp_path


def test_ensure_folders(export_folder):

    assert (export_folder / "txt").exists()

    assert (export_folder / "markdown").exists()

    assert (export_folder / "html").exists()

    assert (export_folder / "pdf").exists()

    assert (export_folder / "json").exists()


@patch(
    "services.export_agent_service.datetime"
)
def test_generate_filename(
    mock_datetime,
):

    mock_datetime.now.return_value.strftime.return_value = (
        "20260101_120000"
    )

    filename = ExportService.generate_filename(
        "sample video.mp4",
        "report",
    )

    assert filename == (
        "sample_video_report_20260101_120000"
    )


def test_save_txt(export_folder):

    path = ExportService.save_txt(
        "sample",
        "Hello World",
    )

    assert path.exists()

    assert (
        path.read_text(
            encoding="utf-8"
        )
        == "Hello World"
    )


def test_save_markdown(export_folder):

    path = ExportService.save_markdown(
        "sample",
        "# Heading",
    )

    assert path.exists()

    assert "# Heading" in path.read_text(
        encoding="utf-8"
    )


def test_save_html(export_folder):

    path = ExportService.save_html(
        "sample",
        "Hello",
    )

    assert path.exists()

    html = path.read_text(
        encoding="utf-8"
    )

    assert "<html>" in html

    assert "Hello" in html


def test_save_pdf(export_folder):

    path = ExportService.save_pdf(
        "sample",
        "PDF Content",
    )

    assert path.exists()

    assert path.suffix == ".pdf"

    assert path.stat().st_size > 0


def test_save_json(export_folder):

    data = {
        "name": "video",
        "score": 95,
    }

    path = ExportService.save_json(
        "sample",
        data,
    )

    assert path.exists()

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        loaded = json.load(file)

    assert loaded == data


def test_export_txt(export_folder):

    result = ExportService.export(
        filename="report",
        content="Hello",
        export_format="txt",
    )

    assert result["format"] == "txt"

    assert Path(
        result["path"]
    ).exists()


def test_export_markdown(export_folder):

    result = ExportService.export(
        "report",
        "# Markdown",
        "md",
    )

    assert result["format"] == "md"

    assert Path(
        result["path"]
    ).exists()


def test_export_html(export_folder):

    result = ExportService.export(
        "report",
        "HTML",
        "html",
    )

    assert result["format"] == "html"

    assert Path(
        result["path"]
    ).exists()


def test_export_pdf(export_folder):

    result = ExportService.export(
        "report",
        "PDF",
        "pdf",
    )

    assert result["format"] == "pdf"

    assert Path(
        result["path"]
    ).exists()


def test_export_json(export_folder):

    result = ExportService.export(
        filename="report",
        content="ignored",
        export_format="json",
        data={
            "value": 10
        },
    )

    assert result["format"] == "json"

    with open(
        result["path"],
        "r",
        encoding="utf-8",
    ) as file:

        loaded = json.load(file)

    assert loaded["value"] == 10


def test_export_invalid_format(
    export_folder,
):

    with pytest.raises(ValueError):

        ExportService.export(
            "sample",
            "content",
            "xml",
        )


def test_list_exports(
    export_folder,
):

    ExportService.save_txt(
        "a",
        "1",
    )

    ExportService.save_markdown(
        "b",
        "2",
    )

    files = ExportService.list_exports()

    assert len(files) >= 2

    assert all(
        isinstance(
            file,
            Path,
        )
        for file in files
    )


def test_delete_export(
    export_folder,
):

    path = ExportService.save_txt(
        "delete_me",
        "text",
    )

    assert ExportService.delete_export(
        path
    ) is True

    assert not path.exists()


def test_delete_missing_export():

    assert (
        ExportService.delete_export(
            "missing.txt"
        )
        is False
    )


def test_clear_exports(
    export_folder,
):

    ExportService.save_txt(
        "one",
        "1",
    )

    ExportService.save_markdown(
        "two",
        "2",
    )

    ExportService.save_html(
        "three",
        "3",
    )

    ExportService.clear_exports()

    assert (
        len(
            ExportService.list_exports()
        )
        == 0
    )