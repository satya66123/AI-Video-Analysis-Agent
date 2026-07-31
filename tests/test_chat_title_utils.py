from utils.chat_title import ChatTitle


class TestChatTitleUtils:

    def test_generate_simple_title(self):
        result = ChatTitle.generate(
            "Hello World"
        )

        assert result == "Hello_World"

    def test_generate_removes_special_characters(self):
        result = ChatTitle.generate(
            "Hello!!! @World #2024?"
        )

        assert result == "Hello_World_2024"

    def test_generate_trims_whitespace(self):
        result = ChatTitle.generate(
            "   AI Video Analyzer   "
        )

        assert result == "AI_Video_Analyzer"

    def test_generate_multiple_spaces(self):
        result = ChatTitle.generate(
            "AI     Video      Analyzer"
        )

        assert result == "AI_Video_Analyzer"

    def test_generate_preserves_hyphen(self):
        result = ChatTitle.generate(
            "AI-Video Analyzer"
        )

        assert result == "AI-Video_Analyzer"

    def test_generate_empty_string(self):
        result = ChatTitle.generate("")

        assert result == ""

    def test_generate_only_special_characters(self):
        result = ChatTitle.generate(
            "!@#$%^&*()"
        )

        assert result == ""

    def test_generate_max_length_40(self):
        question = (
            "This is a very long chat title that should "
            "be truncated after forty characters"
        )

        result = ChatTitle.generate(question)

        assert len(result) == 40

        assert result == result[:40]