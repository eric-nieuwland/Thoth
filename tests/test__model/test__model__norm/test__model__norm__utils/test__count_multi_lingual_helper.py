import unittest
from unittest.mock import MagicMock, call

from model.norm.utils import count_multi_lingual_helper


class TestCountMultiLingualHelper(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_none(self):
        """
        don't count None
        """
        # given
        arg = None
        # when
        actual = count_multi_lingual_helper(arg)
        # then
        expect = 0, {}
        self.assertTupleEqual(expect, actual)

    def test_attribute(self):
        """
        call method iff present
        """
        # given
        arg = MagicMock()
        arg.count_multi_lingual.return_value = "MOCK", "RESULT"
        # when
        actual = count_multi_lingual_helper(arg)
        # then
        expect = [
            call.count_multi_lingual(),
        ]
        self.assertListEqual(expect, arg.mock_calls)
        expect = "MOCK", "RESULT"
        self.assertTupleEqual(expect, actual)

    def test_dict(self):
        """
        call on values for dict
        """
        # given
        sub_arg = MagicMock()
        sub_arg.count_multi_lingual.return_value = 42, {"foo": 13}
        arg = {
            "ignored": sub_arg,
        }
        # when
        actual = count_multi_lingual_helper(arg)
        # then
        expect = [
            call.count_multi_lingual(),
        ]
        self.assertListEqual(expect, sub_arg.mock_calls)
        expect = 42, {"foo": 13}
        self.assertTupleEqual(expect, actual)

    def test_collection_empty(self):
        """
        an empty list
        """
        # given
        arg = []
        # when
        actual = count_multi_lingual_helper(arg)
        # then
        expect = 0, {}
        self.assertTupleEqual(expect, actual)

    def test_collection_one(self):
        """
        a single item set
        """
        # given
        sub_arg = MagicMock()
        sub_arg.count_multi_lingual.return_value = 42, {"foo": 13}
        arg = {
            sub_arg,
        }
        # when
        actual = count_multi_lingual_helper(arg)
        # then
        expect = [
            call.__hash__(),
            call.count_multi_lingual(),
        ]
        self.assertListEqual(expect, sub_arg.mock_calls)
        expect = 42, {"foo": 13}
        self.assertTupleEqual(expect, actual)

    def test_collection_some(self):
        """
        a multi-item tuple
        """
        # given
        sub_arg_1 = MagicMock()
        sub_arg_1.count_multi_lingual.return_value = 1, {"foo": 1}
        sub_arg_2 = MagicMock()
        sub_arg_2.count_multi_lingual.return_value = 2, {"foo": 1, "bar": 1}
        sub_arg_3 = MagicMock()
        sub_arg_3.count_multi_lingual.return_value = 3, {"bar": 1, "baz": 1}
        arg = (
            sub_arg_1,
            sub_arg_2,
            sub_arg_3,
        )
        # when
        actual = count_multi_lingual_helper(arg)
        # then
        expect = [
            call.count_multi_lingual(),
        ]
        self.assertListEqual(expect, sub_arg_1.mock_calls)
        self.assertListEqual(expect, sub_arg_2.mock_calls)
        self.assertListEqual(expect, sub_arg_3.mock_calls)
        expect = 6, {"foo": 2, "bar": 2, "baz": 1}
        self.assertTupleEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
