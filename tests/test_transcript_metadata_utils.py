from datetime import datetime
from unittest.mock import mock_open, patch, MagicMock

from utils.transcript_metadata import TranscriptMetadata


class TestTranscriptMetadataUtils:

    @patch("utils.transcript_metadata.os.path.getctime")
    @patch("utils.transcript_metadata.os.path.getsize")
    @patch("utils.transcript_metadata.datetime")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="Hello world\nThis is transcript",
    )
    def test_get_metadata_success(
        self,
        mock_file,
        mock_datetime,
        mock_getsize,
        mock_getctime,
    ):
        mock_getsize.return_value = 2048
        mock_getctime.return_value = 1000

        dt = MagicMock()
        dt.strftime.return_value = "01-01-1970 00:16"

        mock_datetime.fromtimestamp.return_value = dt

        result = TranscriptMetadata.get_metadata(
            "sample.txt"
        )

        assert result == {
            "Words": 5,
            "Characters": len(
                "Hello world\nThis is transcript"
            ),
            "Lines": 2,
            "Reading Time": "1 min",
            "Size": "2.0 KB",
            "Created": "01-01-1970 00:16",
        }

        mock_file.assert_called_once_with(
            "sample.txt",
            "r",
            encoding="utf-8",
        )

    @patch("utils.transcript_metadata.os.path.getctime")
    @patch("utils.transcript_metadata.os.path.getsize")
    @patch("utils.transcript_metadata.datetime")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="word " * 400,
    )
    def test_get_metadata_reading_time(
        self,
        mock_file,
        mock_datetime,
        mock_getsize,
        mock_getctime,
    ):
        mock_getsize.return_value = 4096
        mock_getctime.return_value = 1000

        dt = MagicMock()
        dt.strftime.return_value = "01-01-1970 00:16"

        mock_datetime.fromtimestamp.return_value = dt

        result = TranscriptMetadata.get_metadata(
            "sample.txt"
        )

        assert result["Reading Time"] == "2 min"

    @patch("utils.transcript_metadata.os.path.getctime")
    @patch("utils.transcript_metadata.os.path.getsize")
    @patch("utils.transcript_metadata.datetime")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="",
    )
    def test_get_metadata_empty_file(
        self,
        mock_file,
        mock_datetime,
        mock_getsize,
        mock_getctime,
    ):
        mock_getsize.return_value = 0
        mock_getctime.return_value = 1000

        dt = MagicMock()
        dt.strftime.return_value = "01-01-1970 00:16"

        mock_datetime.fromtimestamp.return_value = dt

        result = TranscriptMetadata.get_metadata(
            "sample.txt"
        )

        assert result["Words"] == 0
        assert result["Characters"] == 0
        assert result["Lines"] == 0
        assert result["Reading Time"] == "1 min"
        assert result["Size"] == "0.0 KB"