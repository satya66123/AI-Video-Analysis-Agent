from unittest.mock import MagicMock, patch

from agents.ai_orchestrator import AIOrchestrator


def make_service():
    return MagicMock()


@patch("agents.ai_orchestrator.WorkflowEngine")
@patch("agents.ai_orchestrator.AgentPipeline")
@patch("agents.ai_orchestrator.AgentRegistry")
@patch("agents.ai_orchestrator.AgentFactory")
def test_orchestrator_creation(
    factory_cls,
    registry_cls,
    pipeline_cls,
    engine_cls,
):
    agents = {
        "upload": MagicMock(),
        "chat": MagicMock(),
    }

    factory_cls.create_agents.return_value = agents

    registry = registry_cls.return_value
    pipeline = pipeline_cls.return_value
    engine = engine_cls.return_value

    orchestrator = AIOrchestrator(
        video_service=make_service(),
        audio_service=make_service(),
        speech_service=make_service(),
        analysis_service=make_service(),
        report_service=make_service(),
        export_service=make_service(),
        chat_service=make_service(),
    )

    factory_cls.create_agents.assert_called_once()

    registry.register_many.assert_called_once_with(agents)
    pipeline.register_default_pipelines.assert_called_once_with(registry)
    engine_cls.assert_called_once_with(pipeline)

    assert orchestrator.registry is registry
    assert orchestrator.pipeline is pipeline
    assert orchestrator.engine is engine


@patch("agents.ai_orchestrator.WorkflowEngine")
@patch("agents.ai_orchestrator.AgentPipeline")
@patch("agents.ai_orchestrator.AgentRegistry")
@patch("agents.ai_orchestrator.AgentFactory")
def test_run_pipeline(
    factory_cls,
    registry_cls,
    pipeline_cls,
    engine_cls,
):
    factory_cls.create_agents.return_value = {}

    engine = engine_cls.return_value
    engine.run.return_value = {"status": "completed"}

    orchestrator = AIOrchestrator(
        video_service=make_service(),
        audio_service=make_service(),
        speech_service=make_service(),
        analysis_service=make_service(),
        report_service=make_service(),
        export_service=make_service(),
        chat_service=make_service(),
    )

    context = {"video": "video.mp4"}

    result = orchestrator.run(
        context=context,
        pipeline="standard",
    )

    assert result["status"] == "completed"

    engine.run.assert_called_once_with(
        pipeline_name="standard",
        context=context,
    )


@patch("agents.ai_orchestrator.WorkflowEngine")
@patch("agents.ai_orchestrator.AgentPipeline")
@patch("agents.ai_orchestrator.AgentRegistry")
@patch("agents.ai_orchestrator.AgentFactory")
def test_run_chat(
    factory_cls,
    registry_cls,
    pipeline_cls,
    engine_cls,
):
    factory_cls.create_agents.return_value = {}

    registry = registry_cls.return_value
    registry.get.return_value = "chat_agent"

    engine = engine_cls.return_value
    engine.run_agent.return_value = {"status": "ok"}

    orchestrator = AIOrchestrator(
        video_service=make_service(),
        audio_service=make_service(),
        speech_service=make_service(),
        analysis_service=make_service(),
        report_service=make_service(),
        export_service=make_service(),
        chat_service=make_service(),
    )

    context = {}

    result = orchestrator.run_chat(context)

    assert result == {"status": "ok"}

    registry.get.assert_called_once_with("chat")

    engine.run_agent.assert_called_once_with(
        "chat_agent",
        context,
    )


@patch("agents.ai_orchestrator.WorkflowEngine")
@patch("agents.ai_orchestrator.AgentPipeline")
@patch("agents.ai_orchestrator.AgentRegistry")
@patch("agents.ai_orchestrator.AgentFactory")
def test_get_agent(
    factory_cls,
    registry_cls,
    pipeline_cls,
    engine_cls,
):
    factory_cls.create_agents.return_value = {}

    registry = registry_cls.return_value
    registry.get.return_value = "agent"

    orchestrator = AIOrchestrator(
        video_service=make_service(),
        audio_service=make_service(),
        speech_service=make_service(),
        analysis_service=make_service(),
        report_service=make_service(),
        export_service=make_service(),
        chat_service=make_service(),
    )

    assert orchestrator.get_agent("upload") == "agent"

    registry.get.assert_called_once_with("upload")


@patch("agents.ai_orchestrator.WorkflowEngine")
@patch("agents.ai_orchestrator.AgentPipeline")
@patch("agents.ai_orchestrator.AgentRegistry")
@patch("agents.ai_orchestrator.AgentFactory")
def test_list_agents(
    factory_cls,
    registry_cls,
    pipeline_cls,
    engine_cls,
):
    factory_cls.create_agents.return_value = {}

    registry = registry_cls.return_value
    registry.list_agents.return_value = ["upload", "chat"]

    orchestrator = AIOrchestrator(
        video_service=make_service(),
        audio_service=make_service(),
        speech_service=make_service(),
        analysis_service=make_service(),
        report_service=make_service(),
        export_service=make_service(),
        chat_service=make_service(),
    )

    assert orchestrator.list_agents() == ["upload", "chat"]

    registry.list_agents.assert_called_once()


@patch("agents.ai_orchestrator.WorkflowEngine")
@patch("agents.ai_orchestrator.AgentPipeline")
@patch("agents.ai_orchestrator.AgentRegistry")
@patch("agents.ai_orchestrator.AgentFactory")
def test_list_pipelines(
    factory_cls,
    registry_cls,
    pipeline_cls,
    engine_cls,
):
    factory_cls.create_agents.return_value = {}

    pipeline = pipeline_cls.return_value
    pipeline.list_pipelines.return_value = [
        "standard",
        "chat",
    ]

    orchestrator = AIOrchestrator(
        video_service=make_service(),
        audio_service=make_service(),
        speech_service=make_service(),
        analysis_service=make_service(),
        report_service=make_service(),
        export_service=make_service(),
        chat_service=make_service(),
    )

    assert orchestrator.list_pipelines() == [
        "standard",
        "chat",
    ]

    pipeline.list_pipelines.assert_called_once()