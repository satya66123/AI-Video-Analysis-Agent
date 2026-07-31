# tests/test_metadata.py

from unittest.mock import MagicMock, call, patch

from components.metadata import show_metadata


class TestMetadata:

    @patch("components.metadata.st.metric")
    @patch("components.metadata.st.columns")
    @patch("components.metadata.st.subheader")
    def test_show_metadata(
        self,
        mock_subheader,
        mock_columns,
        mock_metric,
    ):
        metadata = {
            "resolution": "1920x1080",
            "fps": 30,
            "duration": 125.678,
            "frames": 3770,
            "codec": "H.264",
            "file_size_mb": 256,
        }

        col1 = MagicMock()
        col2 = MagicMock()

        col1.__enter__.return_value = col1
        col1.__exit__.return_value = False

        col2.__enter__.return_value = col2
        col2.__exit__.return_value = False

        mock_columns.return_value = (
            col1,
            col2,
        )

        show_metadata(metadata)

        mock_subheader.assert_called_once_with(
            "📊 Video Metadata"
        )

        mock_columns.assert_called_once_with(2)

        mock_metric.assert_has_calls(
            [
                call(
                    "Resolution",
                    "1920x1080",
                ),
                call(
                    "FPS",
                    30,
                ),
                call(
                    "Duration",
                    "125.68 sec",
                ),
                call(
                    "Frames",
                    3770,
                ),
                call(
                    "Codec",
                    "H.264",
                ),
                call(
                    "File Size",
                    "256 MB",
                ),
            ],
            any_order=False,
        )

        assert mock_metric.call_count == 6