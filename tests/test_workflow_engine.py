from unittest.mock import MagicMock

from agents.workflow_agent import WorkflowAgent


def make_agent(name):
    agent = MagicMock()
    agent.name = name
    agent.execute.side_effect = lambda ctx: ctx
    return agent


def test_workflow_agent_creation():
    upload = make_agent("UploadAgent")
    audio = make_agent("AudioAgent")
    transcript = make_agent("TranscriptAgent")
    analysis = make_agent("AnalysisAgent")
    report = make_agent("ReportAgent")
    export = make_agent("ExportAgent")

    agent = WorkflowAgent(
        upload_agent=upload,
        audio_agent=audio,
        transcript_agent=transcript,
        analysis_agent=analysis,
        report_agent=report,
        export_agent=export,
    )

    assert agent.name == "WorkflowAgent"
    assert len(agent.pipeline) == 6
    assert agent.pipeline[0] is upload
    assert agent.pipeline[1] is audio
    assert agent.pipeline[2] is transcript
    assert agent.pipeline[3] is analysis
    assert agent.pipeline[4] is report
    assert agent.pipeline[5] is export


def test_execute_success():
    upload = make_agent("UploadAgent")
    audio = make_agent("AudioAgent")
    transcript = make_agent("TranscriptAgent")
    analysis = make_agent("AnalysisAgent")
    report = make_agent("ReportAgent")
    export = make_agent("ExportAgent")

    workflow = WorkflowAgent(
        upload_agent=upload,
        audio_agent=audio,
        transcript_agent=transcript,
        analysis_agent=analysis,
        report_agent=report,
        export_agent=export,
    )

    context = {}

    result = workflow.execute(context)

    assert result["status"] == "completed"
    assert result["current_agent"] == "WorkflowAgent"

    assert len(result["workflow_log"]) == 6

    for entry in result["workflow_log"]:
        assert entry["status"] == "completed"

    upload.execute.assert_called_once()
    audio.execute.assert_called_once()
    transcript.execute.assert_called_once()
    analysis.execute.assert_called_once()
    report.execute.assert_called_once()
    export.execute.assert_called_once()


def test_execute_failure():
    upload = make_agent("UploadAgent")
    audio = make_agent("AudioAgent")
    transcript = make_agent("TranscriptAgent")
    analysis = make_agent("AnalysisAgent")
    report = make_agent("ReportAgent")
    export = make_agent("ExportAgent")

    analysis.execute.side_effect = RuntimeError("Analysis failed")

    workflow = WorkflowAgent(
        upload_agent=upload,
        audio_agent=audio,
        transcript_agent=transcript,
        analysis_agent=analysis,
        report_agent=report,
        export_agent=export,
    )

    context = {}

    result = workflow.execute(context)

    assert result["status"] == "failed"
    assert result["current_agent"] == "AnalysisAgent"
    assert result["error"] == "Analysis failed"

    assert len(result["workflow_log"]) == 4

    assert result["workflow_log"][0]["status"] == "completed"
    assert result["workflow_log"][1]["status"] == "completed"
    assert result["workflow_log"][2]["status"] == "completed"
    assert result["workflow_log"][3]["status"] == "failed"
    assert result["workflow_log"][3]["error"] == "Analysis failed"

    upload.execute.assert_called_once()
    audio.execute.assert_called_once()
    transcript.execute.assert_called_once()
    analysis.execute.assert_called_once()
    report.execute.assert_not_called()
    export.execute.assert_not_called()