from unittest.mock import MagicMock, patch

from pages.about import show_about


class TestAbout:

    @patch("pages.about.st.caption")
    @patch("pages.about.st.metric")
    @patch("pages.about.st.columns")
    @patch("pages.about.st.write")
    @patch("pages.about.st.markdown")
    @patch("pages.about.st.subheader")
    @patch("pages.about.st.divider")
    @patch("pages.about.st.header")
    def test_show_about(
        self,
        mock_header,
        mock_divider,
        mock_subheader,
        mock_markdown,
        mock_write,
        mock_columns,
        mock_metric,
        mock_caption,
    ):
        col1 = MagicMock()
        col2 = MagicMock()

        col1.__enter__.return_value = col1
        col1.__exit__.return_value = False

        col2.__enter__.return_value = col2
        col2.__exit__.return_value = False

        mock_columns.side_effect = [
            (col1, col2),  # Features
            (col1, col2),  # Version
        ]

        show_about()

        mock_header.assert_called_once_with(
            "ℹ️ About AI Video Analyzer"
        )

        assert mock_divider.call_count == 6

        assert mock_subheader.call_count == 5

        mock_subheader.assert_any_call(
            "🎯 Features"
        )

        mock_subheader.assert_any_call(
            "🧠 Supported AI Providers"
        )

        mock_subheader.assert_any_call(
            "🛠 Technology Stack"
        )

        mock_subheader.assert_any_call(
            "🚀 Project Roadmap"
        )

        mock_subheader.assert_any_call(
            "📌 Version Information"
        )

        # Description + roadmap items
        assert mock_write.call_count == 11

        # Features + Providers + Stack
        assert mock_markdown.call_count == 4

        mock_columns.assert_any_call(2)

        mock_metric.assert_any_call(
            "Version",
            "v1.0.0",
        )

        mock_metric.assert_any_call(
            "Status",
            "Development",
        )

        mock_caption.assert_called_once_with(
            "© 2026 AI Video Analyzer | Built with ❤️ using Python & Streamlit"
        )