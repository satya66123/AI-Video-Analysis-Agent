from prompts.summary_prompt import SUMMARY_PROMPT


def test_prompt_is_string():
    assert isinstance(SUMMARY_PROMPT, str)


def test_prompt_not_empty():
    assert SUMMARY_PROMPT.strip() != ""


def test_contains_title():
    assert "Create a professional summary of the transcript." in SUMMARY_PROMPT


def test_contains_requirements():
    assert "Requirements:" in SUMMARY_PROMPT


def test_contains_executive_summary():
    assert "- Executive Summary" in SUMMARY_PROMPT


def test_contains_main_discussion():
    assert "- Main Discussion" in SUMMARY_PROMPT


def test_contains_important_decisions():
    assert "- Important Decisions" in SUMMARY_PROMPT


def test_contains_important_events():
    assert "- Important Events" in SUMMARY_PROMPT


def test_contains_overall_conclusion():
    assert "- Overall Conclusion" in SUMMARY_PROMPT


def test_contains_markdown():
    assert "Use markdown formatting." in SUMMARY_PROMPT


def test_prompt_starts_correctly():
    assert SUMMARY_PROMPT.strip().startswith(
        "Create a professional summary of the transcript."
    )


def test_prompt_ends_correctly():
    assert SUMMARY_PROMPT.strip().endswith(
        "Use markdown formatting."
    )