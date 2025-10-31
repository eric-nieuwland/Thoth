import unittest
from types import UnionType

from pydantic.fields import FieldInfo, PydanticUndefined

from model.mixins.example_mixin import ExampleMixIn, EXAMPLES


class TestExampleMixInFieldTypeBaseAndDefault(unittest.TestCase):
    """
    test ExampleMixIn.field_type_base_and_default() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_no_info(self):
        # given
        field_info = FieldInfo()
        # when
        actual = ExampleMixIn.field_type_base_and_default(field_info)
        # then
        expect = None, None, PydanticUndefined
        self.assertTupleEqual(expect, actual)

    def test_annotation_basic_type(self):
        for t in (str, int, float, bool):
            # given
            field_info = FieldInfo(annotation=t)
            # when
            actual = ExampleMixIn.field_type_base_and_default(field_info)
            # then
            expect = t, None, PydanticUndefined
            self.assertTupleEqual(expect, actual, msg=f"failed for {t}")

    def test_annotation_collection_type(self):
        for c in (list, tuple, set):
            for t in (str, int, float, bool):
                # given
                field_info = FieldInfo(annotation=c[t])
                # when
                actual = ExampleMixIn.field_type_base_and_default(field_info)
                # then
                expect = c, (t,), PydanticUndefined
                self.assertTupleEqual(expect, actual, msg=f"failed for {c} and {t}")

    def test_annotation_union_type(self):
        # given
        field_info = FieldInfo(annotation=str | int | float | bool)
        # when
        actual = ExampleMixIn.field_type_base_and_default(field_info)
        # then
        expect = UnionType, (str, int, float, bool,), PydanticUndefined
        self.assertTupleEqual(expect, actual)

    def test_annotation_basic_default(self):
        for t, d in (
            (str, "foo"),
            (int, 42),
            (float, 3.14),
            (bool, True),
            (list, []),
        ):
            # given
            field_info = FieldInfo(annotation=t, default=d)
            # when
            actual = ExampleMixIn.field_type_base_and_default(field_info)
            # then
            expect = t, None, d
            self.assertTupleEqual(expect, actual, msg=f"failed for {t} and {d}")

    def test_annotation_collection_default(self):
        for c, t, d in (
            (list, str, ["foo"]),
            (tuple, int, (42, 3)),
        ):
            # given
            field_info = FieldInfo(annotation=c[t], default=d)
            # when
            actual = ExampleMixIn.field_type_base_and_default(field_info)
            # then
            expect = c, (t,), d
            self.assertTupleEqual(expect, actual, msg=f"failed for {c}, {t} and {d}")


class TestExampleMixInExampleForClass(unittest.TestCase):
    """
    test ExampleMixIn.example_for_class() function
    """

    def setUp(self):
        self.maxDiff = None

    def test_example_for_known_class(self):
        # given
        for t in (str, int, float, bool):
            # when
            actual = ExampleMixIn.example_for_class(t)
            # then
            expect = EXAMPLES[t]
            self.assertIn(actual, expect, msg=f"failed for {t}")

    def test_example_for_unknown_class(self):
        # given
        for t in (list, tuple, set, complex):
            # when
            actual = ExampleMixIn.example_for_class(t)
            # then
            self.assertIsNone(actual, msg=f"failed for {t}")


if __name__ == "__main__":
    unittest.main()
