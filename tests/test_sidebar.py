import pytest
from unittest.mock import MagicMock, patch

from components.sidebar import show_sidebar


# ==========================================================
# Fixture
# ==========================================================

@pytest.fixture
def mock_provider():
    provider = MagicMock()
    provider.health_check.return_value = True
    return provider


# ==========================================================
# Sidebar
# ==========================================================

@patch("components.sidebar.ProviderFactory.get_provider")
@patch("components.sidebar.ModelManager.get_models")
@patch("components.sidebar.st.sidebar.error")
@patch("components.sidebar.st.sidebar.success")
@patch("components.sidebar.st.sidebar.selectbox")
@patch("components.sidebar.st.sidebar.radio")
@patch("components.sidebar.st.sidebar.title")
@patch("components.sidebar.st.session_state", {})
def test_show_sidebar_success(
    mock_title,
    mock_radio,
    mock_selectbox,
    mock_success,
    mock_error,
    mock_get_models,
    mock_get_provider,
    mock_provider,
):
    mock_radio.return_value = "Dashboard"

    mock_selectbox.side_effect = [
        "Ollama",
        "llama3.1:8b",
    ]

    mock_get_provider.return_value = mock_provider

    mock_get_models.return_value = [
        "llama3.1:8b",
        "qwen3:8b",
    ]

    page, provider, model = show_sidebar()

    assert page == "Dashboard"
    assert provider == "Ollama"
    assert model == "llama3.1:8b"

    mock_get_provider.assert_called_once_with("Ollama")
    mock_get_models.assert_called_once_with("Ollama")

    mock_success.assert_called_once_with(
        "Provider Connected"
    )

    mock_error.assert_not_called()


@patch("components.sidebar.ProviderFactory.get_provider")
@patch("components.sidebar.ModelManager.get_models")
@patch("components.sidebar.st.sidebar.error")
@patch("components.sidebar.st.sidebar.success")
@patch("components.sidebar.st.sidebar.selectbox")
@patch("components.sidebar.st.sidebar.radio")
@patch("components.sidebar.st.sidebar.title")
@patch("components.sidebar.st.session_state", {})
def test_show_sidebar_provider_unavailable(
    mock_title,
    mock_radio,
    mock_selectbox,
    mock_success,
    mock_error,
    mock_get_models,
    mock_get_provider,
):
    provider = MagicMock()
    provider.health_check.return_value = False

    mock_radio.return_value = "Reports"

    mock_selectbox.side_effect = [
        "OpenAI",
        "gpt-4.1",
    ]

    mock_get_provider.return_value = provider

    mock_get_models.return_value = [
        "gpt-4.1",
    ]

    page, provider_name, model = show_sidebar()

    assert page == "Reports"
    assert provider_name == "OpenAI"
    assert model == "gpt-4.1"

    mock_error.assert_called_once_with(
        "Provider Not Available"
    )

    mock_success.assert_not_called()