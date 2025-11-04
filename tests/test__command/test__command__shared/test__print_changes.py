import unittest
from unittest.mock import patch

from io import StringIO

from thoth.command.shared.print_changes import print_changes


class TestPrintChanges(unittest.TestCase):
    """
    test print_changes() function
    """

    def setUp(self) -> None:
        self.maxDiff = None

    @patch("sys.stdout", new_callable=StringIO)
    def test_empties(self, mock_stdout) -> None:
        # given
        for original in ([], ""):
            for changed in ([], ""):
                # when
                actual = print_changes(original, changed)
                # then
                expect = False
                self.assertEqual(expect, actual, msg=f"failed for {original!r} and {changed!r}")
                expect = ""
                self.assertEqual(expect, mock_stdout.getvalue(), msg=f"failed for {original!r} and {changed!r}")

    @patch("sys.stdout", new_callable=StringIO)
    def test_one_line_added(self, mock_stdout) -> None:
        # given
        original = ""
        changed = "foo bar"
        # when
        actual = print_changes(original, changed)
        # then
        expect = True
        self.assertEqual(expect, actual)
        expect = """
+     foo bar
        """.strip()
        self.assertEqual(expect, mock_stdout.getvalue().strip())

    @patch("sys.stdout", new_callable=StringIO)
    def test_one_line_removed(self, mock_stdout) -> None:
        # given
        original = "foo bar"
        changed = ""
        # when
        actual = print_changes(original, changed)
        # then
        expect = True
        self.assertEqual(expect, actual)
        expect = """
-   1 foo bar
        """.strip()
        self.assertEqual(expect, mock_stdout.getvalue().strip())

    @patch("sys.stdout", new_callable=StringIO)
    def test_one_line_changed(self, mock_stdout) -> None:
        # given
        original = "foo bar"
        changed = "baz qux"
        # when
        actual = print_changes(original, changed)
        # then
        expect = True
        self.assertEqual(expect, actual)
        expect = """
-   1 foo bar
+     baz qux
        """.strip()
        self.assertEqual(expect, mock_stdout.getvalue().strip())

    @patch("sys.stdout", new_callable=StringIO)
    def test_interior_removed(self, mock_stdout) -> None:
        # given
        original = """
foo
bar
baz
        """.strip()
        changed = """
foo
baz
        """.strip()
        # when
        actual = print_changes(original, changed)
        # then
        expect = True
        self.assertEqual(expect, actual)
        expect = """
    1 foo
-   2 bar
    3 baz
        """.strip()
        self.assertEqual(expect, mock_stdout.getvalue().strip())

    @patch("sys.stdout", new_callable=StringIO)
    def test_interior_added(self, mock_stdout) -> None:
        # given
        original = """
foo
baz
        """.strip()
        changed = """
foo
bar
baz
        """.strip()
        # when
        actual = print_changes(original, changed)
        # then
        expect = True
        self.assertEqual(expect, actual)
        expect = """
    1 foo
+     bar
    2 baz
        """.strip()
        self.assertEqual(expect, mock_stdout.getvalue().strip())

    @patch("sys.stdout", new_callable=StringIO)
    def test_interior_changed(self, mock_stdout) -> None:
        # given
        original = """
foo
bar
baz
        """.strip()
        changed = """
foo
qux
baz
        """.strip()
        # when
        actual = print_changes(original, changed)
        # then
        expect = True
        self.assertEqual(expect, actual)
        expect = """
    1 foo
-   2 bar
+     qux
    3 baz
        """.strip()
        self.assertEqual(expect, mock_stdout.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
