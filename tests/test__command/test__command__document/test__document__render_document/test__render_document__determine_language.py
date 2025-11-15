import unittest
from unittest.mock import MagicMock, call, patch

from thoth.command.document.render_document import determine_language


class TestDetermineLanguage(unittest.TestCase):
    """
    test determine_language() function
    """

    def setUp(self) -> None:
        self.maxDiff = None

    @patch("thoth.command.document.render_document._notify")
    def test__nothing(self, mock_notify):
        # given
        language = None
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {}
        document_path = "MOCK document path"
        fragments = None
        fragments_path = None
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = None
        self.assertEqual(expect, actual)
        expect = []
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__no_lang__doc__no_frag(self, mock_notify):
        # given
        language = None
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0}
        document_path = "MOCK document path"
        fragments = None
        fragments_path = None
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = "foo"
        self.assertEqual(expect, actual)
        expect = [
            call("NOTE: language 'foo' automatically selected"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__no_lang__no_doc__frag(self, mock_notify):
        # given
        language = None
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"bar": 0}
        fragments_path = "MOCK fragments path"
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = "bar"
        self.assertEqual(expect, actual)
        expect = [
            call("NOTE: language 'bar' automatically selected"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__no_lang__no_overlap(self, mock_notify):
        # given
        language = None
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"bar": 0}
        fragments_path = "MOCK fragments path"
        # when
        # then
        with self.assertRaises(SystemExit):
            _ = determine_language(language, document, document_path, fragments, fragments_path)
        expect = [
            call("no language selected, document and fragments do not share languages"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__no_lang__multiple_overlap(self, mock_notify):
        # given
        language = None
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0, "bar": 0, "baz": 0}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"bar": 0, "baz": 0, "qux": 0}
        fragments_path = "MOCK fragments path"
        # when
        # then
        with self.assertRaises(SystemExit):
            _ = determine_language(language, document, document_path, fragments, fragments_path)
        expect = [
            call("no language selected, document and fragments contain languages 'bar' and 'baz'"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__no_lang__one_overlap(self, mock_notify):
        # given
        language = None
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0, "baz": 0}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"bar": 0, "baz": 0, "qux": 0}
        fragments_path = "MOCK fragments path"
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = "baz"
        self.assertEqual(expect, actual)
        expect = [
            call("NOTE: language 'baz' automatically selected"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__no_lang__one_overlap__incomplete(self, mock_notify):
        # given
        language = None
        document = MagicMock()
        document.count_multi_lingual.return_value = 1, {"foo": 0, "baz": 0}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 1, {"bar": 0, "baz": 0, "qux": 0}
        fragments_path = "MOCK fragments path"
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = "baz"
        self.assertEqual(expect, actual)
        expect = [
            call("NOTE: language 'baz' automatically selected"),
            call("WARNING: language 'baz' incomplete in - MOCK document path, MOCK fragments path\n     check output for warnings"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__no_doc__no_frag(self, mock_notify):
        # given
        language = "que"
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {}
        document_path = "MOCK document path"
        fragments = None
        fragments_path = None
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = None
        self.assertEqual(expect, actual)
        expect = []
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__doc_no_match__no_frag(self, mock_notify):
        # given
        language = "que"
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0}
        document_path = "MOCK document path"
        fragments = None
        fragments_path = None
        # when
        # then
        with self.assertRaises(SystemExit):
            _ = determine_language(language, document, document_path, fragments, fragments_path)
        expect = [
            call("language 'que' not in - MOCK document path"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__doc_match__no_frag(self, mock_notify):
        # given
        language = "foo"
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0}
        document_path = "MOCK document path"
        fragments = None
        fragments_path = None
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = "foo"
        self.assertEqual(expect, actual)
        expect = []
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__no_doc__frag_no_match(self, mock_notify):
        # given
        language = "que"
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"bar": 0}
        fragments_path = "MOCK fragments path"
        # when
        # then
        with self.assertRaises(SystemExit):
            _ = determine_language(language, document, document_path, fragments, fragments_path)
        expect = [
            call("language 'que' not in - MOCK fragments path"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__no_doc__frag_match(self, mock_notify):
        # given
        language = "que"
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"que": 0}
        fragments_path = "MOCK fragments path"
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = "que"
        self.assertEqual(expect, actual)
        expect = []
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__no_overlap(self, mock_notify):
        # given
        language = "que"
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"bar": 0}
        fragments_path = "MOCK fragments path"
        # when
        # then
        with self.assertRaises(SystemExit):
            _ = determine_language(language, document, document_path, fragments, fragments_path)
        expect = [
            call("no language selected, document and fragments do not share languages"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__multiple_overlap_no_match(self, mock_notify):
        # given
        language = "que"
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0, "bar": 0, "baz": 0}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"bar": 0, "baz": 0, "qux": 0}
        fragments_path = "MOCK fragments path"
        # when
        # then
        with self.assertRaises(SystemExit):
            _ = determine_language(language, document, document_path, fragments, fragments_path)
        expect = [
            call("language 'que' not in - MOCK document path, MOCK fragments path"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__multiple_overlap_match(self, mock_notify):
        # given
        language = "baz"
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0, "bar": 0, "baz": 0}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"bar": 0, "baz": 0, "qux": 0}
        fragments_path = "MOCK fragments path"
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = "baz"
        self.assertEqual(expect, actual)
        expect = []
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__one_overlap_no_match(self, mock_notify):
        # given
        language = "que"
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0, "baz": 0}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"bar": 0, "baz": 0, "qux": 0}
        fragments_path = "MOCK fragments path"
        # when
        # then
        with self.assertRaises(SystemExit):
            _ = determine_language(language, document, document_path, fragments, fragments_path)
        expect = [
            call("language 'que' not in - MOCK document path, MOCK fragments path"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__one_overlap_match(self, mock_notify):
        # given
        language = "baz"
        document = MagicMock()
        document.count_multi_lingual.return_value = 0, {"foo": 0, "baz": 0}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 0, {"bar": 0, "baz": 0, "qux": 0}
        fragments_path = "MOCK fragments path"
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = "baz"
        self.assertEqual(expect, actual)
        expect = []
        self.assertListEqual(expect, mock_notify.mock_calls)

    @patch("thoth.command.document.render_document._notify")
    def test__lang__one_overlap__incomplete(self, mock_notify):
        # given
        language = "baz"
        document = MagicMock()
        document.count_multi_lingual.return_value = 1, {"foo": 0, "baz": 0}
        document_path = "MOCK document path"
        fragments = MagicMock()
        fragments.count_multi_lingual.return_value = 1, {"bar": 0, "baz": 0, "qux": 0}
        fragments_path = "MOCK fragments path"
        # when
        actual = determine_language(language, document, document_path, fragments, fragments_path)
        # then
        expect = "baz"
        self.assertEqual(expect, actual)
        expect = [
            call("WARNING: language 'baz' incomplete in - MOCK document path, MOCK fragments path\n     check output for warnings"),
        ]
        self.assertListEqual(expect, mock_notify.mock_calls)


if __name__ == "__main__":
    unittest.main()
