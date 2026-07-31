from unittest.mock import MagicMock, mock_open, patch

from components.uploaded_videos import show_uploaded_videos


class TestUploadedVideos:

    @patch("components.uploaded_videos.st.info")
    @patch("components.uploaded_videos.VideoService.list_videos")
    @patch("components.uploaded_videos.st.header")
    @patch("components.uploaded_videos.st.divider")
    def test_show_uploaded_videos_empty(
        self,
        mock_divider,
        mock_header,
        mock_list,
        mock_info,
    ):
        mock_list.return_value = []

        show_uploaded_videos()

        mock_divider.assert_called_once()
        mock_header.assert_called_once_with(
            "📁 Uploaded Videos"
        )

        mock_info.assert_called_once_with(
            "No uploaded videos."
        )

    @patch("builtins.open", new_callable=mock_open, read_data=b"video")
    @patch("components.uploaded_videos.st.download_button")
    @patch("components.uploaded_videos.st.button")
    @patch("components.uploaded_videos.st.columns")
    @patch("components.uploaded_videos.st.expander")
    @patch("components.uploaded_videos.st.json")
    @patch("components.uploaded_videos.st.video")
    @patch("components.uploaded_videos.VideoMetadata.get_metadata")
    @patch("components.uploaded_videos.VideoService.list_videos")
    @patch("components.uploaded_videos.st.header")
    @patch("components.uploaded_videos.st.divider")
    def test_show_uploaded_videos_success(
        self,
        mock_divider,
        mock_header,
        mock_list,
        mock_metadata,
        mock_video,
        mock_json,
        mock_expander,
        mock_columns,
        mock_button,
        mock_download,
        mock_open_file,
    ):
        mock_list.return_value = ["sample.mp4"]

        mock_metadata.return_value = {
            "duration": 120,
            "size": "10 MB",
        }

        mock_button.return_value = False

        expander = MagicMock()
        expander.__enter__.return_value = expander
        expander.__exit__.return_value = False

        mock_expander.return_value = expander

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

        show_uploaded_videos()

        mock_video.assert_called_once()

        mock_json.assert_called_once_with(
            {
                "duration": 120,
                "size": "10 MB",
            }
        )

        mock_download.assert_called_once()

        kwargs = mock_download.call_args.kwargs

        assert kwargs["file_name"] == "sample.mp4"

    @patch("components.uploaded_videos.st.rerun")
    @patch("components.uploaded_videos.VideoService.delete_video")
    @patch("builtins.open", new_callable=mock_open, read_data=b"video")
    @patch("components.uploaded_videos.st.download_button")
    @patch("components.uploaded_videos.st.button")
    @patch("components.uploaded_videos.st.columns")
    @patch("components.uploaded_videos.st.expander")
    @patch("components.uploaded_videos.st.json")
    @patch("components.uploaded_videos.st.video")
    @patch("components.uploaded_videos.VideoMetadata.get_metadata")
    @patch("components.uploaded_videos.VideoService.list_videos")
    def test_show_uploaded_videos_delete(
        self,
        mock_list,
        mock_metadata,
        mock_video,
        mock_json,
        mock_expander,
        mock_columns,
        mock_button,
        mock_download,
        mock_open_file,
        mock_delete,
        mock_rerun,
    ):
        mock_list.return_value = ["sample.mp4"]

        mock_metadata.return_value = {}

        mock_button.return_value = True

        expander = MagicMock()
        expander.__enter__.return_value = expander
        expander.__exit__.return_value = False

        mock_expander.return_value = expander

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

        show_uploaded_videos()

        mock_delete.assert_called_once_with(
            "sample.mp4"
        )

        mock_rerun.assert_called_once()