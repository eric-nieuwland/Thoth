import unittest
from unittest.mock import MagicMock, call

from renderers.html.html_norm_fragments import html_norm__common


class TestMonoLingualList(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_empty(self):
        """
        empty list produces empty list
        """
        # given
        texts = []
        # when
        actual = html_norm__common.mono_lingual_list(texts)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_some(self):
        """
        list with some strings produces list with HTML
        """
        # given
        texts = [
            "foo",
            "bar",
            "baz",
        ]
        # when
        actual = html_norm__common.mono_lingual_list(texts)
        # then
        expect = [
            "<ul>",
            [
                "<li>foo</li>",
                "<li>bar</li>",
                "<li>baz</li>",
            ],
            "</ul>",
        ]
        self.assertListEqual(expect, actual)


class TestMultiLingualList(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @staticmethod
    def mock_multi_lingual_text(arg):
        mock = MagicMock()
        mock.__getitem__.return_value = arg
        return mock

    def test_empty(self):
        """
        empty list produces empty list
        """
        # given
        texts = []
        language = "py"
        # when
        actual = html_norm__common.multi_lingual_list(texts, language)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_some(self):
        """
        list with some strings produces list with HTML
        """
        # given
        mock_multi_lingual_text_1 = self.mock_multi_lingual_text("foo")
        mock_multi_lingual_text_2 = self.mock_multi_lingual_text("bar")
        mock_multi_lingual_text_3 = self.mock_multi_lingual_text("baz")
        texts = [
            mock_multi_lingual_text_1,
            mock_multi_lingual_text_2,
            mock_multi_lingual_text_3,
        ]
        language = "py"
        # when
        actual = html_norm__common.multi_lingual_list(texts, language)
        # then
        expect = [
            call.__getitem__("py"),
        ]
        self.assertListEqual(expect, mock_multi_lingual_text_1.mock_calls)
        self.assertListEqual(expect, mock_multi_lingual_text_2.mock_calls)
        self.assertListEqual(expect, mock_multi_lingual_text_3.mock_calls)
        expect = [
            "<ul>",
            [
                "<li>foo</li>",
                "<li>bar</li>",
                "<li>baz</li>",
            ],
            "</ul>",
        ]
        self.assertListEqual(expect, actual)


class TestWrapperDiv(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_it(self):
        """
        wraps the argument in an HTML <div>
        """
        # given
        div_class = "div_class"
        lst = (
            "bar",
            "baz",
            "foo",
        )
        # when
        actual = html_norm__common.classed_div(div_class, lst)
        # then
        expect = [
            '<div class="div_class">',
            (
                "bar",
                "baz",
                "foo",
            ),
            "</div>",
        ]
        self.assertListEqual(expect, actual)


class TestTitleDiv(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_it(self):
        """
        wraps the argument in an HTML <div>
        """
        # given
        div_class = "div_class"
        title = "baz bar foo"
        # when
        actual = html_norm__common.title_div(div_class, title)
        # then
        expect = [
            '<div class="div_class">',
            "  <p>baz bar foo</p>",
            "</div>",
        ]
        self.assertListEqual(expect, actual)


class TestTable(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_it(self):
        """
        wraps the argument in an HTML <table>
        """
        # given
        rows = (
            "bar",
            "baz",
            "foo",
        )
        # when
        actual = html_norm__common.table(*rows)
        # then
        expect = [
            "<table>",
            (
                "bar",
                "baz",
                "foo",
            ),
            "</table>",
        ]
        self.assertListEqual(expect, actual)


class TestTableRow(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_it(self):
        """
        wraps the argument in an HTML <tr>
        """
        # given
        cells = (
            "bar",
            "baz",
            "foo",
        )
        # when
        actual = html_norm__common.table_row(*cells)
        # then
        expect = [
            "<tr>",
            (
                "bar",
                "baz",
                "foo",
            ),
            "</tr>",
        ]
        self.assertListEqual(expect, actual)


class TestTableCell(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_empty(self):
        """
        wraps the argument in an HTML <td>
        """
        # given
        content = tuple()
        # when
        actual = html_norm__common.table_cell(*content)
        # then
        expect = [
            "<td/>",
        ]
        self.assertListEqual(expect, actual)

    def test_non_empty(self):
        """
        wraps the argument in an HTML <td>
        """
        # given
        content = (
            "bar",
            "baz",
            "foo",
        )
        # when
        actual = html_norm__common.table_cell(*content)
        # then
        expect = [
            "<td>",
            (
                "bar",
                "baz",
                "foo",
            ),
            "</td>",
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
