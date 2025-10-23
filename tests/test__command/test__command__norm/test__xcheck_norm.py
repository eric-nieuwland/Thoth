import io
import unittest
from unittest.mock import MagicMock, call, patch

from thoth.command.old_norm.xcheck_norm import (
    _report_issues,
    xcheck_norm,
)


class TestReportIssues(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_nothing(self, mock_stdout):
        # given
        path1 = "MOCK path1"
        path2 = "MOCK path2"
        issue_kind = "MOCK issue_kind"
        issues = []
        # when
        _report_issues(path1, path2, issue_kind, issues)
        actual = mock_stdout.getvalue().strip()
        # then
        expect = "".strip()
        self.assertEqual(expect, actual)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_one(self, mock_stdout):
        # given
        path1 = "MOCK path1"
        path2 = "MOCK path2"
        issue_kind = "MOCK issue_kind"
        issues = [
            "MOCK issue #1",
        ]
        # when
        _report_issues(path1, path2, issue_kind, issues)
        actual = mock_stdout.getvalue().strip()
        # then
        expect = """
MOCK issue_kind found in 'MOCK path1' <-> 'MOCK path2':
  - MOCK issue #1
        """.strip()
        self.assertEqual(expect, actual)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_some(self, mock_stdout):
        # given
        path1 = "MOCK path1"
        path2 = "MOCK path2"
        issue_kind = "MOCK issue_kind"
        issues = (
            "MOCK issue #1",
            "MOCK issue #2",
            "MOCK issue #3",
        )
        # when
        _report_issues(path1, path2, issue_kind, issues)
        actual = mock_stdout.getvalue().strip()
        # then
        expect = """
MOCK issue_kind found in 'MOCK path1' <-> 'MOCK path2':
  - MOCK issue #1
  - MOCK issue #2
  - MOCK issue #3
        """.strip()
        self.assertEqual(expect, actual)


class TestXCheckNorm(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("thoth.command.norm.xcheck_norm.compare_norm_structures")
    @patch("thoth.command.norm.xcheck_norm.Norm")
    def test_it(
        self,
        mock_norm,
        mock_compare_norm_structures,
        mock_stdout,
    ):
        norm_mock = MagicMock()
        norm_mock.identifier = "MOCK norm identifier"
        norm_mock.drivers = "MOCK norm drivers"
        norm_mock.indicators = "MOCK norm indicators"
        mock_norm.from_yaml.side_effect = lambda *args: norm_mock
        mock_compare_norm_structures.return_value = [
            "MOCK compare_norm_structures() result",
            "MOCK diff #1",
            "MOCK diff #2",
            "MOCK diff #3",
        ]
        # given
        path1 = MagicMock()
        path1.is_file.return_value = True
        path1.open.return_value = "MOCK path1.open()"
        path2 = MagicMock()
        path2.is_file.return_value = True
        path2.open.return_value = "MOCK path2.open()"
        # when
        xcheck_norm(path1, path2)
        actual = mock_stdout.getvalue().strip()
        # then
        expect = [
            call.from_yaml("MOCK path1.open()"),
            call.from_yaml("MOCK path2.open()"),
        ]
        self.assertListEqual(expect, mock_norm.mock_calls)
        expect = [
            call(norm_mock, norm_mock),
        ]
        self.assertListEqual(expect, mock_compare_norm_structures.mock_calls)
        expect = f"""
differences found in '{path1}' <-> '{path2}':
  - MOCK compare_norm_structures() result
  - MOCK diff #1
  - MOCK diff #2
  - MOCK diff #3
        """.strip()
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
