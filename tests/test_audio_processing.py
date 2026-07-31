import os
from unittest.mock import patch

from pages.audio_processing import show_audio_processing


class TestAudioProcessing:

    @patch("pages.audio_processing.st.info")
    @patch("pages.audio_processing.st.title")
    @patch("pages.audio_processing.VideoService.list_videos")
    def test_no_videos(
        self,
        mock_list_videos,
        mock_title,
        mock_info,
    ):
        mock_list_videos.return_value = []

        show_audio_processing()

        mock_title.assert_called_once_with(
            "🎵 Audio Processing"
        )

        mock_info.assert_called_once_with(
            "No uploaded videos found."
        )

    @patch("pages.audio_processing.show_extracted_audio")
    @patch("pages.audio_processing.st.divider")
    @patch("pages.audio_processing.st.button")
    @patch("pages.audio_processing.st.video")
    @patch("pages.audio_processing.st.selectbox")
    @patch("pages.audio_processing.VideoService.list_videos")
    def test_button_not_clicked(
        self,
        mock_list_videos,
        mock_selectbox,
        mock_video,
        mock_button,
        mock_divider,
        mock_show_audio,
    ):
        mock_list_videos.return_value = [
            "video.mp4"
        ]

        mock_selectbox.return_value = "video.mp4"

        mock_button.return_value = False

        show_audio_processing()

        import os

        mock_video.assert_called_once_with(
            os.path.join("uploads", "video.mp4")
        )

        mock_show_audio.assert_called_once()

    @patch("pages.audio_processing.show_extracted_audio")
    @patch("pages.audio_processing.st.audio")
    @patch("pages.audio_processing.AudioService.extract_audio")
    @patch("pages.audio_processing.st.empty")
    @patch("pages.audio_processing.st.progress")
    @patch("pages.audio_processing.st.button")
    @patch("pages.audio_processing.st.video")
    @patch("pages.audio_processing.st.selectbox")
    @patch("pages.audio_processing.VideoService.list_videos")
    @patch("pages.audio_processing.st.divider")
    def test_extract_audio_success(
        self,
        mock_divider,
        mock_list_videos,
        mock_selectbox,
        mock_video,
        mock_button,
        mock_progress,
        mock_empty,
        mock_extract,
        mock_audio,
        mock_show_audio,
    ):
        mock_list_videos.return_value = [
            "video.mp4"
        ]

        mock_selectbox.return_value = "video.mp4"

        mock_button.return_value = True

        progress = mock_progress.return_value
        status = mock_empty.return_value

        mock_extract.return_value = "audio/video.mp3"

        show_audio_processing()



        mock_extract.assert_called_once_with(
            os.path.join("uploads", "video.mp4"),
            progress,
            status,
        )

        mock_audio.assert_called_once_with(
            "audio/video.mp3"
        )

        mock_show_audio.assert_called_once()

    @patch("pages.audio_processing.show_extracted_audio")
    @patch("pages.audio_processing.st.audio")
    @patch("pages.audio_processing.AudioService.extract_audio")
    @patch("pages.audio_processing.st.empty")
    @patch("pages.audio_processing.st.progress")
    @patch("pages.audio_processing.st.button")
    @patch("pages.audio_processing.st.video")
    @patch("pages.audio_processing.st.selectbox")
    @patch("pages.audio_processing.VideoService.list_videos")
    @patch("pages.audio_processing.st.divider")
    def test_extract_audio_failure(
        self,
        mock_divider,
        mock_list_videos,
        mock_selectbox,
        mock_video,
        mock_button,
        mock_progress,
        mock_empty,
        mock_extract,
        mock_audio,
        mock_show_audio,
    ):
        mock_list_videos.return_value = [
            "video.mp4"
        ]

        mock_selectbox.return_value = "video.mp4"

        mock_button.return_value = True

        mock_extract.return_value = None

        show_audio_processing()

        mock_audio.assert_not_called()

        mock_show_audio.assert_called_once()