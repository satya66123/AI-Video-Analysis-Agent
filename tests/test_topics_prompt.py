from prompts.topics_prompt import TOPICS_PROMPT


def test_prompt_is_string():
    assert isinstance(TOPICS_PROMPT, str)


def test_prompt_not_empty():
    assert TOPICS_PROMPT.strip() != ""


def test_contains_title():
    assert "Extract the major topics discussed." in TOPICS_PROMPT


def test_contains_for_each_topic():
    assert "For each topic include:" in TOPICS_PROMPT


def test_contains_topic_name():
    assert "- Topic name" in TOPICS_PROMPT


def test_contains_short_explanation():
    assert "- Short explanation" in TOPICS_PROMPT


def test_contains_markdown():
    assert "Use markdown." in TOPICS_PROMPT


def test_prompt_starts_correctly():
    assert TOPICS_PROMPT.strip().startswith(
        "Extract the major topics discussed."
    )


def test_prompt_ends_correctly():
    assert TOPICS_PROMPT.strip().endswith(
        "Use markdown."
    )