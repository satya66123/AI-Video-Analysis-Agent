from pathlib import Path
import tomllib


def load_config():
    config_path = Path(".streamlit/config.toml")
    assert config_path.exists(), ".streamlit/config.toml not found"

    with config_path.open("rb") as f:
        return tomllib.load(f)


def test_server_section_exists():
    config = load_config()
    assert "server" in config


def test_client_section_exists():
    config = load_config()
    assert "client" in config


def test_max_upload_size():
    config = load_config()
    assert config["server"]["maxUploadSize"] == 1024


def test_max_upload_size_type():
    config = load_config()
    assert isinstance(config["server"]["maxUploadSize"], int)


def test_sidebar_navigation():
    config = load_config()
    assert config["client"]["showSidebarNavigation"] is False


def test_server_key_exists():
    config = load_config()
    assert "maxUploadSize" in config["server"]


def test_client_key_exists():
    config = load_config()
    assert "showSidebarNavigation" in config["client"]


def test_server_not_empty():
    config = load_config()
    assert len(config["server"]) > 0


def test_client_not_empty():
    config = load_config()
    assert len(config["client"]) > 0