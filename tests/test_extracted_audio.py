import os
from unittest.mock import MagicMock, mock_open, patch

from components.extracted_audio import show_extracted_audio


class TestExtractedAudio:

    @patch("components.extracted_audio.AudioService.list_audio")
    @patch("components.extracted_audio.st.info")
    @patch("components.extracted_audio.st.subheader")
    def test_show_extracted_audio_no_files(
        self,
        mock_subheader,
        mock_info,
        mock_list_audio,
    ):
        mock_list_audio.return_value = []

        show_extracted_audio()

        mock_subheader.assert_called_once_with(
            "🎵 Extracted Audio"
        )

        mock_info.assert_called_once_with(
            "No extracted audio found."
        )

    @patch("builtins.open", new_callable=mock_open, read_data=b"audio")
    @patch("components.extracted_audio.st.download_button")
    @patch("components.extracted_audio.st.button")
    @patch("components.extracted_audio.st.columns")
    @patch("components.extracted_audio.show_audio_metadata")
    @patch("components.extracted_audio.AudioMetadata.get_metadata")
    @patch("components.extracted_audio.st.audio")
    @patch("components.extracted_audio.st.markdown")
    @patch("components.extracted_audio.st.container")
    @patch("components.extracted_audio.AudioService.list_audio")
    @patch("components.extracted_audio.st.subheader")
    def test_show_extracted_audio_success(
        self,
        mock_subheader,
        mock_list_audio,
        mock_container,
        mock_markdown,
        mock_audio,
        mock_get_metadata,
        mock_show_metadata,
        mock_columns,
        mock_button,
        mock_download_button,
        mock_open_file,
    ):
        mock_list_audio.return_value = [
            "d5241d3e-adac-40fd-ad7b-b4de56136f67.mp3"
        ]

        metadata = {
            "duration": 120,
            "bitrate": 320,
        }

        mock_get_metadata.return_value = metadata

        container = MagicMock()
        container.__enter__.return_value = container
        container.__exit__.return_value = False
        mock_container.return_value = container

        col1 = MagicMock()
        col2 = MagicMock()

        col1.__enter__.return_value = col1
        col1.__exit__.return_value = False

        col2.__enter__.return_value = col2
        col2.__exit__.return_value = False

        mock_columns.return_value = (
            col1,
            col2,
        )

        mock_button.return_value = False

        show_extracted_audio()



        mock_subheader.assert_called_once_with(
            "🎵 Extracted Audio"
        )

        mock_container.assert_called_once_with(
            border=True
        )

        mock_markdown.assert_called_once_with(
            "### 🎵 d5241d3e-adac-40fd-ad7b-b4de56136f67.mp3"
        )

        expected_path = os.path.join("audio", "d5241d3e-adac-40fd-ad7b-b4de56136f67.mp3")

        mock_audio.assert_called_once_with(expected_path)
        mock_get_metadata.assert_called_once_with(expected_path)

        mock_show_metadata.assert_called_once_with(
            metadata
        )

        mock_download_button.assert_called_once()

        mock_button.assert_called_once_with(
            "🗑 Delete Audio",
            key="delete_d5241d3e-adac-40fd-ad7b-b4de56136f67.mp3",
            use_container_width=True,
        )

    @patch("builtins.open", new_callable=mock_open, read_data=b"audio")
    @patch("components.extracted_audio.st.rerun")
    @patch("components.extracted_audio.st.success")
    @patch("components.extracted_audio.AudioService.delete_audio")
    @patch("components.extracted_audio.st.download_button")
    @patch("components.extracted_audio.st.button")
    @patch("components.extracted_audio.st.columns")
    @patch("components.extracted_audio.show_audio_metadata")
    @patch("components.extracted_audio.AudioMetadata.get_metadata")
    @patch("components.extracted_audio.st.audio")
    @patch("components.extracted_audio.st.markdown")
    @patch("components.extracted_audio.st.container")
    @patch("components.extracted_audio.AudioService.list_audio")
    def test_show_extracted_audio_delete(
        self,
        mock_list_audio,
        mock_container,
        mock_markdown,
        mock_audio,
        mock_get_metadata,
        mock_show_metadata,
        mock_columns,
        mock_button,
        mock_download_button,
        mock_delete_audio,
        mock_success,
        mock_rerun,
        mock_open_file,
    ):
        mock_list_audio.return_value = [
            "d5241d3e-adac-40fd-ad7b-b4de56136f67.mp3"
        ]

        mock_get_metadata.return_value = {
            "duration": 100
        }

        container = MagicMock()
        container.__enter__.return_value = container
        container.__exit__.return_value = False
        mock_container.return_value = container

        col1 = MagicMock()
        col2 = MagicMock()

        col1.__enter__.return_value = col1
        col1.__exit__.return_value = False

        col2.__enter__.return_value = col2
        col2.__exit__.return_value = False

        mock_columns.return_value = (
            col1,
            col2,
        )

        mock_button.return_value = True

        show_extracted_audio()

        mock_delete_audio.assert_called_once_with(
            "d5241d3e-adac-40fd-ad7b-b4de56136f67.mp3"
        )

        mock_success.assert_called_once_with(
            "Audio deleted successfully."
        )

        mock_rerun.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data=b"audio")
    @patch("components.extracted_audio.st.download_button")
    @patch("components.extracted_audio.st.button")
    @patch("components.extracted_audio.st.columns")
    @patch("components.extracted_audio.show_audio_metadata")
    @patch("components.extracted_audio.AudioMetadata.get_metadata")
    @patch("components.extracted_audio.st.audio")
    @patch("components.extracted_audio.st.markdown")
    @patch("components.extracted_audio.st.container")
    @patch("components.extracted_audio.AudioService.list_audio")
    def test_show_extracted_audio_no_metadata(
        self,
        mock_list_audio,
        mock_container,
        mock_markdown,
        mock_audio,
        mock_get_metadata,
        mock_show_metadata,
        mock_columns,
        mock_button,
        mock_download_button,
        mock_open_file,
    ):
        mock_list_audio.return_value = [
            "d5241d3e-adac-40fd-ad7b-b4de56136f67.mp3"
        ]

        mock_get_metadata.return_value = None

        container = MagicMock()
        container.__enter__.return_value = container
        container.__exit__.return_value = False
        mock_container.return_value = container

        col1 = MagicMock()
        col2 = MagicMock()

        col1.__enter__.return_value = col1
        col1.__exit__.return_value = False

        col2.__enter__.return_value = col2
        col2.__exit__.return_value = False

        mock_columns.return_value = (
            col1,
            col2,
        )

        mock_button.return_value = False

        show_extracted_audio()

        mock_get_metadata.assert_called_once()

        mock_show_metadata.assert_not_called()

        mock_download_button.assert_called_once()