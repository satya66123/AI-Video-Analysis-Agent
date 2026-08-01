"""
tests/test_transcript_agent.py
"""

import os
from unittest.mock import MagicMock

import pytest

from agents.transcript_agent import TranscriptAgent


def make_service():

    service = MagicMock()

    service.TRANSCRIPT_FOLDER = "transcripts"

    service.transcribe.return_value = {

        "text": "This is the generated transcript.",

        "path": os.path.join(
            "transcripts",
            "video.txt",
        ),

        "model": "base",

        "chunks": 2,

        "word_count": len(
            "This is the generated transcript.".split()
        ),

        "character_count": len(
            "This is the generated transcript."
        ),

    }

    return service


def test_transcript_agent_creation():

    service = make_service()

    agent = TranscriptAgent(service)

    assert agent.name == "TranscriptAgent"

    assert agent.speech_service is service


def test_execute_success():

    service = make_service()

    agent = TranscriptAgent(service)

    progress_bar = MagicMock()

    status_text = MagicMock()

    context = {

        "audio": "audio/video.wav",

        "progress_bar": progress_bar,

        "status_text": status_text,

        "whisper_model": "base",

        "chunk_minutes": 10,

    }

    result = agent.execute(context)

    assert result["status"] == "transcript_generated"

    assert result["current_agent"] == "TranscriptAgent"

    assert (
        result["transcript"]
        == "This is the generated transcript."
    )

    expected_path = os.path.join(
        "transcripts",
        "video.txt",
    )

    assert result["transcript_path"] == expected_path

    metadata = result["transcript_metadata"]

    assert metadata["filename"] == "video.txt"

    assert metadata["filepath"] == expected_path

    assert metadata["model"] == "base"

    assert metadata["chunk_minutes"] == 10

    assert metadata["characters"] == len(
        "This is the generated transcript."
    )

    assert metadata["words"] == len(
        "This is the generated transcript.".split()
    )

    assert "generated_at" in metadata

    service.transcribe.assert_called_once_with(

        audio_path="audio/video.wav",

        progress_bar=progress_bar,

        status_text=status_text,

        model_name="base",

        chunk_minutes=10,

    )


def test_execute_default_values():

    service = make_service()

    service.transcribe.return_value = {

        "text": "Transcript",

        "path": os.path.join(
            "transcripts",
            "sample.txt",
        ),

        "model": "base",

        "chunks": 1,

        "word_count": 1,

        "character_count": len("Transcript"),

    }

    agent = TranscriptAgent(service)

    context = {

        "audio": "sample.wav",

    }

    result = agent.execute(context)

    assert result["status"] == "transcript_generated"

    service.transcribe.assert_called_once_with(

        audio_path="sample.wav",

        progress_bar=None,

        status_text=None,

        model_name="base",

        chunk_minutes=5,

    )

    metadata = result["transcript_metadata"]

    assert metadata["filename"] == "sample.txt"

    assert metadata["model"] == "base"

    assert metadata["chunk_minutes"] == 5


def test_execute_without_audio():

    service = make_service()

    agent = TranscriptAgent(service)

    with pytest.raises(

        ValueError,

        match="Workflow context does not contain an audio file.",

    ):

        agent.execute({})


def test_execute_transcription_failure():

    service = make_service()

    service.transcribe.return_value = None

    agent = TranscriptAgent(service)

    with pytest.raises(

        RuntimeError,

        match="Transcript generation failed.",

    ):

        agent.execute(

            {

                "audio": "video.wav",

            }

        )