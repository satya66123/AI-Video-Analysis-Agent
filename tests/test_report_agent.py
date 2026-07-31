from unittest.mock import MagicMock

from agents.report_agent import ReportAgent


def make_service():
    service = MagicMock()
    service.generate_complete_report.return_value = (
        "# AI Video Analysis Report\n\nReport content."
    )
    return service


def make_context():
    return {
        "video_metadata": {
            "filename": "video.mp4",
            "duration": "00:10:00",
            "resolution": "1920x1080",
            "fps": 30,
            "extension": "mp4",
            "size": 1024,
        },
        "audio_metadata": {
            "filename": "video.wav",
            "duration": "00:10:00",
            "channels": 2,
            "sample_rate": 44100,
            "extension": ".wav",
            "size": 512,
        },
        "provider_name": "ollama",
        "model_name": "llama3.1",
        "transcript": "Transcript text",
        "analysis": "Analysis text",
        "chat_history": [
            {
                "user": "Hi",
                "assistant": "Hello",
            }
        ],
    }


def test_report_agent_creation():
    service = make_service()

    agent = ReportAgent(service)

    assert agent.name == "ReportAgent"
    assert agent.report_service is service


def test_execute_success():
    service = make_service()

    agent = ReportAgent(service)

    context = make_context()

    result = agent.execute(context)

    assert result["status"] == "report_generated"
    assert result["current_agent"] == "ReportAgent"
    assert result["report"] == "# AI Video Analysis Report\n\nReport content."

    metadata = result["report_metadata"]

    assert metadata["length"] == len(result["report"])
    assert metadata["words"] == len(result["report"].split())
    assert "generated_at" in metadata

    service.generate_complete_report.assert_called_once()

    _, kwargs = service.generate_complete_report.call_args

    assert kwargs["include_video"] is True
    assert kwargs["include_audio"] is True
    assert kwargs["include_transcript"] is True
    assert kwargs["include_analysis"] is True
    assert kwargs["include_chat"] is True
    assert kwargs["include_metadata"] is True

    data = kwargs["data"]

    assert data["video_name"] == "video.mp4"
    assert data["video_duration"] == "00:10:00"
    assert data["video_resolution"] == "1920x1080"
    assert data["video_fps"] == 30
    assert data["video_format"] == "mp4"
    assert data["video_size"] == 1024

    assert data["audio_name"] == "video.wav"
    assert data["audio_duration"] == "00:10:00"
    assert data["channels"] == 2
    assert data["sample_rate"] == 44100
    assert data["audio_format"] == ".wav"
    assert data["audio_size"] == 512

    assert data["provider"] == "ollama"
    assert data["model"] == "llama3.1"
    assert data["transcript"] == "Transcript text"
    assert data["analysis"] == "Analysis text"
    assert data["chat"] == [{"user": "Hi", "assistant": "Hello"}]


def test_execute_with_empty_context():
    service = make_service()

    agent = ReportAgent(service)

    result = agent.execute({})

    assert result["status"] == "report_generated"
    assert result["current_agent"] == "ReportAgent"

    _, kwargs = service.generate_complete_report.call_args

    data = kwargs["data"]

    assert data["video_name"] == "N/A"
    assert data["audio_name"] == "N/A"
    assert data["provider"] == "N/A"
    assert data["model"] == "N/A"
    assert data["transcript"] == ""
    assert data["analysis"] == ""
    assert data["chat"] == ""