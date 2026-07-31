from unittest.mock import MagicMock

from agents.agent_factory import AgentFactory
from agents.upload_agent import UploadAgent
from agents.audio_agent import AudioAgent
from agents.transcript_agent import TranscriptAgent
from agents.analysis_agent import AnalysisAgent
from agents.report_agent import ReportAgent
from agents.export_agent import ExportAgent
from agents.chat_agent import ChatAgent
from agents.workflow_agent import WorkflowAgent


def make_services():
    return {
        "video_service": MagicMock(),
        "audio_service": MagicMock(),
        "speech_service": MagicMock(),
        "analysis_service": MagicMock(),
        "report_service": MagicMock(),
        "export_service": MagicMock(),
        "chat_service": MagicMock(),
    }


def test_create_agents_returns_dictionary():

    agents = AgentFactory.create_agents(
        **make_services()
    )

    assert isinstance(agents, dict)


def test_create_agents_contains_all_agents():

    agents = AgentFactory.create_agents(
        **make_services()
    )

    expected = {
        "upload",
        "audio",
        "transcript",
        "analysis",
        "report",
        "export",
        "chat",
        "workflow",
    }

    assert set(agents.keys()) == expected


def test_upload_agent_type():

    agents = AgentFactory.create_agents(
        **make_services()
    )

    assert isinstance(
        agents["upload"],
        UploadAgent,
    )


def test_audio_agent_type():

    agents = AgentFactory.create_agents(
        **make_services()
    )

    assert isinstance(
        agents["audio"],
        AudioAgent,
    )


def test_transcript_agent_type():

    agents = AgentFactory.create_agents(
        **make_services()
    )

    assert isinstance(
        agents["transcript"],
        TranscriptAgent,
    )


def test_analysis_agent_type():

    agents = AgentFactory.create_agents(
        **make_services()
    )

    assert isinstance(
        agents["analysis"],
        AnalysisAgent,
    )


def test_report_agent_type():

    agents = AgentFactory.create_agents(
        **make_services()
    )

    assert isinstance(
        agents["report"],
        ReportAgent,
    )


def test_export_agent_type():

    agents = AgentFactory.create_agents(
        **make_services()
    )

    assert isinstance(
        agents["export"],
        ExportAgent,
    )


def test_chat_agent_type():

    agents = AgentFactory.create_agents(
        **make_services()
    )

    assert isinstance(
        agents["chat"],
        ChatAgent,
    )


def test_workflow_agent_type():

    agents = AgentFactory.create_agents(
        **make_services()
    )

    assert isinstance(
        agents["workflow"],
        WorkflowAgent,
    )