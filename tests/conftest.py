import tempfile
from pathlib import Path

import pytest


class FakeSessionState(dict):
    """
    Fake replacement for streamlit.session_state.
    Supports both:
        session["key"]
        session.key
    """

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        self[name] = value


@pytest.fixture
def session_state():
    return FakeSessionState()


@pytest.fixture
def sample_provider():
    return "Ollama"


@pytest.fixture
def sample_model():
    return "qwen2.5:1.5b"


@pytest.fixture
def sample_question():
    return "Summarize this transcript."


@pytest.fixture
def sample_answer():
    return "This is a summary."


@pytest.fixture
def sample_transcript():
    return (
        "Artificial Intelligence is transforming education. "
        "Machine learning improves automation."
    )


@pytest.fixture
def sample_analysis():
    return """
# Summary

Artificial Intelligence improves automation.
"""


@pytest.fixture
def sample_chat_history():
    return [
        {
            "user": "Hello",
            "assistant": "Hi!"
        },
        {
            "user": "Summarize",
            "assistant": "Summary"
        }
    ]


@pytest.fixture
def sample_video_metadata():
    return {
        "filename": "video.mp4",
        "duration": 120,
        "fps": 30,
        "resolution": "1920x1080",
        "size": "100 MB"
    }


@pytest.fixture
def sample_audio_metadata():
    return {
        "filename": "audio.wav",
        "duration": 120,
        "sample_rate": 44100,
        "channels": 2,
        "size": "15 MB"
    }


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def transcript_file(temp_dir):
    file = temp_dir / "sample.txt"
    file.write_text(
        "This is a sample transcript.",
        encoding="utf-8"
    )
    return file


@pytest.fixture
def markdown_file(temp_dir):
    file = temp_dir / "sample.md"
    file.write_text(
        "# Sample",
        encoding="utf-8"
    )
    return file


@pytest.fixture
def html_file(temp_dir):
    file = temp_dir / "sample.html"
    file.write_text(
        "<h1>Sample</h1>",
        encoding="utf-8"
    )
    return file


@pytest.fixture
def pdf_file(temp_dir):
    file = temp_dir / "sample.pdf"
    file.touch()
    return file


@pytest.fixture
def txt_file(temp_dir):
    file = temp_dir / "sample.txt"
    file.write_text(
        "Sample",
        encoding="utf-8"
    )
    return file