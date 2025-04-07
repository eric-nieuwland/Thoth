import unittest
from unittest.mock import MagicMock, patch, call

from renderers.html.html_norm_fragments import html_norm_driver


class TestDriver(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch.object(html_norm_driver, "table_cell")
    @patch.object(html_norm_driver, "table_row")
    @patch.object(html_norm_driver, "table")
    def test_none(self, mock_table, mock_table_row, mock_table_cell):
        mock_table.side_effect = lambda *args: f"MOCK table{args}"
        mock_table_row.side_effect = lambda *args: f"MOCK table_row{args}"
        mock_table_cell.side_effect = lambda *args: f"MOCK table_cell{args}"
        # given
        driver = MagicMock()
        driver.name = "MOCK driver name"
        driver.details = None
        language = "py"
        # when
        actual = html_norm_driver.driver(driver, language)
        # then
        expect = []
        self.assertListEqual(expect, mock_table.mock_calls)
        self.assertListEqual(expect, mock_table_row.mock_calls)
        self.assertListEqual(expect, mock_table_cell.mock_calls)
        expect = [
            [
                '<div class="sub-part-title">',
                "MOCK driver name",
                "</div>",
            ],
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_driver, "table_cell")
    @patch.object(html_norm_driver, "table_row")
    @patch.object(html_norm_driver, "table")
    def test_empty(self, mock_table, mock_table_row, mock_table_cell):
        mock_table.side_effect = lambda *args: f"MOCK table{args}"
        mock_table_row.side_effect = lambda *args: f"MOCK table_row{args}"
        mock_table_cell.side_effect = lambda *args: f"MOCK table_cell{args}"
        # given
        driver = MagicMock()
        driver.name = "MOCK driver name"
        driver.details = []
        language = "py"
        # when
        actual = html_norm_driver.driver(driver, language)
        # then
        expect = []
        self.assertListEqual(expect, mock_table.mock_calls)
        self.assertListEqual(expect, mock_table_row.mock_calls)
        self.assertListEqual(expect, mock_table_cell.mock_calls)
        expect = [
            [
                '<div class="sub-part-title">',
                "MOCK driver name",
                "</div>",
            ],
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_driver, "table_cell")
    @patch.object(html_norm_driver, "table_row")
    @patch.object(html_norm_driver, "table")
    def test_one(self, mock_table, mock_table_row, mock_table_cell):
        mock_table.side_effect = lambda *args: f"MOCK table{args}"
        mock_table_row.side_effect = lambda *args: f"MOCK table_row{args}"
        mock_table_cell.side_effect = lambda *args: f"MOCK table_cell{args}"
        # given
        driver = MagicMock()
        driver.name = "MOCK driver name"
        driver.details = [
            "Detail #1",
        ]
        language = "py"
        # when
        actual = html_norm_driver.driver(driver, language)
        # then
        expect = [
            call("""MOCK table_row("MOCK table_cell('Detail #1',)",)"""),
        ]
        self.assertListEqual(expect, mock_table.mock_calls)
        expect = [
            call("MOCK table_cell('Detail #1',)"),
        ]
        self.assertListEqual(expect, mock_table_row.mock_calls)
        expect = [
            call("Detail #1"),
        ]
        self.assertListEqual(expect, mock_table_cell.mock_calls)
        expect = [
            [
                '<div class="sub-part-title">',
                "MOCK driver name",
                "</div>",
            ],
            """MOCK table("""
            """'MOCK table_row("MOCK table_cell(\\'Detail #1\\',)",)',"""
            """)""",
        ]
        self.assertListEqual(expect, actual)

    @patch.object(html_norm_driver, "table_cell")
    @patch.object(html_norm_driver, "table_row")
    @patch.object(html_norm_driver, "table")
    def test_some(self, mock_table, mock_table_row, mock_table_cell):
        mock_table.side_effect = lambda *args: f"MOCK table{args}"
        mock_table_row.side_effect = lambda *args: f"MOCK table_row{args}"
        mock_table_cell.side_effect = lambda *args: f"MOCK table_cell{args}"
        # given
        driver = MagicMock()
        driver.name = "MOCK driver name"
        driver.details = [
            "Detail #1",
            "Detail #2",
            "Detail #3",
        ]
        language = "py"
        # when
        actual = html_norm_driver.driver(driver, language)
        # then
        expect = [
            call(
                """MOCK table_row("MOCK table_cell('Detail #1',)",)""",
                """MOCK table_row("MOCK table_cell('Detail #2',)",)""",
                """MOCK table_row("MOCK table_cell('Detail #3',)",)""",
            ),
        ]
        self.assertListEqual(expect, mock_table.mock_calls)
        expect = [
            call("MOCK table_cell('Detail #1',)"),
            call("MOCK table_cell('Detail #2',)"),
            call("MOCK table_cell('Detail #3',)"),
        ]
        self.assertListEqual(expect, mock_table_row.mock_calls)
        expect = [
            call("Detail #1"),
            call("Detail #2"),
            call("Detail #3"),
        ]
        self.assertListEqual(expect, mock_table_cell.mock_calls)
        expect = [
            [
                '<div class="sub-part-title">',
                "MOCK driver name",
                "</div>",
            ],
            """MOCK table("""
            """'MOCK table_row("MOCK table_cell(\\'Detail #1\\',)",)', """
            """'MOCK table_row("MOCK table_cell(\\'Detail #2\\',)",)', """
            """'MOCK table_row("MOCK table_cell(\\'Detail #3\\',)",)'"""
            """)""",
        ]
        self.assertListEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
