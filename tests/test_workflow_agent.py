from unittest.mock import MagicMock

from agents.workflow_agent import WorkflowAgent


def make_agent(name):
    agent = MagicMock()
    agent.name = name

    def execute(context):
        context[name] = True
        return context

    agent.execute.side_effect = execute
    return agent


def create_workflow():
    return WorkflowAgent(
        upload_agent=make_agent("upload"),
        audio_agent=make_agent("audio"),
        transcript_agent=make_agent("transcript"),
        analysis_agent=make_agent("analysis"),
        report_agent=make_agent("report"),
        export_agent=make_agent("export"),
    )


def test_workflow_creation():
    workflow = create_workflow()

    assert workflow.name == "WorkflowAgent"
    assert len(workflow.pipeline) == 6


def test_workflow_execute_success():
    workflow = create_workflow()

    context = {}

    result = workflow.execute(context)

    assert result["status"] == "completed"
    assert result["current_agent"] == "WorkflowAgent"
    assert len(result["workflow_log"]) == 6

    assert result["upload"]
    assert result["audio"]
    assert result["transcript"]
    assert result["analysis"]
    assert result["report"]
    assert result["export"]


def test_workflow_execute_failure():
    upload = make_agent("upload")

    bad = MagicMock()
    bad.name = "audio"
    bad.execute.side_effect = RuntimeError("failure")

    workflow = WorkflowAgent(
        upload_agent=upload,
        audio_agent=bad,
        transcript_agent=make_agent("transcript"),
        analysis_agent=make_agent("analysis"),
        report_agent=make_agent("report"),
        export_agent=make_agent("export"),
    )

    result = workflow.execute({})

    assert result["status"] == "failed"
    assert result["current_agent"] == "audio"
    assert result["error"] == "failure"
    assert result["workflow_log"][-1]["status"] == "failed"