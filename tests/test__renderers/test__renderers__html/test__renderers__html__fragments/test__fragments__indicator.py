import unittest
from unittest.mock import MagicMock, patch, call

from renderers.html.html_norm_fragments import html_norm_indicator


class TestIndicator(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch.object(html_norm_indicator, "explanation")
    @patch.object(html_norm_indicator, "conformities")
    @patch.object(html_norm_indicator, "description")
    def test_calls(self, mock_description, mock_conformities, mock_explanation):
        mock_description.side_effect = lambda *args: f"MOCK description{args}"
        mock_conformities.side_effect = lambda *args: f"MOCK conformities{args}"
        mock_explanation.side_effect = lambda *args: f"MOCK explanation{args}"
        # given
        indicator = MagicMock()
        indicator.identifier = "MOCK indicator identifier"
        indicator.title = {"py": "MOCK indicator title"}
        indicator.description = "MOCK indicator description"
        indicator.conformities = "MOCK indicator conformities"
        indicator.explanation = "MOCK indicator explanation"
        language = "py"
        id_prefix = ""
        # when
        actual = html_norm_indicator.indicator(indicator, language, id_prefix)
        # then
        expect = [
            call("MOCK indicator description", "py"),
        ]
        self.assertListEqual(expect, mock_description.mock_calls)
        expect = [
            call("MOCK indicator conformities", "py", "MOCK indicator identifier", None),
        ]
        self.assertListEqual(expect, mock_conformities.mock_calls)
        expect = [
            call("MOCK indicator explanation", "py"),
        ]
        self.assertListEqual(expect, mock_explanation.mock_calls)
        expect = [
            '<div class="sub-part">',
            [
                '<div class="indicator-title">',
                'MOCK indicator identifier MOCK indicator title',
                '</div>',
            ],
            "MOCK description('MOCK indicator description', 'py')",
            "MOCK conformities('MOCK indicator conformities', 'py', 'MOCK indicator identifier', None)",
            "MOCK explanation('MOCK indicator explanation', 'py')",
            "</div>",
        ]
        self.assertListEqual(expect, actual)

    def test_integrated(self):
        # given
        conformity = MagicMock()
        conformity.identifier = "MOCK conformity identifier"
        conformity.description = {"py": "MOCK conformity description"}
        conformity.guidance = {"py": "MOCK conformity guidance"}
        indicator = MagicMock()
        indicator.identifier = "MOCK indicator identifier"
        indicator.title = {"py": "MOCK indicator title"}
        indicator.description = {"py": "MOCK indicator description"}
        indicator.conformities = [conformity]
        indicator.explanation = {"py": "MOCK indicator explanation"}
        language = "py"
        id_prefix = ""
        # when
        actual = html_norm_indicator.indicator(indicator, language, id_prefix)
        # then
        expect = [
            '<div class="sub-part">',
            [
                '<div class="indicator-title">',
                "MOCK indicator identifier MOCK indicator title",
                "</div>",
            ],
            [
                '<div class="sub-sub-part">',
                "MOCK indicator description",
                "</div>",
            ],
            [
                '<div class="sub-sub-part">',
                [
                    '<div class="sub-sub-part-title">',
                    "Conformity indicators",
                    "</div>",
                ],
                [
                    "<table>",
                    [
                        [
                            "<tr>",
                               [
                                   "<td>",
                                   "MOCK indicator identifier/MOCK conformity identifier",
                                   "</td>",
                               ],
                               [
                                   "<td>",
                                   "MOCK conformity description",
                                   "</td>",
                               ],
                            "</tr>",
                        ],
                        [
                            "<tr>",
                            [
                                "<td/>",
                            ],
                            [
                                "<td>",
                                "<em>MOCK conformity guidance</em>",
                                "</td>",
                            ],
                            "</tr>",
                        ],
                    ],
                    "</table>",
                ],
                "</div>",
            ],
            [
                '<div class="sub-sub-part">',
                [
                    '<div class="sub-sub-part-title">',
                    "Explanation",
                    "</div>",
                ],
                'MOCK indicator explanation',
                "</div>",
            ],
            "</div>",
        ]
        self.assertListEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
