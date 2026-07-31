from prompts.meeting_prompt import MEETING_PROMPT


def test_prompt_is_string():
    assert isinstance(MEETING_PROMPT, str)


def test_prompt_not_empty():
    assert MEETING_PROMPT.strip() != ""


def test_contains_role():
    assert "You are an expert meeting assistant." in MEETING_PROMPT


def test_contains_analysis_instruction():
    assert "Analyze ONLY the transcript below." in MEETING_PROMPT


def test_contains_rules():
    assert "Rules:" in MEETING_PROMPT


def test_contains_not_meeting_rule():
    assert "This transcript is not a meeting transcript." in MEETING_PROMPT


def test_contains_summary_heading():
    assert "## Meeting Summary" in MEETING_PROMPT


def test_contains_participants():
    assert "## Participants" in MEETING_PROMPT


def test_contains_agenda():
    assert "## Agenda" in MEETING_PROMPT


def test_contains_discussion():
    assert "## Discussion" in MEETING_PROMPT


def test_contains_decisions():
    assert "## Decisions" in MEETING_PROMPT


def test_contains_action_items():
    assert "## Action Items" in MEETING_PROMPT


def test_contains_next_steps():
    assert "## Next Steps" in MEETING_PROMPT


def test_prompt_starts_correctly():
    assert MEETING_PROMPT.strip().startswith(
        "You are an expert meeting assistant."
    )