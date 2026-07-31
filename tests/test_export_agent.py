from unittest.mock import MagicMock

import pytest

from agents.export_agent import ExportAgent


def make_service():
    service = MagicMock()
    service.generate_filename.return_value = "video_analysis"
    service.export.side_effect = [
        "exports/video_analysis.pdf",
        "exports/video_analysis.docx",
        "exports/video_analysis.html",
    ]
    return service


def make_context():
    return {
        "report": "# Report",
        "video_metadata": {
            "filename": "video.mp4",
        },
        "audio_metadata": {
            "filename": "video.wav",
        },
        "transcript": "Transcript",
        "analysis": "Analysis",
        "provider_name": "ollama",
        "model_name": "llama3.1",
    }


def test_export_agent_creation():
    service = make_service()

    agent = ExportAgent(service)

    assert agent.name == "ExportAgent"
    assert agent.export_service is service


def test_execute_default_pdf():
    service = make_service()

    agent = ExportAgent(service)

    context = make_context()

    result = agent.execute(context)

    assert result["status"] == "export_completed"
    assert result["current_agent"] == "ExportAgent"
    assert result["exports"] == [
        "exports/video_analysis.pdf",
    ]

    service.generate_filename.assert_called_once_with(
        video_name="video.mp4",
        report_type="analysis",
    )

    service.export.assert_called_once()

    _, kwargs = service.export.call_args

    assert kwargs["filename"] == "video_analysis"
    assert kwargs["content"] == "# Report"
    assert kwargs["export_format"] == "pdf"

    assert kwargs["data"]["video"] == context["video_metadata"]
    assert kwargs["data"]["audio"] == context["audio_metadata"]
    assert kwargs["data"]["transcript"] == "Transcript"
    assert kwargs["data"]["analysis"] == "Analysis"
    assert kwargs["data"]["provider"] == "ollama"
    assert kwargs["data"]["model"] == "llama3.1"


def test_execute_multiple_formats():
    service = make_service()

    agent = ExportAgent(service)

    context = make_context()
    context["export_formats"] = [
        "pdf",
        "docx",
        "html",
    ]

    result = agent.execute(context)

    assert result["status"] == "export_completed"

    assert result["exports"] == [
        "exports/video_analysis.pdf",
        "exports/video_analysis.docx",
        "exports/video_analysis.html",
    ]

    assert service.export.call_count == 3


def test_execute_without_report():
    service = make_service()

    agent = ExportAgent(service)

    with pytest.raises(
        ValueError,
        match="Workflow context does not contain a report.",
    ):
        agent.execute({})


def test_execute_defaults():
    service = make_service()

    agent = ExportAgent(service)

    context = {
        "report": "# Report",
    }

    result = agent.execute(context)

    assert result["status"] == "export_completed"
    assert result["exports"] == [
        "exports/video_analysis.pdf",
    ]

    service.generate_filename.assert_called_once_with(
        video_name="video",
        report_type="analysis",
    )