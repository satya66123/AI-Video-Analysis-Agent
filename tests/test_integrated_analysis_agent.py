import streamlit as st
import pytest

from agents.integrated_analysis_agent import (
    IntegratedAnalysisAgent,
)


@pytest.fixture(autouse=True)
def clear_session_state():

    st.session_state.clear()

    yield

    st.session_state.clear()


@pytest.fixture
def agent():

    return IntegratedAnalysisAgent()


########################################################
# Success
########################################################

def test_load_existing_video_success(
    monkeypatch,
    agent,
):

    monkeypatch.setattr(

        agent.video_service,

        "load_metadata",

        lambda filename: {

            "filename": filename,

            "duration": "10 sec",

        },

    )

    monkeypatch.setattr(

        agent.audio_service,

        "load_metadata",

        lambda filename: {

            "filename": f"{filename}.mp3",

            "duration": "10 sec",

        },

    )

    monkeypatch.setattr(

        "services.speech_agent_service.SpeechService.load_transcript",

        lambda filename: "Sample Transcript",

    )

    monkeypatch.setattr(

        agent.analysis_service,

        "find_latest_analysis",

        lambda stem: "analysis.json",

    )

    monkeypatch.setattr(

        agent.analysis_service,

        "load_analysis",

        lambda filename: {

            "summary": "AI Summary",

        },

    )

    monkeypatch.setattr(

        agent.chat_service,

        "load_chat",

        lambda filename: [

            {

                "user": "Hi",

                "assistant": "Hello",

            }

        ],

    )

    result = agent.load_existing_video(

        "video.mp4"

    )

    assert result is True

    assert st.session_state[
        "assistant_video"
    ] == "video.mp4"

    assert st.session_state[
        "assistant_video_metadata"
    ]["filename"] == "video.mp4"

    assert st.session_state[
        "assistant_audio_metadata"
    ]["duration"] == "10 sec"

    assert st.session_state[
        "assistant_transcript"
    ] == "Sample Transcript"

    assert st.session_state[
        "assistant_analysis"
    ]["summary"] == "AI Summary"

    assert st.session_state[
        "assistant_history"
    ][0]["user"] == "Hi"

    assert st.session_state[
        "assistant_ready"
    ] is True


########################################################
# Transcript Missing
########################################################

def test_load_existing_video_transcript_missing(
    monkeypatch,
    agent,
):

    monkeypatch.setattr(

        agent.video_service,

        "load_metadata",

        lambda filename: {},

    )

    monkeypatch.setattr(

        agent.audio_service,

        "load_metadata",

        lambda filename: {},

    )

    monkeypatch.setattr(

        "services.speech_agent_service.SpeechService.load_transcript",

        lambda filename: None,

    )

    result = agent.load_existing_video(

        "video.mp4"

    )

    assert result is False


########################################################
# Video Metadata Exception
########################################################

def test_video_metadata_exception(
    monkeypatch,
    agent,
):

    def raise_error(filename):

        raise Exception()

    monkeypatch.setattr(

        agent.video_service,

        "load_metadata",

        raise_error,

    )

    monkeypatch.setattr(

        agent.audio_service,

        "load_metadata",

        lambda filename: {},

    )

    monkeypatch.setattr(

        "services.speech_agent_service.SpeechService.load_transcript",

        lambda filename: "Transcript",

    )

    monkeypatch.setattr(

        agent.analysis_service,

        "find_latest_analysis",

        lambda stem: None,

    )

    monkeypatch.setattr(

        agent.chat_service,

        "load_chat",

        lambda filename: [],

    )

    result = agent.load_existing_video(

        "video.mp4"

    )

    assert result is True

    assert st.session_state[
        "assistant_video_metadata"
    ] == {}


########################################################
# Audio Metadata Exception
########################################################

def test_audio_metadata_exception(
    monkeypatch,
    agent,
):

    monkeypatch.setattr(

        agent.video_service,

        "load_metadata",

        lambda filename: {},

    )

    def raise_audio(filename):

        raise Exception()

    monkeypatch.setattr(

        agent.audio_service,

        "load_metadata",

        raise_audio,

    )

    monkeypatch.setattr(

        "services.speech_agent_service.SpeechService.load_transcript",

        lambda filename: "Transcript",

    )

    monkeypatch.setattr(

        agent.analysis_service,

        "find_latest_analysis",

        lambda stem: None,

    )

    monkeypatch.setattr(

        agent.chat_service,

        "load_chat",

        lambda filename: [],

    )

    result = agent.load_existing_video(

        "video.mp4"

    )

    assert result is True

    assert st.session_state[
        "assistant_audio_metadata"
    ] == {}


########################################################
# Analysis Missing
########################################################

def test_analysis_missing(
    monkeypatch,
    agent,
):

    monkeypatch.setattr(

        agent.video_service,

        "load_metadata",

        lambda filename: {},

    )

    monkeypatch.setattr(

        agent.audio_service,

        "load_metadata",

        lambda filename: {},

    )

    monkeypatch.setattr(

        "services.speech_agent_service.SpeechService.load_transcript",

        lambda filename: "Transcript",

    )

    monkeypatch.setattr(

        agent.analysis_service,

        "find_latest_analysis",

        lambda stem: None,

    )

    monkeypatch.setattr(

        agent.chat_service,

        "load_chat",

        lambda filename: [],

    )

    result = agent.load_existing_video(

        "video.mp4"

    )

    assert result is True

    assert st.session_state[
        "assistant_analysis"
    ] == ""


########################################################
# Chat Missing
########################################################

def test_chat_missing(
    monkeypatch,
    agent,
):

    monkeypatch.setattr(

        agent.video_service,

        "load_metadata",

        lambda filename: {},

    )

    monkeypatch.setattr(

        agent.audio_service,

        "load_metadata",

        lambda filename: {},

    )

    monkeypatch.setattr(

        "services.speech_agent_service.SpeechService.load_transcript",

        lambda filename: "Transcript",

    )

    monkeypatch.setattr(

        agent.analysis_service,

        "find_latest_analysis",

        lambda stem: None,

    )

    def raise_chat(filename):

        raise Exception()

    monkeypatch.setattr(

        agent.chat_service,

        "load_chat",

        raise_chat,

    )

    result = agent.load_existing_video(

        "video.mp4"

    )

    assert result is True

    assert st.session_state[
        "assistant_history"
    ] == []