"""
tests/test_export_agent.py
"""

from unittest.mock import MagicMock

import pytest

from agents.export_agent import ExportAgent


def make_service():

    service = MagicMock()

    service.generate_filename.return_value = "video_analysis"

    service.export.side_effect = [

        {
            "path": "exports/pdf/video_analysis.pdf",
            "filename": "video_analysis.pdf",
            "format": "pdf",
        },

        {
            "path": "exports/html/video_analysis.html",
            "filename": "video_analysis.html",
            "format": "html",
        },

        {
            "path": "exports/markdown/video_analysis.md",
            "filename": "video_analysis.md",
            "format": "md",
        },

        {
            "path": "exports/txt/video_analysis.txt",
            "filename": "video_analysis.txt",
            "format": "txt",
        },

        {
            "path": "exports/json/video_analysis.json",
            "filename": "video_analysis.json",
            "format": "json",
        },

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


def test_execute_default_formats():

    service = make_service()

    agent = ExportAgent(service)

    context = make_context()

    result = agent.execute(context)

    assert result["status"] == "export_completed"

    assert result["current_agent"] == "ExportAgent"

    assert len(result["exports"]) == 5

    assert "pdf" in result["exports"]

    assert "html" in result["exports"]

    assert "md" in result["exports"]

    assert "txt" in result["exports"]

    assert "json" in result["exports"]

    service.generate_filename.assert_called_once_with(

        video_name="video.mp4",

        report_type="analysis",

    )

    assert service.export.call_count == 5


def test_execute_custom_formats():

    service = MagicMock()

    service.generate_filename.return_value = "video_analysis"

    service.export.side_effect = [

        {

            "path": "exports/pdf/video_analysis.pdf",

            "format": "pdf",

        },

        {

            "path": "exports/html/video_analysis.html",

            "format": "html",

        },

    ]

    agent = ExportAgent(service)

    context = make_context()

    context["export_formats"] = [

        "pdf",

        "html",

    ]

    result = agent.execute(context)

    assert result["status"] == "export_completed"

    assert len(result["exports"]) == 2

    assert "pdf" in result["exports"]

    assert "html" in result["exports"]

    assert service.export.call_count == 2


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

    assert len(result["exports"]) == 5

    service.generate_filename.assert_called_once_with(

        video_name="video",

        report_type="analysis",

    )


def test_export_called_with_correct_arguments():

    service = make_service()

    agent = ExportAgent(service)

    context = make_context()

    agent.execute(context)

    _, kwargs = service.export.call_args

    assert kwargs["filename"] == "video_analysis"

    assert kwargs["content"] == "# Report"

    assert kwargs["data"]["video"] == context["video_metadata"]

    assert kwargs["data"]["audio"] == context["audio_metadata"]

    assert kwargs["data"]["transcript"] == "Transcript"

    assert kwargs["data"]["analysis"] == "Analysis"

    assert kwargs["data"]["provider"] == "ollama"

    assert kwargs["data"]["model"] == "llama3.1"