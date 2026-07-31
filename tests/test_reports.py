from unittest.mock import MagicMock, patch

from pages.reports import show_reports


@patch("pages.reports.show_download_center")
@patch("pages.reports.show_report_preview")
@patch("pages.reports.show_chat_reports")
@patch("pages.reports.show_analysis_reports")
@patch("pages.reports.show_transcript_reports")
@patch("pages.reports.st.tabs")
@patch("pages.reports.st.divider")
@patch("pages.reports.st.caption")
@patch("pages.reports.st.title")
def test_show_reports(
    mock_title,
    mock_caption,
    mock_divider,
    mock_tabs,
    mock_transcripts,
    mock_analysis,
    mock_chat,
    mock_preview,
    mock_download,
):
    transcript_tab = MagicMock()
    analysis_tab = MagicMock()
    chat_tab = MagicMock()
    summary_tab = MagicMock()
    export_tab = MagicMock()

    for tab in (
        transcript_tab,
        analysis_tab,
        chat_tab,
        summary_tab,
        export_tab,
    ):
        tab.__enter__.return_value = tab
        tab.__exit__.return_value = False

    mock_tabs.return_value = (
        transcript_tab,
        analysis_tab,
        chat_tab,
        summary_tab,
        export_tab,
    )

    show_reports()

    mock_title.assert_called_once_with(
        "📄 Reports"
    )

    mock_caption.assert_called_once_with(
        "View, manage and export transcripts, AI analysis, chat history and reports."
    )

    mock_divider.assert_called_once()

    mock_tabs.assert_called_once_with(
        [
            "📑 Transcript Reports",
            "🤖 AI Analysis Reports",
            "💬 Chat Reports",
            "📊 Summary Report",
            "📥 Export Center",
        ]
    )

    mock_transcripts.assert_called_once()
    mock_analysis.assert_called_once()
    mock_chat.assert_called_once()
    mock_preview.assert_called_once()
    mock_download.assert_called_once()