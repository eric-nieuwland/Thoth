import unittest

from pydantic import ValidationError

from model.multi_lingual_text import MultiLingualText


class TestMultiLingualTextCreate(unittest.TestCase):

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


class TestMultiLingualTextCheckLanguageCodes(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_create_with_non_language_key(self):
        # given
        text = {"skibidi": "foo bar baz"}
        # when
        # then
        with self.assertRaises(ValidationError):
            MultiLingualText(text)


class TestMultiLingualTextNormaliseLines(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_single_line(self):
        # given
        text = {"nl": "  foo bar baz  "}
        mlt = MultiLingualText(text)
        # when
        actual = mlt["nl"]
        # then
        expect = "foo bar baz"
        self.assertEqual(expect, actual)

    def test_paragraph_multiple_lines(self):
        # given
        text = {"nl": "  foo\n bar \nbaz  "}
        mlt = MultiLingualText(text)
        # when
        actual = mlt["nl"]
        # then
        expect = "foo bar baz"
        self.assertEqual(expect, actual)

    def test_multiple_paragraphs(self):
        # given
        text = {"nl": "  foo\n \nbar \n\n\n baz \n \n "}
        mlt = MultiLingualText(text)
        # when
        actual = mlt["nl"]
        # then
        expect = "foo\n\nbar\n\nbaz"
        self.assertEqual(expect, actual)

    def test_multiline_preservation(self):
        # given
        text = {
            "en": """
This text is split over two lines
and becomes one once loaded.
            """.strip(),
            "nl": """
Dit is alinea #1.

Dit is alinea #2.
            """.strip(),
        }
        mlt = MultiLingualText(text)
        # when
        actual = mlt.root
        # then
        expect = {
            "en": """This text is split over two lines and becomes one once loaded.""",
            "nl": """Dit is alinea #1.\n\nDit is alinea #2.""",
        }
        self.assertDictEqual(expect, actual)


class TestMultiLingualTextAdd(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

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

class TestMultiLingualTextGet(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

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


class TestMultiLingualTextset(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_overwrite(self):
        # given
        text = {"en": "foo bar baz"}
        actual = MultiLingualText(text)
        # when
        # then
        with self.assertRaises(KeyError):
            actual["en"] = "aap noot mies"


class TestMultiLingualTextMisc(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_count_multi_lingual(self):
        # given
        text = {
            "en": """
This text is split over two lines
and becomes one once loaded.
            """.strip(),
            "nl": """
Dit is alinea #1.

Dit is alinea #2.
            """.strip(),
        }
        mlt = MultiLingualText(text)
        # when
        actual = mlt.count_multi_lingual()
        # then
        expect = 1, {
            "en": 1,
            "nl": 1,
        }
        self.assertTupleEqual(expect, actual)

    def test_copy_for_language(self):
        # given
        text = {
            "en": """
This text is split over two lines
and becomes one once loaded.
            """.strip(),
            "nl": """
Dit is alinea #1.

Dit is alinea #2.
            """.strip(),
        }
        mlt = MultiLingualText(text)
        # when
        actual = mlt.copy_for_language("nl", "de").root
        # then
        expect = {
            "de": "please fill with text",
            "nl": "Dit is alinea #1.\n\nDit is alinea #2.",
        }
        self.assertDictEqual(expect, actual)


class TestMultiLingualTextJoin(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_empty_empty(self):
        # given
        text_1 = {}
        text_2 = {}
        mlt_1 = MultiLingualText(text_1)
        mlt_2 = MultiLingualText(text_2)
        # when
        actual = MultiLingualText.join(mlt_1, mlt_2).root
        # then
        expect = {}
        self.assertDictEqual(expect, actual)

    def test_non_empty_empty(self):
        # given
        text_1 = {
            "en": "foo bar baz",
            "nl": "aap noot mies",
        }
        text_2 = {}
        mlt_1 = MultiLingualText(text_1)
        mlt_2 = MultiLingualText(text_2)
        # when
        actual = MultiLingualText.join(mlt_1, mlt_2).root
        # then
        expect = {
            "en": "foo bar baz",
            "nl": "aap noot mies",
        }
        self.assertDictEqual(expect, actual)

    def test_empty_non_empty(self):
        # given
        text_1 = {}
        text_2 = {
            "en": "foo bar baz",
            "nl": "aap noot mies",
        }
        mlt_1 = MultiLingualText(text_1)
        mlt_2 = MultiLingualText(text_2)
        # when
        actual = MultiLingualText.join(mlt_1, mlt_2).root
        # then
        expect = {
            "en": "foo bar baz",
            "nl": "aap noot mies",
        }
        self.assertDictEqual(expect, actual)

    def test_no_overlap(self):
        # given
        text_1 = {
            "en": "foo bar baz",
        }
        text_2 = {
            "nl": "aap noot mies",
        }
        mlt_1 = MultiLingualText(text_1)
        mlt_2 = MultiLingualText(text_2)
        # when
        actual = MultiLingualText.join(mlt_1, mlt_2).root
        # then
        expect = {
            "en": "foo bar baz",
            "nl": "aap noot mies",
        }
        self.assertDictEqual(expect, actual)

    def test_overlap(self):
        # given
        text_1 = {
            "en": "foo bar baz",
            "de": "unvollendet",
        }
        text_2 = {
            "nl": "aap noot mies",
            "de": "wohltemperiert",
        }
        mlt_1 = MultiLingualText(text_1)
        mlt_2 = MultiLingualText(text_2)
        # when
        # then
        with self.assertRaises(ValueError):
            _ = MultiLingualText.join(mlt_1, mlt_2).root


if __name__ == "__main__":
    unittest.main()
