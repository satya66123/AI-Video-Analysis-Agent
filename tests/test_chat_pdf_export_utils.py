import os
from unittest.mock import MagicMock, patch

from utils.chat_pdf_export import ChatPDFExport


class TestChatPDFExportUtils:

    @patch("utils.chat_pdf_export.Paragraph")
    @patch("utils.chat_pdf_export.getSampleStyleSheet")
    @patch("utils.chat_pdf_export.SimpleDocTemplate")
    @patch("utils.chat_pdf_export.os.makedirs")
    def test_export_success(
        self,
        mock_makedirs,
        mock_doc_class,
        mock_stylesheet,
        mock_paragraph,
    ):
        styles = {
            "Title": MagicMock(),
            "Normal": MagicMock(),
            "Heading2": MagicMock(),
            "BodyText": MagicMock(),
        }

        mock_stylesheet.return_value = styles

        mock_doc = MagicMock()
        mock_doc_class.return_value = mock_doc

        mock_paragraph.side_effect = (
            lambda text, style: f"P:{text}"
        )

        history = [
            {
                "user": "Hello",
                "assistant": "Hi",
            },
            {
                "user": "How are you?",
                "assistant": "I'm fine.",
            },
        ]

        result = ChatPDFExport.export(
            history=history,
            transcript_name="video.txt",
            provider="Ollama",
            model="llama3",
            filename="report",
        )

        expected = os.path.join(
            "exports",
            "report.pdf",
        )

        assert result == expected

        mock_makedirs.assert_called_once_with(
            "exports",
            exist_ok=True,
        )

        mock_doc_class.assert_called_once_with(
            expected
        )

        mock_doc.build.assert_called_once()

        story = mock_doc.build.call_args.args[0]

        assert len(story) == 16

    @patch("utils.chat_pdf_export.Paragraph")
    @patch("utils.chat_pdf_export.getSampleStyleSheet")
    @patch("utils.chat_pdf_export.SimpleDocTemplate")
    @patch("utils.chat_pdf_export.os.makedirs")
    def test_export_empty_history(
        self,
        mock_makedirs,
        mock_doc_class,
        mock_stylesheet,
        mock_paragraph,
    ):
        styles = {
            "Title": MagicMock(),
            "Normal": MagicMock(),
            "Heading2": MagicMock(),
            "BodyText": MagicMock(),
        }

        mock_stylesheet.return_value = styles

        mock_doc = MagicMock()
        mock_doc_class.return_value = mock_doc

        mock_paragraph.side_effect = (
            lambda text, style: text
        )

        result = ChatPDFExport.export(
            history=[],
            transcript_name="video.txt",
            provider="OpenAI",
            model="gpt-4",
            filename="empty",
        )

        expected = os.path.join(
            "exports",
            "empty.pdf",
        )

        assert result == expected

        mock_doc.build.assert_called_once()

        story = mock_doc.build.call_args.args[0]

        assert len(story) == 6