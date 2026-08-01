"""
tests/test_upload_agent.py
"""

from unittest.mock import MagicMock

import pytest

from agents.upload_agent import UploadAgent


def make_uploaded_file():

    file = MagicMock()

    file.name = "video.mp4"

    file.size = 1024

    return file


def make_service():

    service = MagicMock()

    service.is_duplicate.return_value = False

    service.save_video.return_value = {

        "filepath": "uploads/video.mp4",

        "filename": "video.mp4",

        "original_filename": "video.mp4",

        "size": 1024,

    }

    return service


def test_upload_agent_creation():

    service = make_service()

    agent = UploadAgent(service)

    assert agent.name == "UploadAgent"

    assert agent.video_service is service


def test_execute_success():

    service = make_service()

    agent = UploadAgent(service)

    uploaded_file = make_uploaded_file()

    progress_bar = MagicMock()

    status_text = MagicMock()

    context = {

        "uploaded_file": uploaded_file,

        "progress_bar": progress_bar,

        "status_text": status_text,

    }

    result = agent.execute(context)

    assert result["status"] == "video_uploaded"

    assert result["duplicate"] is False

    assert result["current_agent"] == "UploadAgent"

    assert result["video"] == "uploads/video.mp4"

    metadata = result["video_metadata"]

    assert metadata["filename"] == "video.mp4"

    assert metadata["saved_path"] == "uploads/video.mp4"

    assert metadata["original_filename"] == "video.mp4"

    assert metadata["size"] == 1024

    assert metadata["extension"] == "mp4"

    assert "uploaded_at" in metadata

    service.is_duplicate.assert_called_once_with(
        uploaded_file
    )

    service.save_video.assert_called_once_with(

        uploaded_file=uploaded_file,

        progress_bar=progress_bar,

        status_text=status_text,

    )


def test_execute_duplicate():

    service = make_service()
    service.is_duplicate.return_value = True

    agent = UploadAgent(service)

    uploaded_file = make_uploaded_file()

    context = {
        "uploaded_file": uploaded_file,
    }

    with pytest.raises(
        ValueError,
        match="Video already uploaded.",
    ):
        agent.execute(context)

    service.save_video.assert_not_called()


def test_execute_missing_uploaded_file():

    service = make_service()

    agent = UploadAgent(service)

    with pytest.raises(

        ValueError,

        match="No uploaded file found in workflow context.",

    ):

        agent.execute({})