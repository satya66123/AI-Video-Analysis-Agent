from unittest.mock import MagicMock, patch

from components.uploader import show_uploader


class TestUploader:

    @patch("components.uploader.st.file_uploader")
    def test_show_uploader_no_file(
        self,
        mock_file_uploader,
    ):
        mock_file_uploader.return_value = None

        show_uploader()

        mock_file_uploader.assert_called_once()


    @patch("components.uploader.st.error")
    @patch("components.uploader.FileValidator.validate")
    @patch("components.uploader.st.button")
    @patch("components.uploader.st.info")
    @patch("components.uploader.st.file_uploader")
    def test_show_uploader_invalid_file(
        self,
        mock_file_uploader,
        mock_info,
        mock_button,
        mock_validate,
        mock_error,
    ):
        uploaded = MagicMock()
        uploaded.name = "video.mp4"

        mock_file_uploader.return_value = uploaded
        mock_button.return_value = True

        mock_validate.return_value = (
            False,
            "Invalid file"
        )

        show_uploader()

        mock_info.assert_called_once_with(
            "Selected File: video.mp4"
        )

        mock_error.assert_called_once_with(
            "Invalid file"
        )


    @patch("components.uploader.st.warning")
    @patch("components.uploader.VideoService.is_duplicate")
    @patch("components.uploader.FileValidator.validate")
    @patch("components.uploader.st.button")
    @patch("components.uploader.st.info")
    @patch("components.uploader.st.file_uploader")
    def test_show_uploader_duplicate(
        self,
        mock_file_uploader,
        mock_info,
        mock_button,
        mock_validate,
        mock_duplicate,
        mock_warning,
    ):
        uploaded = MagicMock()
        uploaded.name = "video.mp4"

        mock_file_uploader.return_value = uploaded
        mock_button.return_value = True

        mock_validate.return_value = (
            True,
            ""
        )

        mock_duplicate.return_value = True

        show_uploader()

        mock_warning.assert_called_once_with(
            "⚠ This video already exists."
        )


    @patch("components.uploader.st.rerun")
    @patch("components.uploader.show_metadata")
    @patch("components.uploader.VideoMetadata.get_metadata")
    @patch("components.uploader.st.video")
    @patch("components.uploader.st.success")
    @patch("components.uploader.VideoService.save_video")
    @patch("components.uploader.st.empty")
    @patch("components.uploader.st.progress")
    @patch("components.uploader.VideoService.is_duplicate")
    @patch("components.uploader.FileValidator.validate")
    @patch("components.uploader.st.button")
    @patch("components.uploader.st.info")
    @patch("components.uploader.st.file_uploader")
    def test_show_uploader_success(
        self,
        mock_file_uploader,
        mock_info,
        mock_button,
        mock_validate,
        mock_duplicate,
        mock_progress,
        mock_empty,
        mock_save,
        mock_success,
        mock_video,
        mock_metadata,
        mock_show_metadata,
        mock_rerun,
    ):
        uploaded = MagicMock()
        uploaded.name = "video.mp4"

        mock_file_uploader.return_value = uploaded
        mock_button.return_value = True

        mock_validate.return_value = (
            True,
            ""
        )

        mock_duplicate.return_value = False

        progress = MagicMock()
        status = MagicMock()

        mock_progress.return_value = progress
        mock_empty.return_value = status

        mock_save.return_value = "uploads/video.mp4"

        metadata = {
            "duration": 120,
            "size": "10 MB",
        }

        mock_metadata.return_value = metadata

        show_uploader()

        mock_save.assert_called_once_with(
            uploaded,
            progress,
            status,
        )

        progress.progress.assert_called_once_with(100)

        mock_success.assert_called_once_with(
            "✅ Video Uploaded Successfully"
        )

        mock_video.assert_called_once_with(
            "uploads/video.mp4"
        )

        mock_show_metadata.assert_called_once_with(
            metadata
        )

        mock_rerun.assert_called_once()


    @patch("components.uploader.st.rerun")
    @patch("components.uploader.show_metadata")
    @patch("components.uploader.VideoMetadata.get_metadata")
    @patch("components.uploader.st.video")
    @patch("components.uploader.st.success")
    @patch("components.uploader.VideoService.save_video")
    @patch("components.uploader.st.empty")
    @patch("components.uploader.st.progress")
    @patch("components.uploader.VideoService.is_duplicate")
    @patch("components.uploader.FileValidator.validate")
    @patch("components.uploader.st.button")
    @patch("components.uploader.st.info")
    @patch("components.uploader.st.file_uploader")
    def test_show_uploader_no_metadata(
        self,
        mock_file_uploader,
        mock_info,
        mock_button,
        mock_validate,
        mock_duplicate,
        mock_progress,
        mock_empty,
        mock_save,
        mock_success,
        mock_video,
        mock_metadata,
        mock_show_metadata,
        mock_rerun,
    ):
        uploaded = MagicMock()
        uploaded.name = "video.mp4"

        mock_file_uploader.return_value = uploaded
        mock_button.return_value = True

        mock_validate.return_value = (
            True,
            ""
        )

        mock_duplicate.return_value = False

        progress = MagicMock()
        status = MagicMock()

        mock_progress.return_value = progress
        mock_empty.return_value = status

        mock_save.return_value = "uploads/video.mp4"

        mock_metadata.return_value = None

        show_uploader()

        mock_show_metadata.assert_not_called()

        mock_rerun.assert_called_once()