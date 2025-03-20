import unittest
from unittest.mock import MagicMock, patch, call

from renderers.html.html_norm_fragments import html_norm_drivers


class TestDrivers(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_none(self):
        # given
        drivers = None
        language = "py"
        # when
        actual = html_norm_drivers._drivers(drivers, language)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_empty(self):
        # given
        drivers = []
        language = "py"
        # when
        actual = html_norm_drivers._drivers(drivers, language)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_drivers, "_driver")
    def test_one(self, mock_driver):
        mock_driver.side_effect = lambda *args: [f"{args}"]
        # given
        drivers = [
            "foo",
        ]
        language = "py"
        # when
        actual = html_norm_drivers._drivers(drivers, language)
        # then
        expect = [
            call("foo", "py", 100, 0),
        ]
        self.assertListEqual(expect, mock_driver.mock_calls)
        expect = [
            '<div class="sub-part">',
            (
                '  <table width="100%">',
                '    <tr>',
                [
                    ["('foo', 'py', 100, 0)"],
                ],
                '    </tr>',
                '  </table>',
            ),
            '</div>',
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_drivers, "_driver")
    def test_some(self, mock_driver):
        mock_driver.side_effect = lambda *args: [f"{args}"]
        # given
        drivers = [
            "foo",
            "bar",
            "baz",
        ]
        language = "py"
        # when
        actual = html_norm_drivers._drivers(drivers, language)
        # then
        expect = [
            call("foo", "py", 33, 0),
            call("bar", "py", 33, 1),
            call("baz", "py", 33, 2),
        ]
        self.assertListEqual(expect, mock_driver.mock_calls)
        expect = [
            '<div class="sub-part">',
            (
                '  <table width="100%">',
                '    <tr>',
                [
                    ["('foo', 'py', 33, 0)"],
                    ["('bar', 'py', 33, 1)"],
                    ["('baz', 'py', 33, 2)"],
                ],
                '    </tr>',
                '  </table>',
            ),
            '</div>',
        ]
        self.assertListEqual(expect, actual)


class TestDetails(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_none(self):
        # given
        details = None
        # when
        actual = html_norm_drivers._details(details)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_empty(self):
        # given
        details = []
        # when
        actual = html_norm_drivers._details(details)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_one(self):
        # given
        details = [
            "foo",
        ]
        # when
        actual = html_norm_drivers._details(details)
        # then
        expect = [
            '<table>',
            (
                [
                    '<tr>',
                    (
                        [
                            '<td>',
                            ('foo',),
                            '</td>'
                        ],
                    ),
                    '</tr>'
                ],
            ),
            '</table>',
        ]
        self.assertListEqual(expect, actual)

    def test_some(self):
        # given
        details = [
            "foo",
            "bar",
            "baz",
        ]
        # when
        actual = html_norm_drivers._details(details)
        # then
        expect = [
            '<table>',
            (
                [
                    '<tr>',
                    (
                        [
                            '<td>',
                            ('foo',),
                            '</td>'
                        ],
                    ),
                    '</tr>'
                ],
                [
                    '<tr>',
                    (
                        [
                            '<td>',
                            ('bar',),
                            '</td>'
                        ],
                    ),
                    '</tr>'
                ],
                [
                    '<tr>',
                    (
                        [
                            '<td>',
                            ('baz',),
                            '</td>'
                        ],
                    ),
                    '</tr>'
                ],
            ),
            '</table>',
        ]
        self.assertListEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
