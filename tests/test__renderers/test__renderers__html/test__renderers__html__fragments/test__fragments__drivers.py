import unittest
from unittest.mock import call, patch

from renderers.html.html_norm_fragments import html_norm_drivers


class TestDrivers(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch.object(html_norm_drivers, "driver")
    @patch.object(html_norm_drivers, "_equal_width_horizontal_layout")
    def test_none(self, mock_equal_width_horizontal_layout, mock_driver):
        mock_equal_width_horizontal_layout.side_effect = (
            lambda *args: f"MOCK _equal_width_horizontal_layout{args}"
        )
        mock_driver.side_effect = lambda *args: f"MOCK driver{args}"
        # given
        drivers = []
        language = "py"
        # when
        actual = html_norm_drivers.drivers(drivers, language)
        # then
        expect = []
        self.assertListEqual(expect, mock_driver.mock_calls)
        self.assertListEqual(expect, mock_equal_width_horizontal_layout.mock_calls)
        expect = [
            [
                '<div class="part-title">',
                "drivers",
                "</div>",
            ],
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_drivers, "driver")
    @patch.object(html_norm_drivers, "_equal_width_horizontal_layout")
    def test_empty(self, mock_equal_width_horizontal_layout, mock_driver):
        mock_equal_width_horizontal_layout.side_effect = (
            lambda *args: f"MOCK _equal_width_horizontal_layout{args}"
        )
        mock_driver.side_effect = lambda *args: f"MOCK driver{args}"
        # given
        drivers = []
        language = "py"
        # when
        actual = html_norm_drivers.drivers(drivers, language)
        # then
        expect = []
        self.assertListEqual(expect, mock_driver.mock_calls)
        self.assertListEqual(expect, mock_equal_width_horizontal_layout.mock_calls)
        expect = [
            [
                '<div class="part-title">',
                "drivers",
                "</div>",
            ],
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_drivers, "driver")
    @patch.object(html_norm_drivers, "_equal_width_horizontal_layout")
    def test_one(self, mock_equal_width_horizontal_layout, mock_driver):
        mock_equal_width_horizontal_layout.side_effect = (
            lambda *args: f"MOCK _equal_width_horizontal_layout{args}"
        )
        mock_driver.side_effect = lambda *args: f"MOCK driver{args}"
        # given
        drivers = [
            "Driver #1",
        ]
        language = "py"
        # when
        actual = html_norm_drivers.drivers(drivers, language)
        # then
        expect = [
            call("Driver #1", "py", None),
        ]
        self.assertListEqual(expect, mock_driver.mock_calls)
        expect = [
            call(
                [
                    "MOCK driver('Driver #1', 'py', None)",
                ],
            ),
        ]
        self.assertListEqual(expect, mock_equal_width_horizontal_layout.mock_calls)
        expect = [
            '<div class="part">',
            [
                '<div class="part-title">',
                "drivers",
                "</div>",
            ],
            "MOCK _equal_width_horizontal_layout([\"MOCK driver('Driver #1', 'py', None)\"],)",
            "</div>",
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_drivers, "driver")
    @patch.object(html_norm_drivers, "_equal_width_horizontal_layout")
    def test_some(self, mock_equal_width_horizontal_layout, mock_driver):
        mock_equal_width_horizontal_layout.side_effect = (
            lambda *args: f"MOCK _equal_width_horizontal_layout{args}"
        )
        mock_driver.side_effect = lambda *args: f"MOCK driver{args}"
        # given
        drivers = [
            "Driver #1",
            "Driver #2",
            "Driver #3",
        ]
        language = "py"
        # when
        actual = html_norm_drivers.drivers(drivers, language)
        # then
        expect = [
            call("Driver #1", "py", None),
            call("Driver #2", "py", None),
            call("Driver #3", "py", None),
        ]
        self.assertListEqual(expect, mock_driver.mock_calls)
        expect = [
            call(
                [
                    "MOCK driver('Driver #1', 'py', None)",
                    "MOCK driver('Driver #2', 'py', None)",
                    "MOCK driver('Driver #3', 'py', None)",
                ],
            ),
        ]
        self.assertListEqual(expect, mock_equal_width_horizontal_layout.mock_calls)
        expect = [
            '<div class="part">',
            [
                '<div class="part-title">',
                "drivers",
                "</div>",
            ],
            "MOCK _equal_width_horizontal_layout("
            "["
            "\"MOCK driver('Driver #1', 'py', None)\", "
            "\"MOCK driver('Driver #2', 'py', None)\", "
            "\"MOCK driver('Driver #3', 'py', None)\""
            "],"
            ")",
            "</div>",
        ]
        self.assertListEqual(expect, actual)


class TestEqualWidthHorizontalLayout(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_empty(self):
        # given
        elements = []
        # when
        actual = html_norm_drivers._equal_width_horizontal_layout(elements)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_one(self):
        # given
        elements = [
            "foo",
        ]
        # when
        actual = html_norm_drivers._equal_width_horizontal_layout(elements)
        # then
        expect = [
            '<table width="100%">',
            "<tr>",
            [
                '<td width="*">',
                "foo",
                "</td>",
            ],
            "</tr>",
            "</table>",
        ]
        self.assertListEqual(expect, actual)

    def test_some(self):
        # given
        elements = [
            "foo",
            "bar",
            "baz",
        ]
        # when
        actual = html_norm_drivers._equal_width_horizontal_layout(elements)
        # then
        expect = [
            '<table width="100%">',
            "<tr>",
            [
                '<td width="*">',
                "foo",
                "</td>",
            ],
            [
                '<td width="33%">',
                "bar",
                "</td>",
            ],
            [
                '<td width="33%">',
                "baz",
                "</td>",
            ],
            "</tr>",
            "</table>",
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
