from unittest.mock import MagicMock, call, patch

from components.dashboard_cards import show_dashboard_cards


class TestDashboardCards:

    @patch("components.dashboard_cards.st.metric")
    @patch("components.dashboard_cards.st.columns")
    @patch("components.dashboard_cards.os.path.getsize")
    @patch("components.dashboard_cards.os.path.join")
    @patch("components.dashboard_cards.VideoService.list_videos")
    def test_show_dashboard_cards_with_videos(
        self,
        mock_list_videos,
        mock_join,
        mock_getsize,
        mock_columns,
        mock_metric,
    ):
        mock_list_videos.return_value = [
            "video1.mp4",
            "video2.mp4",
            "video3.mp4",
        ]

        mock_join.side_effect = [
            "uploads/video1.mp4",
            "uploads/video2.mp4",
            "uploads/video3.mp4",
        ]

        # 1 MB + 2 MB + 3 MB = 6 MB
        mock_getsize.side_effect = [
            1024 * 1024,
            2 * 1024 * 1024,
            3 * 1024 * 1024,
        ]

        col1 = MagicMock()
        col2 = MagicMock()
        col3 = MagicMock()

        for col in (col1, col2, col3):
            col.__enter__.return_value = col
            col.__exit__.return_value = False

        mock_columns.return_value = (
            col1,
            col2,
            col3,
        )

        show_dashboard_cards()

        mock_list_videos.assert_called_once()

        assert mock_join.call_count == 3
        assert mock_getsize.call_count == 3

        mock_columns.assert_called_once_with(3)

        mock_metric.assert_has_calls(
            [
                call("Videos", 3),
                call("Storage", "6.00 MB"),
                call("Providers", 3),
            ]
        )

        assert mock_metric.call_count == 3

    @patch("components.dashboard_cards.st.metric")
    @patch("components.dashboard_cards.st.columns")
    @patch("components.dashboard_cards.os.path.getsize")
    @patch("components.dashboard_cards.os.path.join")
    @patch("components.dashboard_cards.VideoService.list_videos")
    def test_show_dashboard_cards_no_videos(
        self,
        mock_list_videos,
        mock_join,
        mock_getsize,
        mock_columns,
        mock_metric,
    ):
        mock_list_videos.return_value = []

        col1 = MagicMock()
        col2 = MagicMock()
        col3 = MagicMock()

        for col in (col1, col2, col3):
            col.__enter__.return_value = col
            col.__exit__.return_value = False

        mock_columns.return_value = (
            col1,
            col2,
            col3,
        )

        show_dashboard_cards()

        mock_list_videos.assert_called_once()

        mock_join.assert_not_called()
        mock_getsize.assert_not_called()

        mock_columns.assert_called_once_with(3)

        mock_metric.assert_has_calls(
            [
                call("Videos", 0),
                call("Storage", "0.00 MB"),
                call("Providers", 3),
            ]
        )

        assert mock_metric.call_count == 3