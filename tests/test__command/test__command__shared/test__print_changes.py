import unittest
from unittest.mock import patch

from thoth.command.shared.print_changes import human_centric_diff, print_changes


class TestHumanCentricDiff(unittest.TestCase):
    """
    test human_centric_diff() function
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_empties(self) -> None:
        # given
        for original in ([], ""):
            for changed in ([], ""):
                # when
                actual = list(human_centric_diff(original, changed))
                # then
                expect = []
                self.assertListEqual(expect, actual, msg=f"failed for {original!r} and {changed!r}")

    def test_one_line_added(self) -> None:
        # given
        original = ""
        changed = "foo bar"
        # when
        actual = list(human_centric_diff(original, changed))
        # then
        expect = [
            "+     foo bar",
        ]
        self.assertListEqual(expect, actual)

    def test_one_line_removed(self) -> None:
        # given
        original = "foo bar"
        changed = ""
        # when
        actual = list(human_centric_diff(original, changed))
        # then
        expect = [
            "-   1 foo bar",
        ]
        self.assertListEqual(expect, actual)

    def test_one_line_changed(self) -> None:
        # given
        original = "foo bar"
        changed = "baz qux"
        # when
        actual = list(human_centric_diff(original, changed))
        # then
        expect = [
            "-   1 foo bar",
            "+     baz qux",
        ]
        self.assertListEqual(expect, actual)

    def test_interior_removed(self) -> None:
        # given
        original = """
foo
bar
baz
        """.strip()
        changed = [
            "foo",
            "baz",
        ]
        # when
        actual = list(human_centric_diff(original, changed))
        # then
        expect = [
            "    1 foo",
            "-   2 bar",
            "    3 baz",
        ]
        self.assertListEqual(expect, actual)

    def test_interior_added(self) -> None:
        # given
        original = [
            "foo",
            "baz",
        ]
        changed = [
            "foo",
            "bar",
            "baz",
        ]
        # when
        actual = list(human_centric_diff(original, changed))
        # then
        expect = [
            "    1 foo",
            "+     bar",
            "    2 baz",
        ]
        self.assertListEqual(expect, actual)

    def test_interior_changed(self) -> None:
        # given
        original = [
            "foo",
            "bar",
            "baz",
        ]
        changed = [
            "foo",
            "qux",
            "baz",
        ]
        # when
        actual = list(human_centric_diff(original, changed))
        # then
        expect = [
            "    1 foo",
            "-   2 bar",
            "+     qux",
            "    3 baz",
        ]
        self.assertListEqual(expect, actual)


class TestPrintChanges(unittest.TestCase):
    """
    test print_changes() function
    """

    def setUp(self) -> None:
        self.maxDiff = None

    @patch("thoth.command.shared.print_changes.human_centric_diff")
    def test_no_change(self, mock_human_centric_diff) -> None:
        # given
        mock_human_centric_diff.return_value = []
        # when
        actual = print_changes("", "")
        # then
        expect = False
        self.assertEqual(expect, actual)

    @patch("thoth.command.shared.print_changes.human_centric_diff")
    def test_change(self, mock_human_centric_diff) -> None:
        # given
        mock_human_centric_diff.return_value = [""]
        # when
        actual = print_changes("", "")
        # then
        expect = True
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
