import unittest

from pydantic import ValidationError

from model.multi_lingual_text import MultiLingualText


class TestMultiLingualText(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_create_from_nothing(self):
        # given
        text = None
        # when
        # then
        with self.assertRaises(ValidationError):
            MultiLingualText(text)

    def test_create_from_empty_dict(self):
        # given
        text = {}
        # when
        actual = MultiLingualText(text)
        # then
        expect = 0
        self.assertEqual(expect, len(actual.root))
        expect = "<MultiLingualText:>"
        self.assertEqual(expect, repr(actual))
        expect = "<T||T>"
        self.assertEqual(expect, str(actual))

    def test_create_with_non_string_key(self):
        # given
        text = {42: "foo bar baz"}
        # when
        # then
        with self.assertRaises(ValidationError):
            MultiLingualText(text)

    def test_create_with_non_string_value(self):
        # given
        text = {"en": 42}
        # when
        # then
        with self.assertRaises(ValidationError):
            MultiLingualText(text)

    def test_create_with_non_language_key(self):
        # given
        text = {"skibidi": "foo bar baz"}
        # when
        # then
        with self.assertRaises(ValidationError):
            MultiLingualText(text)

    def test_add_to_empty(self):
        # given
        text = {}
        actual = MultiLingualText(text)
        # when
        actual["nl"] = "aap noot mies"
        # then
        expect = 1
        self.assertEqual(expect, len(actual.root))
        expect = """
<MultiLingualText:
  |nl| 'aap noot mies'
>
        """.strip()
        self.assertEqual(expect, repr(actual))
        expect = "<T|'nl': 'aap noot mies'|T>"
        self.assertEqual(expect, str(actual))

    def test_add_to_non_empty(self):
        # given
        text = {"en": "foo bar baz"}
        actual = MultiLingualText(text)
        # when
        actual["nl"] = "aap noot mies"
        # then
        expect = 2
        self.assertEqual(expect, len(actual.root))
        expect = """
<MultiLingualText:
  |en| 'foo bar baz'
  |nl| 'aap noot mies'
>
        """.strip()
        self.assertEqual(expect, repr(actual))
        expect = "<T|'en': 'foo bar baz'; 'nl': 'aap noot mies'|T>"
        self.assertEqual(expect, str(actual))

    def test_overwrite(self):
        # given
        text = {"en": "foo bar baz"}
        actual = MultiLingualText(text)
        # when
        # then
        with self.assertRaises(KeyError):
            actual["en"] = "aap noot mies"

    def test_get_existing_key(self):
        # given
        text = {"en": "foo bar baz"}
        mlt = MultiLingualText(text)
        # when
        actual = mlt["en"]
        # then
        expect = "foo bar baz"
        self.assertEqual(expect, actual)

    def test_get_non_existing_key(self):
        # given
        text = {"en": "foo bar baz"}
        mlt = MultiLingualText(text)
        # when
        actual = mlt["nl"]
        # then
        expect = "WARNING: text not available in 'nl'; text available in 'en'"
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
