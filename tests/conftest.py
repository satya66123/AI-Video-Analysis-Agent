"""
tests/conftest.py
"""

from pathlib import Path

import pytest


@pytest.fixture
def sample_video():

    return Path("tests/data/sample.mp4")


@pytest.fixture
def sample_transcript():

    return """
This is a sample transcript for testing.
"""


@pytest.fixture
def sample_analysis():

    return {
        "summary": "Sample Summary",
        "key_points": [
            "Point 1",
            "Point 2",
        ],
        "sentiment": "Positive",
        "action_items": [
            "Action 1",
            "Action 2",
        ],
    }