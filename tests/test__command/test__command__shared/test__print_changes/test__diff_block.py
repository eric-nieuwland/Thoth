import unittest
import string

from thoth.command.shared.print_changes import DiffBlock


class TestDiffBlockAddLine(unittest.TestCase):
    """
    test DiffBlock.add_line() method
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_line_not_recognised(self):
        # given
        instance = DiffBlock(1)
        instance.context = 2
        not_recognised = set(string.printable) - {" ", "+", "-"}
        # when
        # then
        for first in not_recognised:
            with self.assertRaises(ValueError, msg=f"failed for {first!r}"):
                instance.add_line(f"{first}foo bar baz")

    def test_ignore_change(self):
        # given
        for line in (
            "-           ",  # essentially empty
            "-  # comment",
        ):
            instance = DiffBlock(1)
            instance.context = 2
            # when
            instance.add_line(line)
            # then
            msg = f"failed for {line!r}"
            expect = [
                (" ", line[1:]),
            ]
            self.assertListEqual(expect, instance.text, msg=msg)
            expect = 1
            self.assertEqual(expect, instance.line_nr, msg=msg)
            expect = None
            self.assertEqual(expect, instance.last_change, msg=msg)

    def test_add_change_to_empty(self):
        # given
        for first in ("+", "-"):
            instance = DiffBlock(1)
            instance.context = 2
            # when
            instance.add_line(f"{first}foo bar baz")
            # then
            msg = f"failed for {first!r}"
            expect = [
                (first, "foo bar baz"),
            ]
            self.assertListEqual(expect, instance.text, msg=msg)
            expect = 1
            self.assertEqual(expect, instance.line_nr, msg=msg)
            expect = 0
            self.assertEqual(expect, instance.last_change, msg=msg)

    def test_add_non_change_within_context(self):
        # given
        instance = DiffBlock(1)
        instance.context = 2
        instance.text = [
            (" ", "context #1"),
        ]
        # when
        instance.add_line(f" foo bar baz")
        # then
        expect = [
            (" ", "context #1"),
            (" " , "foo bar baz"),
        ]
        self.assertListEqual(expect, instance.text)
        expect = 1
        self.assertEqual(expect, instance.line_nr)
        expect = None
        self.assertEqual(expect, instance.last_change)

    def test_add_non_change_full_context(self):
        for context in range(1, 7):
            msg = f"failed for {context}"
            # given
            instance = DiffBlock(1)
            instance.context = context
            instance.text = [
                (" ", f"context #{n}") for n in range(1, context+1)
            ]
            # when
            instance.add_line(f" foo bar baz")
            # then
            expect = [
                *((" ", f"context #{n}") for n in range(2, context+1)),
                (" ", "foo bar baz"),
            ]
            self.assertListEqual(expect, instance.text, msg=msg)
            expect = 2
            self.assertEqual(expect, instance.line_nr, msg=msg)
            expect = None
            self.assertEqual(expect, instance.last_change, msg=msg)

    def test_add_non_change_beyond_context(self):
        for context in range(1, 7):
            msg = f"failed for {context}"
            # given
            instance = DiffBlock(1)
            instance.context = context
            instance.text = [
                (" ", f"context #{n}") for n in range(1, 2 * context + 1)
            ]
            # when
            instance.add_line(f" foo bar baz")
            # then
            expect = [ # last context-1 text lines + added line
                *((" ", f"context #{n}") for n in range(context + 2, 2 * context + 1)),
                (" ", "foo bar baz"),
            ]
            self.assertListEqual(expect, instance.text, msg=msg)
            expect = 2 + context
            self.assertEqual(expect, instance.line_nr, msg=msg)
            expect = None
            self.assertEqual(expect, instance.last_change, msg=msg)

    def test_add_change_within_context(self):
        for context in range(1, 7):
            for first in ("+", "-"):
                msg = f"failed for {context} {first!r}"
                # given
                instance = DiffBlock(1)
                instance.context = context
                instance.text = [
                    (" ", f"context #{n}") for n in range(1, context)
                ]
                # when
                instance.add_line(f"{first}foo bar baz")
                # then
                expect = [
                    *((" ", f"context #{n}") for n in range(1, context)),
                    (first, "foo bar baz"),
                ]
                self.assertListEqual(expect, instance.text, msg=msg)
                expect = 1
                self.assertEqual(expect, instance.line_nr, msg=msg)
                expect = context - 1
                self.assertEqual(expect, instance.last_change, msg=msg)

    def test_add_change_beyond_context(self):
        for context in range(1, 7):
            for first in ("+", "-"):
                msg = f"failed for {context} {first!r}"
                # given
                instance = DiffBlock(1)
                instance.context = 2
                instance.text = [
                    (" ", f"context #{n}") for n in range(1, 2 * context + 1)
                ]
                # when
                instance.add_line(f"{first}foo bar baz")
                # then
                expect = [
                    *((" ", f"context #{n}") for n in range(1, 2 * context + 1)),
                    (first, "foo bar baz"),
                ]
                self.assertListEqual(expect, instance.text, msg=msg)
                expect = 1
                self.assertEqual(expect, instance.line_nr, msg=msg)
                expect = 2 * context
                self.assertEqual(expect, instance.last_change, msg=msg)


class TestDiffBlockIter(unittest.TestCase):
    """
    test DiffBlock.__iter__() method
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_empty(self):
        # given
        instance = DiffBlock(1)
        # when
        actual = list(instance)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_no_last_change(self):
        # given
        instance = DiffBlock(1)
        instance.text = [
            (" ", f"line {nr}") for nr in range(1, 11)
        ]
        # when
        actual = list(instance)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_not_first(self):
        # given
        instance = DiffBlock(1)
        instance.text = []
        instance.line_nr = 42
        instance.last_change = 7
        # when
        actual = list(instance)
        # then
        expect = [
            "  ...",
        ]
        self.assertListEqual(expect, actual)

    def test_integrated(self):
        # given
        instance = DiffBlock(1)
        instance.context = 2
        instance.add_line(" line  1 - should not be included")
        instance.add_line(" line  2 - should not be included")
        instance.add_line(" line  3")
        instance.add_line(" line  4")
        instance.add_line("-line  5 original")
        instance.add_line("+line  5 replacement")
        instance.add_line(" line  6")
        instance.add_line("+insertion")
        instance.add_line(" line  7")
        instance.add_line("-line  8 deleted")
        instance.add_line(" line  9")
        instance.add_line(" line 10")
        instance.add_line(" line 11 - should not be included")
        # when
        actual = list(instance)
        # then
        expect = [
            "  ...",
            "    3 line  3",
            "    4 line  4",
            "-   5 line  5 original",
            "+     line  5 replacement",
            "    6 line  6",
            "+     insertion",
            "    7 line  7",
            "-   8 line  8 deleted",
            "    9 line  9",
            "   10 line 10",
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
