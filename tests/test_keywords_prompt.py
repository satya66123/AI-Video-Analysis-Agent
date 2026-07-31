from prompts.keywords_prompt import KEYWORDS_PROMPT


def test_prompt_is_string():
    assert isinstance(KEYWORDS_PROMPT, str)


def test_prompt_not_empty():
    assert KEYWORDS_PROMPT.strip() != ""


def test_contains_extract_instruction():
    assert "Extract the important keywords." in KEYWORDS_PROMPT


def test_contains_return_section():
    assert "Return:" in KEYWORDS_PROMPT


def test_contains_keyword():
    assert "- Keyword" in KEYWORDS_PROMPT


def test_contains_importance():
    assert "- Importance" in KEYWORDS_PROMPT


def test_contains_explanation():
    assert "- Short explanation" in KEYWORDS_PROMPT


def test_contains_markdown():
    assert "Use markdown." in KEYWORDS_PROMPT


def test_prompt_starts_correctly():
    assert KEYWORDS_PROMPT.strip().startswith(
        "Extract the important keywords."
    )


def test_prompt_ends_correctly():
    assert KEYWORDS_PROMPT.strip().endswith("Use markdown.")