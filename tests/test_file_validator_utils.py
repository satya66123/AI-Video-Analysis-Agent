from unittest.mock import MagicMock

from utils.file_validator import FileValidator


class TestFileValidatorUtils:

    def test_validate_valid_mp4(self):
        uploaded = MagicMock()
        uploaded.name = "video.mp4"
        uploaded.size = 100 * 1024 * 1024

        valid, message = FileValidator.validate(uploaded)

        assert valid is True
        assert message == "Valid"

    def test_validate_valid_uppercase_extension(self):
        uploaded = MagicMock()
        uploaded.name = "movie.MP4"
        uploaded.size = 500

        valid, message = FileValidator.validate(uploaded)

        assert valid is True
        assert message == "Valid"

    def test_validate_invalid_extension(self):
        uploaded = MagicMock()
        uploaded.name = "video.mp3"
        uploaded.size = 100

        valid, message = FileValidator.validate(uploaded)

        assert valid is False
        assert message == "Unsupported video format."

    def test_validate_size_exceeds_limit(self):
        uploaded = MagicMock()
        uploaded.name = "video.mp4"
        uploaded.size = FileValidator.MAX_SIZE + 1

        valid, message = FileValidator.validate(uploaded)

        assert valid is False
        assert message == (
            f"Video exceeds "
            f"{FileValidator.MAX_SIZE // (1024 * 1024)} MB."
        )

    def test_validate_size_at_limit(self):
        uploaded = MagicMock()
        uploaded.name = "video.mp4"
        uploaded.size = FileValidator.MAX_SIZE

        valid, message = FileValidator.validate(uploaded)

        assert valid is True
        assert message == "Valid"

    def test_validate_all_supported_extensions(self):
        for extension in FileValidator.ALLOWED_EXTENSIONS:
            uploaded = MagicMock()
            uploaded.name = f"video{extension}"
            uploaded.size = 1024

            valid, message = FileValidator.validate(uploaded)

            assert valid is True
            assert message == "Valid"