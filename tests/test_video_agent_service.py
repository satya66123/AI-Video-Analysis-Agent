import io
import os

import pytest

from services.video_agent_service import VideoService


class DummyUploadFile:
    def __init__(self, name, content):
        self.name = name
        self._buffer = io.BytesIO(content)
        self.size = len(content)

    def read(self, size=-1):
        return self._buffer.read(size)

    def seek(self, pos):
        self._buffer.seek(pos)


class DummyProgressBar:
    def __init__(self):
        self.values = []

    def progress(self, value):
        self.values.append(value)


class DummyStatus:
    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(message)

    def success(self, message):
        self.messages.append(message)


@pytest.fixture
def upload_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(VideoService, "UPLOAD_FOLDER", str(tmp_path))
    return tmp_path


def test_save_video(upload_dir):
    file = DummyUploadFile("video.mp4", b"hello world")

    result = VideoService.save_video(file)

    assert isinstance(result, dict)

    assert result["original_filename"] == "video.mp4"
    assert result["size"] == len(b"hello world")

    assert os.path.exists(result["filepath"])
    assert result["filename"].endswith(".mp4")

    with open(result["filepath"], "rb") as f:
        assert f.read() == b"hello world"


def test_save_video_with_progress(upload_dir):
    file = DummyUploadFile("video.mp4", b"a" * 5000)

    progress = DummyProgressBar()
    status = DummyStatus()

    result = VideoService.save_video(
        file,
        progress_bar=progress,
        status_text=status,
    )

    assert os.path.exists(result["filepath"])
    assert progress.values[-1] == 1.0
    assert any("Upload Complete" in m for m in status.messages)


def test_list_videos(upload_dir):
    VideoService.save_video(DummyUploadFile("a.mp4", b"abc"))
    VideoService.save_video(DummyUploadFile("b.mp4", b"xyz"))

    videos = VideoService.list_videos()

    assert len(videos) == 2


def test_delete_video(upload_dir):
    result = VideoService.save_video(
        DummyUploadFile("video.mp4", b"abc")
    )

    assert VideoService.delete_video(result["filename"]) is True
    assert not os.path.exists(result["filepath"])


def test_delete_missing_video(upload_dir):
    assert VideoService.delete_video("missing.mp4") is False


def test_calculate_file_hash():
    file = DummyUploadFile("video.mp4", b"hello")

    h1 = VideoService.calculate_file_hash(file)

    file.seek(0)

    h2 = VideoService.calculate_file_hash(file)

    assert h1 == h2


def test_calculate_saved_file_hash(upload_dir):
    result = VideoService.save_video(
        DummyUploadFile("video.mp4", b"hello")
    )

    h = VideoService.calculate_saved_file_hash(
        result["filepath"]
    )

    assert isinstance(h, str)
    assert len(h) == 64


def test_duplicate_detection(upload_dir):
    VideoService.save_video(
        DummyUploadFile("one.mp4", b"same content")
    )

    duplicate = DummyUploadFile(
        "two.mp4",
        b"same content"
    )

    assert VideoService.is_duplicate(duplicate) is True


def test_non_duplicate_detection(upload_dir):
    VideoService.save_video(
        DummyUploadFile("one.mp4", b"video one")
    )

    different = DummyUploadFile(
        "two.mp4",
        b"completely different"
    )

    assert VideoService.is_duplicate(different) is False