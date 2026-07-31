from prompts.keypoints_prompt import KEYPOINTS_PROMPT


def test_prompt_is_string():
    assert isinstance(KEYPOINTS_PROMPT, str)


def test_prompt_not_empty():
    assert KEYPOINTS_PROMPT.strip() != ""


def test_contains_extract_instruction():
    assert "Extract the important key points." in KEYPOINTS_PROMPT


def test_contains_requirements():
    assert "Requirements:" in KEYPOINTS_PROMPT


def test_contains_bullet_list():
    assert "- Bullet list" in KEYPOINTS_PROMPT


def test_contains_important_concepts():
    assert "- Important concepts" in KEYPOINTS_PROMPT


def test_contains_announcements():
    assert "- Important announcements" in KEYPOINTS_PROMPT


def test_contains_conclusions():
    assert "- Important conclusions" in KEYPOINTS_PROMPT


def test_contains_markdown():
    assert "Use markdown." in KEYPOINTS_PROMPT


def test_prompt_starts_correctly():
    assert KEYPOINTS_PROMPT.strip().startswith(
        "Extract the important key points."
    )


def test_prompt_ends_correctly():
    assert KEYPOINTS_PROMPT.strip().endswith("Use markdown.")