import unittest
from unittest.mock import MagicMock

from renderers.html.html_norm_fragments import html_norm_indicator_conformities


class TestIndicator(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_empty(self):
        # given
        conformities = []
        language = "py"
        id_prefix = "prefix"
        # when
        actual = html_norm_indicator_conformities.conformities(conformities, language, id_prefix)
        # then
        expect = [
            '<div class="sub-sub-part">',
            [
                '<div class="sub-sub-part-title">',
                "Conformity indicators",
                "</div>",
            ],
            "</div>",
        ]
        self.assertListEqual(expect, actual)

    def test_one(self):
        # given
        conformity_1 = MagicMock()
        conformity_1.identifier = "MOCK conformity #1 identifier"
        conformity_1.description = {"py": "MOCK conformity #1 description"}
        conformity_1.guidance = {"py": "MOCK conformity #1 guidance"}
        conformities = [
            conformity_1,
        ]
        language = "py"
        id_prefix = "prefix"
        # when
        actual = html_norm_indicator_conformities.conformities(conformities, language, id_prefix)
        # then
        expect = [
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
                            "prefix/MOCK conformity #1 identifier",
                            "</td>",
                        ],
                        [
                            "<td>",
                            "MOCK conformity #1 description",
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
                            "<em>MOCK conformity #1 guidance</em>",
                            "</td>",
                        ],
                        "</tr>",
                    ],
                ],
                "</table>",
            ],
            "</div>",
        ]
        self.assertListEqual(expect, actual)

    def test_some(self):
        # given
        conformity_1 = MagicMock()
        conformity_1.identifier = "MOCK conformity #1 identifier"
        conformity_1.description = {"py": "MOCK conformity #1 description"}
        conformity_1.guidance = {"py": "MOCK conformity #1 guidance"}
        conformity_2 = MagicMock()
        conformity_2.identifier = "MOCK conformity #2 identifier"
        conformity_2.description = {"py": "MOCK conformity #2 description"}
        conformity_2.guidance = None
        conformity_3 = MagicMock()
        conformity_3.identifier = "MOCK conformity #3 identifier"
        conformity_3.description = {"py": "MOCK conformity #3 description"}
        conformity_3.guidance = {"py": "MOCK conformity #3 guidance"}
        conformities = [
            conformity_1,
            conformity_2,
            conformity_3,
        ]
        language = "py"
        id_prefix = "prefix"
        # when
        actual = html_norm_indicator_conformities.conformities(conformities, language, id_prefix)
        # then
        expect = [
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
                            "prefix/MOCK conformity #1 identifier",
                            "</td>",
                        ],
                        [
                            "<td>",
                            "MOCK conformity #1 description",
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
                            "<em>MOCK conformity #1 guidance</em>",
                            "</td>",
                        ],
                        "</tr>",
                    ],
                ],
                [
                    [
                        "<tr>",
                        [
                            "<td>",
                            "prefix/MOCK conformity #2 identifier",
                            "</td>",
                        ],
                        [
                            "<td>",
                            "MOCK conformity #2 description",
                            "</td>",
                        ],
                        "</tr>",
                    ],
                    [],
                ],
                [
                    [
                        "<tr>",
                        [
                            "<td>",
                            "prefix/MOCK conformity #3 identifier",
                            "</td>",
                        ],
                        [
                            "<td>",
                            "MOCK conformity #3 description",
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
                            "<em>MOCK conformity #3 guidance</em>",
                            "</td>",
                        ],
                        "</tr>",
                    ],
                ],
                "</table>",
            ],
            "</div>",
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
