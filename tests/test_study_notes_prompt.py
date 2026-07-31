from prompts.study_notes_prompt import STUDY_NOTES_PROMPT


def test_prompt_is_string():
    assert isinstance(STUDY_NOTES_PROMPT, str)


def test_prompt_not_empty():
    assert STUDY_NOTES_PROMPT.strip() != ""


def test_contains_title():
    assert "Create well-structured study notes from the transcript." in STUDY_NOTES_PROMPT


def test_contains_requirements():
    assert "Requirements:" in STUDY_NOTES_PROMPT


def test_contains_markdown_headings():
    assert "- Use clear Markdown headings." in STUDY_NOTES_PROMPT


def test_contains_main_concepts():
    assert "- Summarize the main concepts." in STUDY_NOTES_PROMPT


def test_contains_definitions():
    assert "- Include key definitions." in STUDY_NOTES_PROMPT


def test_contains_facts_examples():
    assert "- List important facts and examples." in STUDY_NOTES_PROMPT


def test_contains_highlight_terms():
    assert "- Highlight important terms." in STUDY_NOTES_PROMPT


def test_contains_revision_summary():
    assert "- End with a short revision summary." in STUDY_NOTES_PROMPT


def test_contains_unrelated_information():
    assert "- Do not include unrelated information." in STUDY_NOTES_PROMPT


def test_contains_concise():
    assert "- Keep the notes concise and easy to study." in STUDY_NOTES_PROMPT


def test_prompt_starts_correctly():
    assert STUDY_NOTES_PROMPT.strip().startswith(
        "Create well-structured study notes from the transcript."
    )