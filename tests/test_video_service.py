import hashlib
import io
import os
from unittest.mock import MagicMock, mock_open, patch

from services.video_service import VideoService


class TestVideoService:

    @patch("services.video_service.uuid.uuid4")
    @patch("builtins.open", new_callable=mock_open)
    @patch("services.video_service.os.makedirs")
    def test_save_video(
        self,
        mock_makedirs,
        mock_file,
        mock_uuid,
    ):
        mock_uuid.return_value = "1234"

        uploaded = MagicMock()
        uploaded.name = "video.mp4"
        uploaded.size = 4
        uploaded.read.side_effect = [
            b"ab",
            b"cd",
            b"",
        ]

        progress = MagicMock()
        status = MagicMock()

        result = VideoService.save_video(
            uploaded,
            progress,
            status,
        )

        expected = os.path.join(
            "uploads",
            "1234.mp4",
        )

        assert result == expected

        uploaded.seek.assert_any_call(0)

        mock_file.assert_called_once_with(
            expected,
            "wb",
        )

        handle = mock_file()

        handle.write.assert_any_call(b"ab")
        handle.write.assert_any_call(b"cd")

        progress.progress.assert_any_call(1.0)

        status.success.assert_called_once_with(
            "✅ Upload Complete (100%)"
        )

    @patch("services.video_service.os.listdir")
    @patch("services.video_service.os.makedirs")
    def test_list_videos(
        self,
        mock_makedirs,
        mock_listdir,
    ):
        mock_listdir.return_value = [
            "b.mp4",
            "a.mp4",
        ]

        result = VideoService.list_videos()

        assert result == [
            "a.mp4",
            "b.mp4",
        ]

    @patch("services.video_service.os.remove")
    @patch("services.video_service.os.path.exists")
    def test_delete_video_success(
        self,
        mock_exists,
        mock_remove,
    ):
        mock_exists.return_value = True

        result = VideoService.delete_video(
            "video.mp4"
        )

        assert result is True

        mock_remove.assert_called_once_with(
            os.path.join(
                "uploads",
                "video.mp4",
            )
        )

    @patch("services.video_service.os.path.exists")
    def test_delete_video_not_found(
        self,
        mock_exists,
    ):
        mock_exists.return_value = False

        result = VideoService.delete_video(
            "video.mp4"
        )

        assert result is False

    def test_calculate_file_hash(self):
        file = io.BytesIO(
            b"hello world"
        )

        expected = hashlib.sha256(
            b"hello world"
        ).hexdigest()

        result = VideoService.calculate_file_hash(
            file
        )

        assert result == expected

    @patch("builtins.open", new_callable=mock_open, read_data=b"hello world")
    def test_calculate_saved_file_hash(
        self,
        mock_file,
    ):
        expected = hashlib.sha256(
            b"hello world"
        ).hexdigest()

        result = VideoService.calculate_saved_file_hash(
            "sample.mp4"
        )

        assert result == expected

    @patch.object(
        VideoService,
        "calculate_saved_file_hash",
    )
    @patch.object(
        VideoService,
        "list_videos",
    )
    @patch.object(
        VideoService,
        "calculate_file_hash",
    )
    def test_is_duplicate_true(
        self,
        mock_uploaded_hash,
        mock_list,
        mock_saved_hash,
    ):
        mock_uploaded_hash.return_value = "abc"

        mock_list.return_value = [
            "video.mp4"
        ]

        mock_saved_hash.return_value = "abc"

        uploaded = MagicMock()

        assert (
            VideoService.is_duplicate(
                uploaded
            )
            is True
        )

    @patch.object(
        VideoService,
        "calculate_saved_file_hash",
    )
    @patch.object(
        VideoService,
        "list_videos",
    )
    @patch.object(
        VideoService,
        "calculate_file_hash",
    )
    def test_is_duplicate_false(
        self,
        mock_uploaded_hash,
        mock_list,
        mock_saved_hash,
    ):
        mock_uploaded_hash.return_value = "abc"

        mock_list.return_value = [
            "video.mp4"
        ]

        mock_saved_hash.return_value = "xyz"

        uploaded = MagicMock()

        assert (
            VideoService.is_duplicate(
                uploaded
            )
            is False
        )