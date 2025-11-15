import unittest
from unittest.mock import MagicMock, patch

from model.document_model import DocumentModel, DocumentModelAttribute
from pydantic import ValidationError
from pydantic.fields import FieldInfo


class TestDocumentMetaModelCreate(unittest.TestCase):
    """
    test DocumentMetaModel creation
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_empty(self):
        # given
        root = {}
        # when
        actual = DocumentModel(root=root)
        # then
        expect = {}
        self.assertDictEqual(expect, actual.root)

    def test_not_empty_wrong_type(self):
        # given
        attribute_values_wrong_type = True, 1, 1.0, "skibidi"
        # when
        for attribute_value_wrong_type in attribute_values_wrong_type:
            root = {
                "foo": attribute_value_wrong_type,
                "bar": attribute_value_wrong_type,
                "baz": attribute_value_wrong_type,
            }
            # then
            with self.assertRaises(ValidationError):
                _ = DocumentModel(root=root)

    def test_not_empty_right_type(self):
        mock_attribute = DocumentModelAttribute(type="str", required=True)
        # given
        root = {
            "foo": mock_attribute,
            "bar": mock_attribute,
            "baz": mock_attribute,
        }
        # when
        actual = DocumentModel(root=root)
        # then
        expect = {
            "foo": mock_attribute,
            "bar": mock_attribute,
            "baz": mock_attribute,
        }
        self.assertDictEqual(expect, actual.root)


class TestDocumentMetaModelCreateDocumentClass(unittest.TestCase):
    """
    test DocumentMetaModel.create_document_class() method
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_empty(self):
        # given
        root = {}
        model = DocumentModel(root=root)
        # when
        actual = model.create_document_class("TEST")
        # then
        expect = "Test"
        self.assertEqual(expect, actual.__name__)
        expect = set()  # not interested in attribute conversion, just names
        self.assertSetEqual(expect, set(actual.model_fields))

    def test_not_empty(self):
        mock_attribute = DocumentModelAttribute(type="str", required=True)
        # given
        root = {
            "foo": mock_attribute,
            "bar": mock_attribute,
            "baz": mock_attribute,
        }
        model = DocumentModel(root=root)
        # when
        actual = model.create_document_class("TEST")
        # then
        expect = {  # not interested in attribute conversion, just names
            "foo",
            "bar",
            "baz",
        }
        self.assertSetEqual(expect, set(actual.model_fields))
        # all elements should be of the type set by 'nested_attribute'
        expect = str
        for name, field in actual.model_fields.items():
            self.assertEqual(expect, field.annotation, msg=f"failed for {name}")

    def test_nested(self):
        nested_attribute = DocumentModelAttribute(type="str", required=True)
        # given
        nested_root = {
            "foo": nested_attribute,
            "bar": nested_attribute,
            "baz": nested_attribute,
        }
        nested_model = DocumentModel(root=nested_root)
        struct = DocumentModelAttribute(struct=nested_model, required=True)
        root = {
            "qux": struct,
        }
        model = DocumentModel(root=root)
        # when
        actual = model.create_document_class("TEST")
        # then
        expect = {  # not interested in attribute conversion, just names
            "qux",
        }
        self.assertSetEqual(expect, set(actual.model_fields))
        expect = {  # not interested in attribute conversion, just names
            "foo",
            "bar",
            "baz",
        }
        self.assertSetEqual(expect, set(actual.model_fields["qux"].annotation.model_fields))
        # all elements should be of the type set by 'nested_attribute'
        expect = str
        for name, field in actual.model_fields["qux"].annotation.model_fields.items():
            self.assertEqual(expect, field.annotation, msg=f"failed for {name}")


class TestDocumentMetaModelCreateProfileClass(unittest.TestCase):
    """
    test DocumentMetaModel.create_profile_class() method
    """

    def setUp(self) -> None:
        self.maxDiff = None

    def test_empty(self):
        # given
        root = {}
        model = DocumentModel(root=root)
        # when
        actual = model.create_profile_class("TEST")
        # then
        expect = "Test"
        self.assertEqual(expect, actual.__name__)
        expect = set()  # not interested in attribute conversion, just names
        self.assertSetEqual(expect, set(actual.model_fields))

    def test_not_empty(self):
        mock_attribute = DocumentModelAttribute(type="str", required=True)
        # given
        root = {
            "foo": mock_attribute,
            "bar": mock_attribute,
            "baz": mock_attribute,
        }
        model = DocumentModel(root=root)
        # when
        actual = model.create_profile_class("TEST")
        # then
        expect = {  # not interested in attribute conversion, just names
            "foo",
            "bar",
            "baz",
        }
        self.assertSetEqual(expect, set(actual.model_fields))
        # all elements should be boolean
        expect = bool
        for name, field in actual.model_fields.items():
            self.assertEqual(expect, field.annotation, msg=f"failed for {name}")

    def test_nested(self):
        nested_attribute = DocumentModelAttribute(type="str", required=True)
        # given
        nested_root = {
            "foo": nested_attribute,
            "bar": nested_attribute,
            "baz": nested_attribute,
        }
        nested_model = DocumentModel(root=nested_root)
        struct = DocumentModelAttribute(struct=nested_model, required=True)
        root = {
            "qux": struct,
        }
        model = DocumentModel(root=root)
        # when
        actual = model.create_profile_class("TEST")
        # then
        expect = {  # not interested in attribute conversion, just names
            "qux",
        }
        self.assertSetEqual(expect, set(actual.model_fields))
        expect = {  # not interested in attribute conversion, just names
            "foo",
            "bar",
            "baz",
        }
        self.assertSetEqual(expect, set(actual.model_fields["qux"].annotation.model_fields))
        # all elements should be boolean
        expect = bool
        for name, field in actual.model_fields["qux"].annotation.model_fields.items():
            self.assertEqual(expect, field.annotation, msg=f"failed for {name}")


if __name__ == "__main__":
    unittest.main()
