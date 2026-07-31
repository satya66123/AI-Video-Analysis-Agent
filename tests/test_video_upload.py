from unittest.mock import patch

from pages.video_upload import show_video_upload


@patch("pages.video_upload.show_uploaded_videos")
@patch("pages.video_upload.show_uploader")
@patch("pages.video_upload.st.divider")
@patch("pages.video_upload.st.write")
@patch("pages.video_upload.st.header")
def test_show_video_upload(
    mock_header,
    mock_write,
    mock_divider,
    mock_uploader,
    mock_uploaded_videos,
):
    show_video_upload()

    mock_header.assert_called_once_with(
        "📤 Video Upload"
    )

    mock_write.assert_called_once_with(
        "Upload videos, preview them, and manage your video library."
    )

    assert mock_divider.call_count == 2

    mock_uploader.assert_called_once()

    mock_uploaded_videos.assert_called_once()