import unittest

from utils.list_joiner import list_joiner


class TestListJoiner(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_none_none(self):
        """
        2 x None => None
        """
        # given
        lst1 = None
        lst2 = None
        # when
        actual = list_joiner(lst1, lst2)
        # then
        expect = None
        self.assertEqual(expect, actual)

    def test_none_list(self):
        """
        None and list don't go together
        """
        # given
        lst1 = None
        lst2 = []
        # when
        # then
        with self.assertRaises(ValueError):
            list_joiner(lst1, lst2)

    def test_list_none(self):
        """
        list and None don't go together
        """
        # given
        lst1 = []
        lst2 = None
        # when
        # then
        with self.assertRaises(ValueError):
            list_joiner(lst1, lst2)

    def test_uneven_lists_1(self):
        """
        uneven length lists don't go together
        """
        # given
        lst1 = []
        lst2 = ["foo", "bar", "baz"]
        # when
        # then
        with self.assertRaises(ValueError):
            list_joiner(lst1, lst2)

    def test_uneven_lists_2(self):
        """
        uneven length lists don't go together
        """
        # given
        lst1 = ["foo", "bar", "baz"]
        lst2 = []
        # when
        # then
        with self.assertRaises(ValueError):
            list_joiner(lst1, lst2)

    def test_even_lists(self):
        """
        even length lists merge elements
        """
        # given
        lst1 = [{"1.1",}, {"1.2",}, {"1.3",}]
        lst2 = [{"2.1",}, {"2.2",}, {"2.3",}]
        # when
        actual = list_joiner(lst1, lst2)
        # then
        expect = [
            {"1.1", "2.1"},
            {"1.2", "2.2"},
            {"1.3", "2.3"},
        ]
        self.assertListEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
