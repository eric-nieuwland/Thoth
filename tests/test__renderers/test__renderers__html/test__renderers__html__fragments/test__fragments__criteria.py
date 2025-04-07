import unittest
from unittest.mock import MagicMock, patch, call

from renderers.html.html_norm_fragments import html_norm_criteria


class TestCriteria(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch.object(html_norm_criteria, "multi_lingual_list")
    def test_empty(self, mock_multi_lingual_list):
        mock_multi_lingual_list.side_effect = lambda c, l: f"MOCK multi_lingual_list({c}, {l})"
        # given
        criteria = []
        language = "py"
        # when
        actual = html_norm_criteria.criteria(criteria, language)
        # then
        expect = [
            call([], "py"),
        ]
        self.assertListEqual(expect, mock_multi_lingual_list.mock_calls)
        expect = [
            '<div class="part">',
            [
                '<div class="part-title">',
                "criteria",
                "</div>",
            ],
            "MOCK multi_lingual_list([], py)",
            "</div>",
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_criteria, "multi_lingual_list")
    def test_one(self, mock_multi_lingual_list):
        mock_multi_lingual_list.side_effect = lambda c, l: f"MOCK multi_lingual_list({c}, {l})"
        # given
        criteria = [
            "Criterium #1",
        ]
        language = "py"
        # when
        actual = html_norm_criteria.criteria(criteria, language)
        # then
        expect = [
            call(
                [
                    "Criterium #1",
                ],
                "py",
            ),
        ]
        self.assertListEqual(expect, mock_multi_lingual_list.mock_calls)
        expect = [
            '<div class="part">',
            [
                '<div class="part-title">',
                "criteria",
                "</div>",
            ],
            "MOCK multi_lingual_list(['Criterium #1'], py)",
            "</div>",
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_criteria, "multi_lingual_list")
    def test_some(self, mock_multi_lingual_list):
        mock_multi_lingual_list.side_effect = lambda c, l: f"MOCK multi_lingual_list({c}, {l})"
        # given
        criteria = [
            "Criterium #1",
            "Criterium #2",
            "Criterium #3",
        ]
        language = "py"
        # when
        actual = html_norm_criteria.criteria(criteria, language)
        # then
        expect = [
            call(
                [
                    "Criterium #1",
                    "Criterium #2",
                    "Criterium #3",
                ],
                "py",
            ),
        ]
        self.assertListEqual(expect, mock_multi_lingual_list.mock_calls)
        expect = [
            '<div class="part">',
            [
                '<div class="part-title">',
                "criteria",
                "</div>",
            ],
            "MOCK multi_lingual_list(['Criterium #1', 'Criterium #2', 'Criterium #3'], py)",
            "</div>",
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
