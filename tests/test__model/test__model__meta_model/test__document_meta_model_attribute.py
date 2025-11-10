import unittest
from unittest.mock import patch
from typing import Any

from model.document_model import DocumentModelAttribute, DocumentModel
from pydantic import ValidationError


class TestDocumentMetaModelAttributeCreate(unittest.TestCase):
    """
    test DocumentMetaModelAttribute creation
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_unknown_type(self):
        # given
        # when
        # then
        with self.assertRaises(ValueError):
            DocumentModelAttribute(type="unknown")

    def test_known_type_required_no_default(self):
        # given
        known_types = "bool", "int", "float", "str", "multilingual"
        # when
        for known_type in known_types:
            actual = DocumentModelAttribute(type=known_type, required=True, repeated=False)
            # then
            expect = known_type
            self.assertEqual(expect, actual.type, msg=f"failed for {known_type}")
            expect = None
            self.assertEqual(expect, actual.struct, msg=f"failed for {known_type}")

    def test_known_type_repeated_no_default(self):
        # given
        known_types = "bool", "int", "float", "str", "multilingual"
        # when
        for known_type in known_types:
            actual = DocumentModelAttribute(type=known_type, required=False, repeated=True)
            # then
            expect = known_type
            self.assertEqual(expect, actual.type, msg=f"failed for {known_type}")
            expect = None
            self.assertEqual(expect, actual.struct, msg=f"failed for {known_type}")

    def test_known_type_required_default(self):
        # given
        known_types = "bool", "int", "float", "str", "multilingual"
        default = "default"
        # when
        for known_type in known_types:
            # then
            with self.assertRaises(ValidationError, msg=f"failed for {known_type}"):
                _ = DocumentModelAttribute(type=known_type, default=default, required=True, repeated=False)

    def test_struct(self):
        # given
        struct = DocumentModel(root={})
        # when
        actual = DocumentModelAttribute(struct=struct)
        # then
        expect = None
        self.assertEqual(expect, actual.type)
        expect = struct
        self.assertEqual(expect, actual.struct)

    def test_struct_default(self):
        # given
        default = "default"
        struct = DocumentModel(root={})
        # when
        # then
        with self.assertRaises(ValidationError):
            _ = DocumentModelAttribute(default=default, struct=struct)

    def test_type_and_struct(self):
        # given
        known_types = "bool", "int", "float", "str", "multilingual"
        struct = DocumentModel(root={})
        # when
        for known_type in known_types:
            # then
            with self.assertRaises(ValidationError, msg=f"failed for {known_type}"):
                _ = DocumentModelAttribute(type=known_type, struct=struct)


class TestDocumentMetaModelAttributeYaml(unittest.TestCase):
    """
    test DocumentMetaModelAttribute YAML stuff
    """

    def setUp(self) -> None:
        self.maxDiff = None

    @staticmethod
    def install_mock_dict(mock, mock_dict):
        mock.__contains__.side_effect = mock_dict.__contains__
        mock.__getitem__.side_effect = mock_dict.__getitem__
        mock.__iter__.side_effect = mock_dict.__iter__
        mock.items.side_effect = mock_dict.items

    @patch("model.mixins.example_mixin.EXAMPLES")
    @patch("model.document_model.TYPE_MAPPING")
    def test_example(self, mock_type_mapping, mock_examples):
        # given
        self.install_mock_dict(
            mock_type_mapping,
            {
                "mock": "MOCK",
            },
        )
        self.install_mock_dict(
            mock_examples,
            {
                bool: (True,),
                int: (1,),
                float: (1.0,),
                str: ("foo bar",),
            },
        )
        # when
        actual = DocumentModelAttribute._example_yaml_dict()
        # then
        expect = {
            "description": "foo bar",
            "repeated": True,
            "required": True,
            "struct": {
                "bar": {
                    "description": "foo bar",
                    "repeated": True,
                    "required": True,
                    "type": "mock",
                },
                "foo": {
                    "description": "foo bar",
                    "repeated": True,
                    "required": True,
                    "type": "mock",
                },
            },
        }
        self.assertDictEqual(expect, actual)


class TestDocumentMetaModelAttributeAsModelDefinition(unittest.TestCase):
    """
    test DocumentMetaModelAttribute.as_model_definition() function
    """

    TYPE_CLASS_DEFAULT: tuple[tuple[str, type, Any], ...] = (
        ("str", str, "default"),
        ("int", int, 42),
        ("float", float, 3.14),
        ("bool", bool, True),
    )

    def setUp(self) -> None:
        self.maxDiff = None

    def test_type_required(self):
        for t, c, d in self.TYPE_CLASS_DEFAULT:
            # given
            args = dict(
                # default=d,
                description="foo bar",
                repeated=False,
                required=True,
                struct=None,
                type=t,
            )
            instance = DocumentModelAttribute(**args)
            # when
            actual = instance.as_model_definition()
            # then
            expect = c
            self.assertEqual(expect, actual, msg=f"failed for {t}")

    def test_type_repeated(self):
        for t, c, d in self.TYPE_CLASS_DEFAULT:
            # given
            args = dict(
                # default=d,
                description="foo bar",
                repeated=True,
                required=False,
                struct=None,
                type=t,
            )
            instance = DocumentModelAttribute(**args)
            # when
            actual = instance.as_model_definition()
            # then
            expect = list[c], []
            self.assertEqual(expect, actual, msg=f"failed for {t}")

    def test_type_optional_with_default(self):
        for t, c, d in self.TYPE_CLASS_DEFAULT:
            # given
            args = dict(
                default=d,
                description="foo bar",
                repeated=False,
                required=False,
                struct=None,
                type=t,
            )
            instance = DocumentModelAttribute(**args)
            # when
            actual = instance.as_model_definition()
            # then
            expect = c, d
            self.assertEqual(expect, actual, msg=f"failed for {t}")

    def test_type_optional_without_default(self):
        for t, c, d in self.TYPE_CLASS_DEFAULT:
            # given
            args = dict(
                # default=d,
                description="foo bar",
                repeated=False,
                required=False,
                struct=None,
                type=t,
            )
            instance = DocumentModelAttribute(**args)
            # when
            actual = instance.as_model_definition()
            # then
            expect = c | None, None
            self.assertEqual(expect, actual, msg=f"failed for {t}")

    def test_struct_optional(self):
        from types import UnionType, NoneType
        from typing import get_origin, get_args
        # given
        args = dict(
            description="the foo bar struct",
            repeated=False,
            required=False,
            struct={
                "foo": dict(
                    description="a foo",
                    repeated=False,
                    required=False,
                    struct=None,
                    type="str",
                ),
                "bar": dict(
                    default=42,
                    description="a bar",
                    repeated=False,
                    required=False,
                    struct=None,
                    type="int",
                ),
            },
            type=None,
        )
        instance = DocumentModelAttribute(**args)
        # when
        actual = instance.as_model_definition("TEST")
        # then
        expect = None
        self.assertEqual(expect, actual[1])
        expect = UnionType
        self.assertEqual(expect, get_origin(actual[0]))
        expect = NoneType
        self.assertIn(expect, get_args(actual[0]))
        actual_dynamic_type = [t for t in get_args(actual[0]) if t != NoneType][0]
        expect = "Test"
        self.assertEqual(expect, actual_dynamic_type.__name__)
        actual_dynamic_instance = actual_dynamic_type()
        self.assertTrue(hasattr(actual_dynamic_instance, "foo"))
        expect = None
        self.assertEqual(expect, actual_dynamic_instance.foo)
        self.assertTrue(hasattr(actual_dynamic_instance, "bar"))
        expect = 42
        self.assertEqual(expect, actual_dynamic_instance.bar)
        self.assertFalse(hasattr(actual_dynamic_instance, "qux"))


if __name__ == "__main__":
    unittest.main()
