import unittest

from utils.flatten import flatten


class TestFlatten(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_empty(self):
        """
        empty remains empty
        """
        # given
        lst = []
        # when
        actual = flatten(lst)
        # then
        expect = []
        self.assertListEqual(expect, actual)

    def test_non_list(self):
        """
        non-list/tuple remains the same
        """
        # given
        for lst in 42, "foo", {}, set():
            # when
            actual = flatten(lst)
            # then
            expect = lst
            self.assertEqual(expect, actual, msg=f"failed for {lst=}")

    def test_already_flat(self):
        """
        already flat remains flat
        """
        # given
        lst = [1, "foo", "bar", 42, "baz"]
        # when
        actual = flatten(lst)
        # then
        expect = [1, "foo", "bar", 42, "baz"]
        self.assertListEqual(expect, actual)

    def test_one_level(self):
        """
        one level nesting removed
        """
        # given
        lst = [1, "foo", ("bar", 42,), "baz"]
        # when
        actual = flatten(lst)
        # then
        expect = [1, "foo", "bar", 42, "baz"]
        self.assertListEqual(expect, actual)

    def test_two_levels(self):
        """
        two levels nesting removed
        """
        # given
        lst = [1, ("foo", ["bar",], 42,), "baz"]
        # when
        actual = flatten(lst)
        # then
        expect = [1, "foo", "bar", 42, "baz"]
        self.assertListEqual(expect, actual)

    def test_many_levels(self):
        """
        many levels nesting removed
        """
        # given
        lst = [1, ("foo", ["bar", (42, ["baz",],),],),]
        # when
        actual = flatten(lst)
        # then
        expect = [1, "foo", "bar", 42, "baz"]
        self.assertListEqual(expect, actual)

    def test_tree_like(self):
        """
        tree like nesting removed
        """
        # given
        lst = [((1,), "foo",), "bar", (42, ["baz",])]
        # when
        actual = flatten(lst)
        # then
        expect = [1, "foo", "bar", 42, "baz"]
        self.assertListEqual(expect, actual)

    def test_tuple(self):
        """
        get a tuple when top level argument is a tuple
        """
        # given
        lst = (((1,), "foo",), "bar", (42, ["baz",]),)
        # when
        actual = flatten(lst)
        # then
        expect = (1, "foo", "bar", 42, "baz",)
        self.assertTupleEqual(expect, actual)

    def test_nested_empty_01(self):
        """
        a nested empty list/tuple disappears
        """
        # given
        lst = ([],)
        # when
        actual = flatten(lst)
        # then
        expect = tuple()
        self.assertTupleEqual(expect, actual)

    def test_nested_empty_02(self):
        """
        a nested empty list/tuple disappears
        """
        # given
        lst = ["foo", 42, [], "bar", tuple(), "baz",]
        # when
        actual = flatten(lst)
        # then
        expect = ["foo", 42, "bar", "baz",]
        self.assertListEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
