from prompts.actionitems_prompt import ACTIONITEMS_PROMPT


def test_prompt_is_string():
    assert isinstance(ACTIONITEMS_PROMPT, str)


def test_prompt_not_empty():
    assert ACTIONITEMS_PROMPT.strip() != ""


def test_contains_extract_instruction():
    assert "Extract all action items." in ACTIONITEMS_PROMPT


def test_contains_task():
    assert "- Task" in ACTIONITEMS_PROMPT


def test_contains_owner():
    assert "- Owner (if mentioned)" in ACTIONITEMS_PROMPT


def test_contains_deadline():
    assert "- Deadline (if mentioned)" in ACTIONITEMS_PROMPT


def test_contains_markdown_table_instruction():
    assert "Use markdown table." in ACTIONITEMS_PROMPT


def test_contains_include_section():
    assert "Include:" in ACTIONITEMS_PROMPT


def test_prompt_starts_with_extract():
    assert ACTIONITEMS_PROMPT.strip().startswith("Extract all action items.")


def test_prompt_ends_with_markdown_table():
    assert ACTIONITEMS_PROMPT.strip().endswith("Use markdown table.")