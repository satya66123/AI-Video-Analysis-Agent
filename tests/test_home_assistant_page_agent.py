import streamlit as st


from ui.home_assistant_page_agent import (
    HomeAssistantPageAgent,
)


####################################################
# Constructor
####################################################

def test_init():

    page = HomeAssistantPageAgent()

    assert page.video_service is not None

    assert page.chat_service is not None

    assert page.integrated_agent is not None


####################################################
# Render
####################################################

def test_render_calls_all_sections(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    calls = []

    monkeypatch.setattr(
        "ui.home_assistant_page_agent.HeaderAgent.render",
        lambda title: calls.append("header"),
    )

    monkeypatch.setattr(
        page,
        "video_section",
        lambda: calls.append("video"),
    )

    monkeypatch.setattr(
        page,
        "chat_section",
        lambda: calls.append("chat"),
    )

    monkeypatch.setattr(
        page,
        "end_chat_section",
        lambda: calls.append("end_chat"),
    )

    monkeypatch.setattr(
        page,
        "session_information",
        lambda: calls.append("session"),
    )

    monkeypatch.setattr(
        "ui.home_assistant_page_agent.FooterAgent.render",
        lambda: calls.append("footer"),
    )

    monkeypatch.setattr(
        "streamlit.divider",
        lambda: None,
    )

    page.render()

    assert calls == [

        "header",

        "video",

        "chat",

        "end_chat",

        "session",

        "footer",

    ]


####################################################
# Session Information - Not Ready
####################################################

def test_session_information_not_ready(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = False

    info_called = []

    monkeypatch.setattr(
        "streamlit.info",
        lambda message: info_called.append(message),
    )

    page.session_information()

    assert len(info_called) == 1


####################################################
# Session Information - Ready
####################################################

def test_session_information_ready(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True

    st.session_state["assistant_video"] = "video.mp4"

    st.session_state["assistant_video_metadata"] = {
        "duration": "10 sec",
        "resolution": "1920x1080",
        "size": "5 MB",
    }

    st.session_state["assistant_audio_metadata"] = {
        "duration": "10 sec",
    }

    st.session_state["assistant_transcript"] = "Transcript"

    st.session_state["assistant_analysis"] = {
        "summary": "AI Summary",
    }

    st.session_state["assistant_chat_sessions"] = []

    st.session_state["assistant_chat_id"] = "chat1"

    st.session_state["provider_name"] = "Ollama"

    st.session_state["model_name"] = "llama3"

    monkeypatch.setattr(
        "streamlit.columns",
        lambda n: (__import__("contextlib").nullcontext(),
                   __import__("contextlib").nullcontext()),
    )

    monkeypatch.setattr(
        "streamlit.write",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.success",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.button",
        lambda *args, **kwargs: False,
    )

    monkeypatch.setattr(
        "streamlit.divider",
        lambda: None,
    )

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    page.session_information()


####################################################
# Reset Session
####################################################

def test_reset_session(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True

    st.session_state["assistant_video"] = "video.mp4"

    rerun_called = []

    monkeypatch.setattr(
        "streamlit.columns",
        lambda n: (__import__("contextlib").nullcontext(),
                   __import__("contextlib").nullcontext()),
    )

    monkeypatch.setattr(
        "streamlit.write",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.success",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.button",
        lambda *args, **kwargs: True,
    )

    monkeypatch.setattr(
        "streamlit.rerun",
        lambda: rerun_called.append(True),
    )

    monkeypatch.setattr(
        "streamlit.divider",
        lambda: None,
    )

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    page.session_information()

    assert "assistant_ready" not in st.session_state

    assert len(rerun_called) == 1



####################################################
# No Existing Videos
####################################################

def test_video_section_no_existing_videos(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.divider",
        lambda: None,
    )

    monkeypatch.setattr(
        "streamlit.file_uploader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        page.video_service,
        "list_videos",
        lambda: [],
    )

    info_called = []

    monkeypatch.setattr(
        "streamlit.info",
        lambda msg: info_called.append(msg),
    )

    page.video_section()

    assert len(info_called) == 1


####################################################
# Duplicate Video
####################################################

def test_video_section_duplicate_video(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.file_uploader",
        lambda *args, **kwargs: object(),
    )

    monkeypatch.setattr(
        "streamlit.button",
        lambda *args, **kwargs: True,
    )

    monkeypatch.setattr(
        "streamlit.progress",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.empty",
        lambda: None,
    )

    class DummySpinner:
        def __enter__(self):
            return self

        def __exit__(
            self,
            exc_type,
            exc,
            tb,
        ):
            pass

    monkeypatch.setattr(
        "streamlit.spinner",
        lambda *args, **kwargs: DummySpinner(),
    )

    monkeypatch.setattr(
        page.video_service,
        "is_duplicate",
        lambda file: True,
    )

    warnings = []

    monkeypatch.setattr(
        "streamlit.warning",
        lambda msg: warnings.append(msg),
    )

    monkeypatch.setattr(
        "streamlit.info",
        lambda *args, **kwargs: None,
    )

    page.video_section()

    assert len(warnings) == 1


####################################################
# Workflow Failed
####################################################

def test_video_section_workflow_failed(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state["orchestrator"] = type(
        "",
        (),
        {
            "run": lambda self, ctx: {
                "status": "failed",
                "error": "Failed",
            }
        },
    )()

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.file_uploader",
        lambda *args, **kwargs: object(),
    )

    monkeypatch.setattr(
        "streamlit.button",
        lambda *args, **kwargs: True,
    )

    monkeypatch.setattr(
        page.video_service,
        "is_duplicate",
        lambda file: False,
    )

    monkeypatch.setattr(
        "streamlit.progress",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.empty",
        lambda: None,
    )

    class DummySpinner:
        def __enter__(self):
            return self

        def __exit__(
            self,
            exc_type,
            exc,
            tb,
        ):
            pass

    monkeypatch.setattr(
        "streamlit.spinner",
        lambda *args, **kwargs: DummySpinner(),
    )

    errors = []

    monkeypatch.setattr(
        "streamlit.error",
        lambda msg: errors.append(msg),
    )

    page.video_section()

    assert len(errors) == 1


####################################################
# Load Existing Video
####################################################

def test_video_section_load_existing_video(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.divider",
        lambda: None,
    )

    monkeypatch.setattr(
        "streamlit.file_uploader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        page.video_service,
        "list_videos",
        lambda: [
            "video.mp4",
        ],
    )

    monkeypatch.setattr(
        "streamlit.selectbox",
        lambda *args, **kwargs: "video.mp4",
    )

    monkeypatch.setattr(
        "streamlit.button",
        lambda *args, **kwargs: True,
    )

    loaded = []

    monkeypatch.setattr(
        page.integrated_agent,
        "load_existing_video",
        lambda video: loaded.append(video),
    )

    monkeypatch.setattr(
        "streamlit.success",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.rerun",
        lambda: None,
    )

    class DummySpinner:
        def __enter__(self):
            return self

        def __exit__(
            self,
            exc_type,
            exc,
            tb,
        ):
            pass

    monkeypatch.setattr(
        "streamlit.spinner",
        lambda *args, **kwargs: DummySpinner(),
    )

    page.video_section()

    assert loaded == [
        "video.mp4",
    ]


####################################################
# Chat - Not Ready
####################################################

def test_chat_section_not_ready(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = False

    info = []

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.info",
        lambda msg: info.append(msg),
    )

    page.chat_section()

    assert len(info) == 1


####################################################
# Chat - No Previous Chats
####################################################

def test_chat_section_no_previous_chats(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True
    st.session_state["assistant_video"] = "video.mp4"

    monkeypatch.setattr(
        page.chat_service,
        "list_video_chats",
        lambda video: [],
    )

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.info",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.chat_input",
        lambda *args, **kwargs: None,
    )

    page.chat_section()

    assert st.session_state["assistant_history"] == []


####################################################
# Chat - Load Existing Chat
####################################################

def test_chat_section_load_existing_chat(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True
    st.session_state["assistant_video"] = "video.mp4"

    class DummyChat:

        stem = "chat1"

    monkeypatch.setattr(
        page.chat_service,
        "list_video_chats",
        lambda video: [DummyChat()],
    )

    monkeypatch.setattr(
        "streamlit.selectbox",
        lambda *args, **kwargs: "chat1",
    )

    monkeypatch.setattr(
        page.chat_service,
        "load_chat_by_id",
        lambda chat: [
            {
                "user": "Hi",
                "assistant": "Hello",
            }
        ],
    )

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.chat_input",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.chat_message",
        lambda *args, **kwargs: __import__("contextlib").nullcontext(),
    )

    monkeypatch.setattr(
        "streamlit.markdown",
        lambda *args, **kwargs: None,
    )

    page.chat_section()

    assert st.session_state["assistant_chat_id"] == "chat1"


####################################################
# Chat - New Chat
####################################################

def test_chat_section_new_chat(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True
    st.session_state["assistant_video"] = "video.mp4"

    monkeypatch.setattr(
        page.chat_service,
        "list_video_chats",
        lambda video: [],
    )

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.info",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.chat_input",
        lambda *args, **kwargs: None,
    )

    page.chat_section()

    assert st.session_state["assistant_chat_id"] is None


####################################################
# Chat - First Message Creates Chat
####################################################

def test_chat_section_create_chat(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True
    st.session_state["assistant_video"] = "video.mp4"
    st.session_state["provider_name"] = "Ollama"
    st.session_state["model_name"] = "llama3"
    st.session_state["assistant_transcript"] = "Transcript"

    monkeypatch.setattr(
        page.chat_service,
        "list_video_chats",
        lambda video: [],
    )

    monkeypatch.setattr(
        page.chat_service,
        "create_chat",
        lambda video: "chat123",
    )

    monkeypatch.setattr(
        page.chat_service,
        "save_chat_by_id",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.info",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.chat_input",
        lambda *args, **kwargs: "Hello",
    )

    monkeypatch.setattr(
        "streamlit.chat_message",
        lambda *args, **kwargs: __import__("contextlib").nullcontext(),
    )

    monkeypatch.setattr(
        "streamlit.markdown",
        lambda *args, **kwargs: None,
    )

    class DummySpinner:

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(
        "streamlit.spinner",
        lambda *args, **kwargs: DummySpinner(),
    )

    st.session_state["orchestrator"] = type(
        "",
        (),
        {
            "run_chat": lambda self, ctx: {
                "chat_answer": "Hello!"
            }
        },
    )()

    page.chat_section()

    assert st.session_state["assistant_chat_id"] == "chat123"


####################################################
# End Chat - Not Ready
####################################################

def test_end_chat_not_ready(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = False

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    page.end_chat_section()


####################################################
# End Chat - No History
####################################################

def test_end_chat_no_history(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True

    st.session_state["assistant_history"] = []

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    page.end_chat_section()


####################################################
# End Chat Success
####################################################

def test_end_chat_success(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True

    st.session_state["assistant_video"] = "video.mp4"

    st.session_state["assistant_chat_id"] = "chat1"

    st.session_state["assistant_history"] = [
        {
            "user": "Hi",
            "assistant": "Hello",
        }
    ]

    st.session_state["assistant_video_metadata"] = {}

    st.session_state["assistant_audio_metadata"] = {}

    st.session_state["assistant_transcript"] = "Transcript"

    st.session_state["assistant_analysis"] = {}

    st.session_state["provider_name"] = "Ollama"

    st.session_state["model_name"] = "llama3"

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.button",
        lambda *args, **kwargs: True,
    )

    class DummySpinner:

        def __enter__(self):
            return self

        def __exit__(
            self,
            exc_type,
            exc,
            tb,
        ):
            pass

    monkeypatch.setattr(
        "streamlit.spinner",
        lambda *args, **kwargs: DummySpinner(),
    )

    monkeypatch.setattr(
        page.chat_service,
        "save_chat_by_id",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        page.chat_service,
        "list_video_chats",
        lambda video: [],
    )

    monkeypatch.setattr(
        "ui.home_assistant_page_agent.ReportService.build_report_from_files",
        lambda **kwargs: "Report",
    )

    monkeypatch.setattr(
        "ui.home_assistant_page_agent.ReportService.generate_filename",
        lambda *args: "report",
    )

    monkeypatch.setattr(
        "ui.home_assistant_page_agent.ReportService.save_all_reports",
        lambda **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.success",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.rerun",
        lambda: None,
    )

    page.end_chat_section()

    assert st.session_state["assistant_chat_id"] is None

    assert st.session_state["assistant_history"] == []


####################################################
# Report Generation
####################################################

def test_end_chat_generates_report(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True

    st.session_state["assistant_video"] = "video.mp4"

    st.session_state["assistant_chat_id"] = "chat1"

    st.session_state["assistant_history"] = [
        {
            "user": "Hi",
            "assistant": "Hello",
        }
    ]

    st.session_state["assistant_video_metadata"] = {}

    st.session_state["assistant_audio_metadata"] = {}

    st.session_state["assistant_transcript"] = "Transcript"

    st.session_state["assistant_analysis"] = {}

    st.session_state["provider_name"] = "Ollama"

    st.session_state["model_name"] = "llama3"

    report_called = []

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.button",
        lambda *args, **kwargs: True,
    )

    class DummySpinner:

        def __enter__(self):
            return self

        def __exit__(
            self,
            exc_type,
            exc,
            tb,
        ):
            pass

    monkeypatch.setattr(
        "streamlit.spinner",
        lambda *args, **kwargs: DummySpinner(),
    )

    monkeypatch.setattr(
        page.chat_service,
        "save_chat_by_id",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        page.chat_service,
        "list_video_chats",
        lambda video: [],
    )

    monkeypatch.setattr(
        "ui.home_assistant_page_agent.ReportService.build_report_from_files",
        lambda **kwargs: "Report",
    )

    monkeypatch.setattr(
        "ui.home_assistant_page_agent.ReportService.generate_filename",
        lambda *args: "report",
    )

    monkeypatch.setattr(
        "ui.home_assistant_page_agent.ReportService.save_all_reports",
        lambda **kwargs: report_called.append(True),
    )

    monkeypatch.setattr(
        "streamlit.success",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.rerun",
        lambda: None,
    )

    page.end_chat_section()

    assert len(report_called) == 1

####################################################
# Switch From Existing Chat To New Chat
####################################################

def test_chat_section_switch_to_new_chat(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True

    st.session_state["assistant_video"] = "video.mp4"

    st.session_state["assistant_previous_chat"] = "chat1"

    st.session_state["assistant_chat_id"] = "chat1"

    st.session_state["assistant_history"] = [
        {
            "user": "Hi",
            "assistant": "Hello",
        }
    ]

    monkeypatch.setattr(
        page.chat_service,
        "list_video_chats",
        lambda video: [],
    )

    monkeypatch.setattr(
        "streamlit.subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.info",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "streamlit.chat_input",
        lambda *args, **kwargs: None,
    )

    page.chat_section()

    assert st.session_state["assistant_chat_id"] is None

    assert st.session_state["assistant_history"] == []


####################################################
# Existing Chat Is Displayed
####################################################

def test_chat_section_display_history(
    monkeypatch,
):
    from pathlib import Path

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True
    st.session_state["assistant_video"] = "video.mp4"
    st.session_state["assistant_chat_id"] = None

    history = [
        {
            "user": "Hello",
            "assistant": "Hi",
        }
    ]

    monkeypatch.setattr(
        page.chat_service,
        "list_video_chats",
        lambda x: [Path("chat1.json")],
    )

    monkeypatch.setattr(
        page.chat_service,
        "load_chat_by_id",
        lambda x: history,
    )

    monkeypatch.setattr(
        st,
        "selectbox",
        lambda *args, **kwargs: "chat1",
    )

    monkeypatch.setattr(
        st,
        "chat_input",
        lambda *args, **kwargs: None,
    )

    messages = []

    class DummyChat:

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    def fake_chat_message(role):
        messages.append(role)
        return DummyChat()

    monkeypatch.setattr(
        st,
        "chat_message",
        fake_chat_message,
    )

    monkeypatch.setattr(
        st,
        "markdown",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "subheader",
        lambda *args, **kwargs: None,
    )

    page.chat_section()

    assert messages == [
        "user",
        "assistant",
    ]


####################################################
# Refresh Chat List
####################################################

def test_chat_section_refresh_chat_sessions(
    monkeypatch,
):
    from pathlib import Path

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True
    st.session_state["assistant_video"] = "video.mp4"

    chats = [
        Path("chat1.json"),
        Path("chat2.json"),
    ]

    monkeypatch.setattr(
        page.chat_service,
        "list_video_chats",
        lambda x: chats,
    )

    monkeypatch.setattr(
        st,
        "selectbox",
        lambda *args, **kwargs: "➕ New Chat",
    )

    monkeypatch.setattr(
        st,
        "chat_input",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "info",
        lambda *args, **kwargs: None,
    )

    page.chat_section()

    assert (
        st.session_state[
            "assistant_chat_sessions"
        ]
        == chats
    )


####################################################
# AI Response Saved To History
####################################################

def test_chat_section_history_updated(
    monkeypatch,
):

    page = HomeAssistantPageAgent()

    st.session_state.clear()

    st.session_state["assistant_ready"] = True
    st.session_state["assistant_video"] = "video.mp4"
    st.session_state["assistant_transcript"] = "Transcript"
    st.session_state["provider_name"] = "Ollama"
    st.session_state["model_name"] = "llama3"
    st.session_state["assistant_history"] = []

    monkeypatch.setattr(
        page.chat_service,
        "list_video_chats",
        lambda video: [],
    )

    monkeypatch.setattr(
        page.chat_service,
        "create_chat",
        lambda video: "chat1",
    )

    save_called = []

    monkeypatch.setattr(
        page.chat_service,
        "save_chat_by_id",
        lambda *args, **kwargs: save_called.append(True),
    )

    monkeypatch.setattr(
        st,
        "chat_input",
        lambda *args, **kwargs: "Hello",
    )

    monkeypatch.setattr(
        st,
        "subheader",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "info",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        st,
        "markdown",
        lambda *args, **kwargs: None,
    )

    class DummyMessage:

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(
        st,
        "chat_message",
        lambda *args, **kwargs: DummyMessage(),
    )

    class DummySpinner:

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(
        st,
        "spinner",
        lambda *args, **kwargs: DummySpinner(),
    )

    class DummyOrchestrator:

        def run_chat(self, context):
            return {
                "chat_answer": "Hi"
            }

    st.session_state["orchestrator"] = DummyOrchestrator()

    page.chat_section()

    assert st.session_state["assistant_chat_id"] == "chat1"
    assert len(save_called) == 1