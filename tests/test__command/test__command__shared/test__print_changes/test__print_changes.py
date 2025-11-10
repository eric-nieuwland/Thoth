import unittest
from unittest.mock import patch

from thoth.command.shared.print_changes import print_changes


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
