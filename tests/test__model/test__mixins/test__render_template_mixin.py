import unittest
from types import UnionType

from pydantic.fields import FieldInfo

from model.mixins.render_template_mixin import RenderTemplateMixIn, add_counts


class TestRenderTemplateMixInSetIndent(unittest.TestCase):
    """
    test RenderTemplateMixIn.set_indent() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_string(self):
        # given
        indent = "foo"
        RenderTemplateMixIn.set_indent(indent)
        # when
        actual = RenderTemplateMixIn._INDENT_PREFIX
        # then
        expect = "foo"
        self.assertEqual(expect, actual)

    def test_positive_int(self):
        # given
        indent = 2
        RenderTemplateMixIn.set_indent(indent)
        # when
        actual = RenderTemplateMixIn._INDENT_PREFIX
        # then
        expect = "  "
        self.assertEqual(expect, actual)

    def test_zero(self):
        # given
        indent = 0
        RenderTemplateMixIn.set_indent(indent)
        # when
        actual = RenderTemplateMixIn._INDENT_PREFIX
        # then
        expect = ""
        self.assertEqual(expect, actual)

    def test_negative_int(self):
        # given
        indent = -2
        RenderTemplateMixIn.set_indent(indent)
        # when
        actual = RenderTemplateMixIn._INDENT_PREFIX
        # then
        expect = ""
        self.assertEqual(expect, actual)

    def test_wrong_type(self):
        # given
        for indent in (3.14, [], {}, tuple()):
            # when
            # then
            with self.assertRaises(TypeError, msg=f"failed for {indent}"):
                RenderTemplateMixIn.set_indent(indent)


class TestRenderTemplateMixInIndent(unittest.TestCase):
    """
    test RenderTemplateMixIn.indent() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_string(self):
        # given
        RenderTemplateMixIn.set_indent(4)
        text = "foo"
        # when
        actual = RenderTemplateMixIn.indent(text)
        # then
        expect = "    foo"
        self.assertEqual(expect, actual)

    def test_list_of_strings(self):
        # given
        RenderTemplateMixIn.set_indent(4)
        text = [
            "foo",
            "  bar",
            "baz",
        ]
        # when
        actual = RenderTemplateMixIn.indent(text)
        # then
        expect = [
            "    foo",
            "      bar",
            "    baz",
        ]
        self.assertEqual(expect, actual)

    def test_wrong_type(self):
        # given
        for indent in (42, 3.14, {}, tuple()):
            # when
            # then
            with self.assertRaises(TypeError, msg=f"failed for {indent}"):
                RenderTemplateMixIn.indent(indent)


class TestRenderTemplateMixInSingular(unittest.TestCase):
    """
    test RenderTemplateMixIn.singular() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_all(self):
        # given
        for text, expect in (
            ("bars", "bar"),
            ("barbers", "barber"),
            ("barbies", "barby"),
            ("foo", "foo"),
            ("heroes", "hero"),
            ("knives", "knife"),
            ("parts", "part"),
            ("parties", "party"),
            ("ponies", "pony"),
            ("wives", "wife"),
        ):
            # when
            actual = RenderTemplateMixIn.singular(text)
            # then
            self.assertEqual(expect, actual, msg=f"failed for {text}")


class TestRenderTemplateMixInFieldTypeBase(unittest.TestCase):
    """
    test RenderTemplateMixIn.field_type_base() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_no_info(self):
        # given
        field_info = FieldInfo()
        # when
        actual = RenderTemplateMixIn.field_type_base(field_info)
        # then
        expect = None, None
        self.assertTupleEqual(expect, actual)

    def test_annotation_basic_type(self):
        for t in (str, int, float, bool):
            # given
            field_info = FieldInfo(annotation=t)
            # when
            actual = RenderTemplateMixIn.field_type_base(field_info)
            # then
            expect = t, None
            self.assertTupleEqual(expect, actual, msg=f"failed for {t}")

    def test_annotation_collection_type(self):
        for c in (list, tuple, set):
            for t in (str, int, float, bool):
                # given
                field_info = FieldInfo(annotation=c[t])
                # when
                actual = RenderTemplateMixIn.field_type_base(field_info)
                # then
                expect = c, (t,)
                self.assertTupleEqual(expect, actual, msg=f"failed for {c} and {t}")

    def test_annotation_union_type(self):
        # given
        field_info = FieldInfo(annotation=str | int | float | bool)
        # when
        actual = RenderTemplateMixIn.field_type_base(field_info)
        # then
        expect = UnionType, (str, int, float, bool,)
        self.assertTupleEqual(expect, actual)


class TestAddCounts(unittest.TestCase):
    """
    test add_counts() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_zero_zero(self):
        # given
        a = b = 0, {}
        # when
        actual = add_counts(a, b)
        # then
        expect = 0, {}
        self.assertTupleEqual(expect, actual)

    def test_zero_one(self):
        # given
        a = 0, {}
        b = 1, {"en": 1, "nl": 1}
        # when
        actual = add_counts(a, b)
        # then
        expect = 1, {"en": 1, "nl": 1}
        self.assertTupleEqual(expect, actual)

    def test_one_one(self):
        # given
        a = 1, {"en": 1}
        b = 1, {"nl": 1}
        # when
        actual = add_counts(a, b)
        # then
        expect = 2, {"en": 1, "nl": 1}
        self.assertTupleEqual(expect, actual)

    def test_some_some(self):
        # given
        a = 3, {"en": 2, "nl": 1}
        b = 3, {"en": 1, "nl": 2}
        # when
        actual = add_counts(a, b)
        # then
        expect = 6, {"en": 3, "nl": 3}
        self.assertTupleEqual(expect, actual)


if __name__ == "__main__":
    unittest.main()
