import unittest
from unittest.mock import patch

from model.meta_model import DocumentMetaModelAttribute, DocumentMetaModel
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
            DocumentMetaModelAttribute(type="unknown")

    def test_type_not_required_not_repeated_no_default(self):
        # given
        # when
        # then
        with self.assertRaises(ValidationError):
            _ = DocumentMetaModelAttribute(type="int", required=False, repeated=False)

    def test_known_type_required_no_default(self):
        # given
        known_types = "bool", "int", "float", "str", "multilingual"
        # when
        for known_type in known_types:
            actual = DocumentMetaModelAttribute(type=known_type, required=True, repeated=False)
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
            actual = DocumentMetaModelAttribute(type=known_type, required=False, repeated=True)
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
                _ = DocumentMetaModelAttribute(type=known_type, default=default, required=True, repeated=False)

    def test_struct(self):
        # given
        struct = DocumentMetaModel(root={})
        # when
        actual = DocumentMetaModelAttribute(struct=struct)
        # then
        expect = None
        self.assertEqual(expect, actual.type)
        expect = struct
        self.assertEqual(expect, actual.struct)

    def test_struct_default(self):
        # given
        default = "default"
        struct = DocumentMetaModel(root={})
        # when
        # then
        with self.assertRaises(ValidationError):
            _ = DocumentMetaModelAttribute(default=default, struct=struct)

    def test_type_and_struct(self):
        # given
        known_types = "bool", "int", "float", "str", "multilingual"
        struct = DocumentMetaModel(root={})
        # when
        for known_type in known_types:
            # then
            with self.assertRaises(ValidationError, msg=f"failed for {known_type}"):
                _ = DocumentMetaModelAttribute(type=known_type, struct=struct)


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

    @patch("model.mixins.example_mixin.EXAMPLES")
    @patch("model.meta_model.YAML_EXAMPLES")
    @patch("model.meta_model.TYPES")
    def test_example(self, mock_types, mock_yaml_examples, mock_examples):
        # given
        self.install_mock_dict(
            mock_types,
            {
                "mock": "MOCK",
            },
        )
        self.install_mock_dict(
            mock_yaml_examples,
            {
                "mock": ("MOCK",),
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
        actual = DocumentMetaModelAttribute._example_yaml_dict()
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


if __name__ == "__main__":
    unittest.main()
