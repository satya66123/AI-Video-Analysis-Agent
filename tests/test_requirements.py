from pathlib import Path


class TestRequirements:

    def test_requirements_file_exists(self):
        """requirements.txt should exist."""
        assert Path("requirements.txt").exists()

    def test_requirements_not_empty(self):
        """requirements.txt should not be empty."""
        content = Path("requirements.txt").read_text(encoding="utf-8")
        assert content.strip() != ""

    def test_required_packages_present(self):
        """Verify essential dependencies exist."""
        content = Path("requirements.txt").read_text(encoding="utf-8")

        required_packages = [
            "streamlit",
            "pandas",
            "numpy",
            "ollama",
            "openai",
            "anthropic",
            "python-dotenv",
            "requests",
            "openai-whisper",
            "torch",
            "torchaudio",
            "moviepy",
            "opencv-python",
            "mutagen",
            "Pillow",
            "reportlab",
            "markdown",
            "beautifulsoup4",
            "tqdm",
            "typing_extensions",
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "coverage",
            "ruff",
        ]

        for package in required_packages:
            assert package in content, f"{package} not found in requirements.txt"

    def test_no_duplicate_packages(self):
        """Ensure package names are not duplicated."""
        content = Path("requirements.txt").read_text(encoding="utf-8")

        packages = []

        for line in content.splitlines():
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            package = (
                line.split(">=")[0]
                .split("==")[0]
                .split("<=")[0]
                .strip()
                .lower()
            )

            packages.append(package)

        assert len(packages) == len(set(packages)), "Duplicate packages found."

    def test_version_specifiers_present(self):
        """Every dependency should have a version specifier."""
        content = Path("requirements.txt").read_text(encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            assert any(
                op in line for op in (">=", "==", "<=", "~=", "!=")
            ), f"Missing version specifier: {line}"