import os


class FileValidator:

    ALLOWED_EXTENSIONS = {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".webm"
    }

    MAX_SIZE = 1024 * 1024 * 1024  # 1 GB

    @classmethod
    def validate(cls, uploaded_file):

        extension = os.path.splitext(uploaded_file.name)[1].lower()

        if extension not in cls.ALLOWED_EXTENSIONS:
            return False, "Unsupported video format."

        if uploaded_file.size > cls.MAX_SIZE:
            max_size_mb = cls.MAX_SIZE // (1024 * 1024)
            return False, f"Video exceeds {max_size_mb} MB."

        return True, "Valid"