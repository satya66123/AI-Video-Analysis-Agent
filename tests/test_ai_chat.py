from unittest.mock import patch

from pages.ai_chat import show_ai_chat


@patch("pages.ai_chat.show_ai_chat_component")
def test_show_ai_chat(mock_show_component):
    show_ai_chat()

    mock_show_component.assert_called_once()