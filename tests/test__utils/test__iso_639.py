import random
import unittest

from utils import iso_639


class TestIsISO639LanguageCode(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_known(self):
        # given
        for code in random.choices(list(iso_639.ISO_639), k=4):
            # when
            actual = iso_639.is_iso_639_language_code(code)
            # then
            self.assertTrue(actual, msg=f"failed for '{code}'")

    def test_unknown(self):
        # given
        for code in ["", "x", "xx", "xxx"]:
            # when
            actual = iso_639.is_iso_639_language_code(code)
            # then
            self.assertFalse(actual, msg=f"failed for '{code}'")


class TestKnownISO639LanguageCodeOrError(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_known(self):
        # given
        for code in random.choices(list(iso_639.ISO_639), k=4):
            # when
            iso_639.known_iso_639_language_code_or_error(code)
            # then
            pass

    def test_unknown(self):
        # given
        for code in ["", "x", "xx", "xxx"]:
            # when
            # then
            with self.assertRaises(ValueError):
                iso_639.known_iso_639_language_code_or_error(code)


class TestISO639LanguageName(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_known(self):
        # given
        for code in random.choices(list(iso_639.ISO_639), k=4):
            # when
            actual = iso_639.iso_639_language_name(code)
            # then
            expect = iso_639.ISO_639[code]
            self.assertEqual(expect, actual, msg=f"failed for '{code}'")

    def test_unknown(self):
        # given
        for code in ["", "x", "xx", "xxx"]:
            # when
            # then
            with self.assertRaises(ValueError):
                iso_639.iso_639_language_name(code)


if __name__ == "__main__":
    unittest.main()
