from unittest.mock import patch

from utils.transcript_validator import TranscriptValidator


class TestTranscriptValidatorUtils:

    @patch("utils.transcript_validator.os.path.exists")
    def test_validate_file_not_exists(
        self,
        mock_exists,
    ):
        mock_exists.return_value = False

        result = TranscriptValidator.validate(
            "transcript.txt"
        )

        assert result is False

    @patch("utils.transcript_validator.os.path.getsize")
    @patch("utils.transcript_validator.os.path.exists")
    def test_validate_empty_file(
        self,
        mock_exists,
        mock_getsize,
    ):
        mock_exists.return_value = True
        mock_getsize.return_value = 0

        result = TranscriptValidator.validate(
            "transcript.txt"
        )

        assert result is False

    @patch("utils.transcript_validator.os.path.getsize")
    @patch("utils.transcript_validator.os.path.exists")
    def test_validate_valid_file(
        self,
        mock_exists,
        mock_getsize,
    ):
        mock_exists.return_value = True
        mock_getsize.return_value = 1024

        result = TranscriptValidator.validate(
            "transcript.txt"
        )

        assert result is True

    @patch("utils.transcript_validator.os.path.getsize")
    @patch("utils.transcript_validator.os.path.exists")
    def test_validate_small_non_empty_file(
        self,
        mock_exists,
        mock_getsize,
    ):
        mock_exists.return_value = True
        mock_getsize.return_value = 1

        result = TranscriptValidator.validate(
            "transcript.txt"
        )

        assert result is True