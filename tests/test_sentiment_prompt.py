from prompts.sentiment_prompt import SENTIMENT_PROMPT


def test_prompt_is_string():
    assert isinstance(SENTIMENT_PROMPT, str)


def test_prompt_not_empty():
    assert SENTIMENT_PROMPT.strip() != ""


def test_contains_analysis_instruction():
    assert "Analyze the sentiment of the transcript." in SENTIMENT_PROMPT


def test_contains_include():
    assert "Include:" in SENTIMENT_PROMPT


def test_contains_overall_sentiment():
    assert "- Overall sentiment" in SENTIMENT_PROMPT


def test_contains_positive_points():
    assert "- Positive points" in SENTIMENT_PROMPT


def test_contains_negative_points():
    assert "- Negative points" in SENTIMENT_PROMPT


def test_contains_neutral_observations():
    assert "- Neutral observations" in SENTIMENT_PROMPT


def test_contains_explanation():
    assert "Explain why." in SENTIMENT_PROMPT


def test_contains_markdown():
    assert "Use markdown." in SENTIMENT_PROMPT


def test_prompt_starts_correctly():
    assert SENTIMENT_PROMPT.strip().startswith(
        "Analyze the sentiment of the transcript."
    )


def test_prompt_ends_correctly():
    assert SENTIMENT_PROMPT.strip().endswith("Use markdown.")