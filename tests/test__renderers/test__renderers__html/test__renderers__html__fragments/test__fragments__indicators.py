import unittest
from unittest.mock import MagicMock, patch, call

from renderers.html.html_norm_fragments import html_norm_indicators


class TestIndicators(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch.object(html_norm_indicators, "indicator")
    def test_none(self, mock_indicator):
        mock_indicator.side_effect = lambda *args: f"MOCK indicator{args}"
        # given
        indicators = []
        language = "py"
        id_prefix = "prefix"
        # when
        actual = html_norm_indicators.indicators(indicators, language, id_prefix)
        # then
        expect = []
        self.assertListEqual(expect, mock_indicator.mock_calls)
        expect = [
            [
                '<div class="part-title">',
                "indicators",
                "</div>",
            ],
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_indicators, "indicator")
    def test_empty(self, mock_indicator):
        mock_indicator.side_effect = lambda *args: f"MOCK indicator{args}"
        # given
        indicators = []
        language = "py"
        id_prefix = "prefix"
        # when
        actual = html_norm_indicators.indicators(indicators, language, id_prefix)
        # then
        expect = []
        self.assertListEqual(expect, mock_indicator.mock_calls)
        expect = [
            [
                '<div class="part-title">',
                "indicators",
                "</div>",
            ],
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_indicators, "indicator")
    def test_one(self, mock_indicator):
        mock_indicator.side_effect = lambda *args: f"MOCK indicator{args}"
        # given
        indicators = [
            "Indicator #1",
        ]
        language = "py"
        id_prefix = "prefix"
        # when
        actual = html_norm_indicators.indicators(indicators, language, id_prefix)
        # then
        expect = [
            call("Indicator #1", "py", "prefix", None),
        ]
        self.assertListEqual(expect, mock_indicator.mock_calls)
        expect = [
            '<div class="part">',
            [
                '<div class="part-title">',
                "indicators",
                "</div>",
            ],
            [
                "MOCK indicator('Indicator #1', 'py', 'prefix', None)",
            ],
            "</div>",
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_indicators, "indicator")
    def test_some(self, mock_indicator):
        mock_indicator.side_effect = lambda *args: f"MOCK indicator{args}"
        # given
        indicators = [
            "Indicator #1",
            "Indicator #2",
            "Indicator #3",
        ]
        language = "py"
        id_prefix = "prefix"
        # when
        actual = html_norm_indicators.indicators(indicators, language, id_prefix)
        # then
        expect = [
            call("Indicator #1", "py", "prefix", None),
            call("Indicator #2", "py", "prefix", None),
            call("Indicator #3", "py", "prefix", None),
        ]
        self.assertListEqual(expect, mock_indicator.mock_calls)
        expect = [
            '<div class="part">',
            [
                '<div class="part-title">',
                "indicators",
                "</div>",
            ],
            [
                "MOCK indicator('Indicator #1', 'py', 'prefix', None)",
                "MOCK indicator('Indicator #2', 'py', 'prefix', None)",
                "MOCK indicator('Indicator #3', 'py', 'prefix', None)",
            ],
            "</div>",
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
