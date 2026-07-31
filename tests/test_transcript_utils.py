import os
from unittest.mock import mock_open, patch

from utils.transcript_utils import TranscriptUtils


class TestTranscriptUtils:

    @patch("utils.transcript_utils.os.path.getmtime")
    @patch("utils.transcript_utils.os.listdir")
    @patch("utils.transcript_utils.os.makedirs")
    def test_list_transcripts(
        self,
        mock_makedirs,
        mock_listdir,
        mock_getmtime,
    ):
        mock_listdir.return_value = [
            "a.txt",
            "b.txt",
            "c.txt",
        ]

        times = {
            os.path.join("transcripts", "a.txt"): 1,
            os.path.join("transcripts", "b.txt"): 3,
            os.path.join("transcripts", "c.txt"): 2,
        }

        mock_getmtime.side_effect = (
            lambda path: times[path]
        )

        result = TranscriptUtils.list_transcripts()

        assert result == [
            "b.txt",
            "c.txt",
            "a.txt",
        ]

        mock_makedirs.assert_called_once_with(
            "transcripts",
            exist_ok=True,
        )

    @patch("utils.transcript_utils.os.rename")
    @patch("utils.transcript_utils.os.path.exists")
    def test_rename_transcript_success(
        self,
        mock_exists,
        mock_rename,
    ):
        mock_exists.return_value = False

        result = TranscriptUtils.rename_transcript(
            "old.txt",
            "new",
        )

        assert result is True

        mock_rename.assert_called_once_with(
            os.path.join(
                "transcripts",
                "old.txt",
            ),
            os.path.join(
                "transcripts",
                "new.txt",
            ),
        )

    @patch("utils.transcript_utils.os.rename")
    @patch("utils.transcript_utils.os.path.exists")
    def test_rename_transcript_existing_file(
        self,
        mock_exists,
        mock_rename,
    ):
        mock_exists.return_value = True

        result = TranscriptUtils.rename_transcript(
            "old.txt",
            "new.txt",
        )

        assert result is False

        mock_rename.assert_not_called()

    @patch.object(
        TranscriptUtils,
        "read_transcript",
    )
    @patch.object(
        TranscriptUtils,
        "list_transcripts",
    )
    def test_get_total_statistics(
        self,
        mock_list,
        mock_read,
    ):
        mock_list.return_value = [
            "a.txt",
            "b.txt",
        ]

        mock_read.side_effect = [
            "hello world",
            "one\ntwo\nthree",
        ]

        result = TranscriptUtils.get_total_statistics()

        assert result == {
            "files": 2,
            "words": 5,
            "characters": (
                len("hello world")
                + len("one\ntwo\nthree")
            ),
            "lines": 4,
        }

    @patch("builtins.open", new_callable=mock_open, read_data="sample text")
    def test_read_transcript(
        self,
        mock_file,
    ):
        result = TranscriptUtils.read_transcript(
            "sample.txt"
        )

        assert result == "sample text"

        mock_file.assert_called_once_with(
            os.path.join(
                "transcripts",
                "sample.txt",
            ),
            "r",
            encoding="utf-8",
        )

    @patch("utils.transcript_utils.os.remove")
    @patch("utils.transcript_utils.os.path.exists")
    def test_delete_transcript_success(
        self,
        mock_exists,
        mock_remove,
    ):
        mock_exists.return_value = True

        result = TranscriptUtils.delete_transcript(
            "sample.txt"
        )

        assert result is True

        mock_remove.assert_called_once_with(
            os.path.join(
                "transcripts",
                "sample.txt",
            )
        )

    @patch("utils.transcript_utils.os.remove")
    @patch("utils.transcript_utils.os.path.exists")
    def test_delete_transcript_not_found(
        self,
        mock_exists,
        mock_remove,
    ):
        mock_exists.return_value = False

        result = TranscriptUtils.delete_transcript(
            "sample.txt"
        )

        assert result is False

        mock_remove.assert_not_called()

    @patch("utils.transcript_utils.os.remove")
    @patch.object(
        TranscriptUtils,
        "list_transcripts",
    )
    def test_delete_all_transcripts(
        self,
        mock_list,
        mock_remove,
    ):
        mock_list.return_value = [
            "a.txt",
            "b.txt",
        ]

        TranscriptUtils.delete_all_transcripts()

        assert mock_remove.call_count == 2

        mock_remove.assert_any_call(
            os.path.join(
                "transcripts",
                "a.txt",
            )
        )

        mock_remove.assert_any_call(
            os.path.join(
                "transcripts",
                "b.txt",
            )
        )