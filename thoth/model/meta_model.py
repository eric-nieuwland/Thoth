from __future__ import annotations

# standard library
from pathlib import Path
from random import choice
from typing import Any

# third party
from pydantic import BaseModel, RootModel, create_model, model_validator

# own
from .mixins import ExampleMixIn, ProfileMixIn, RenderTemplateMixIn, YamlMixIn
from .multi_lingual_text import MultiLingualText

SUPPORTED_TYPES = str | int | float | bool | MultiLingualText

TYPE_MAPPING = {
    "bool": bool,
    "int": int,
    "float": float,
    "str": str,
    "multilingual": MultiLingualText,
}

YAML_EXAMPLE_VALUES = {
    "bool": (True, False),
    "int": (42, -1, 1984),
    "float": (2.71828183, 3.14159265),
    "str": ("Lorem ipsum dolor sit amet", "Ut labore et dolore magna aliqua"),
}


class DocumentMetaModelAttribute(ExampleMixIn, YamlMixIn, BaseModel):
    default: SUPPORTED_TYPES | None = None
    description: str | None = None
    repeated: bool = False
    required: bool = False
    struct: DocumentMetaModel | None = None
    type: str | None = None

    @model_validator(mode="after")
    def _require_known_type(self):
        """Ensure 'type' is a known type, if defined."""
        has_type = self.type is not None

        if has_type and self.type not in TYPE_MAPPING:
            raise ValueError('Unknown "type" - %s', self.type)

        return self

    @model_validator(mode="after")
    def _require_no_default_for_struct(self):
        """Ensure 'struct' has no default value."""
        has_default = self.default is not None
        has_struct = self.struct is not None

        if has_default and has_struct:
            raise ValueError('Default values for "struct" are not supported.')

        return self

    @model_validator(mode="after")
    def _require_type_default_required_repeated_consistency(self):
        """Ensure 'type' has either default or is required/repeated."""
        has_type = self.type is not None
        has_default = self.default is not None
        is_repeated = self.repeated
        is_required = self.required

        # do the tests apply?
        if not has_type:
            return self
        if is_repeated and not has_default:
            return self

        # are setting consistent?
        if is_repeated and has_default:
            raise ValueError("""Default value for repeated field is meaningless.""")
        if is_required and has_default:
            raise ValueError("""Default value for required field is meaningless.""")
        if not is_required and not has_default:
            raise ValueError("""Need default value for not required field.""")

        return self

    @model_validator(mode="after")
    def _require_either_struct_or_type(self):
        """Ensure exactly one of 'struct' and 'type' is present."""
        has_struct = self.struct is not None
        has_type = self.type is not None

        if not (has_struct or has_type):
            raise ValueError("""Need either "struct" or "type".""")

        if has_struct and has_type:
            raise ValueError("""Need either "struct" or "type", not both.""")

        return self

    @classmethod
    def _example_yaml_dict(cls, stack=[], *_args, **_kwargs) -> dict:
        result = {
            "description": cls._example_yaml_value_for(str, None, stack + ["description"]),
            "repeated": (repeated := cls._example_yaml_value_for(bool, None, stack + ["repeated"])),
            "required": (required := cls._example_yaml_value_for(bool, None, stack + ["required"])),
        }
        if cls.__name__ not in stack:
            result["struct"] = cls._example_yaml_value_for(DocumentMetaModel, None, stack + [cls.__name__])
        else:
            kind = result["type"] = choice(list(TYPE_MAPPING))
            if not required and not repeated:  # default required
                if hasattr(TYPE_MAPPING[kind], "_example_yaml_dict"):
                    result["default"] = TYPE_MAPPING[kind]._example_yaml_dict()  # type: ignore[attr-defined]
                elif examples := YAML_EXAMPLE_VALUES[kind]:
                    result["default"] = choice(examples)
        return result

    def as_model_definition(self, model_name: str = "") -> Any | tuple[str, Any]:
        attribute_default: Any
        attribute_type: Any

        if self.struct:
            attribute_type = self.struct.create_document_class(model_name=model_name)
        else:
            attribute_type = TYPE_MAPPING.get(self.type)  # type: ignore[arg-type]
        if self.repeated:
            attribute_type = list[attribute_type]

        if self.required:
            return attribute_type

        if self.repeated:
            attribute_default = []
        elif self.default:
            attribute_default = self.default
        else:
            attribute_type = attribute_type | None
            attribute_default = None
        return attribute_type, attribute_default

    def as_profile_definition(self, model_name: str = "") -> Any | tuple[str, Any]:
        attribute_type: Any

        if self.struct:
            attribute_type = self.struct.create_profile_class(model_name=model_name)
        else:
            attribute_type = bool

        return attribute_type, True


class DocumentMetaModel(ExampleMixIn, YamlMixIn, RootModel):
    root: dict[str, DocumentMetaModelAttribute]

    def create_document_class(self, model_name: str) -> BaseModel:
        """
        create a pydantic-based document class from this document metamodel
        """
        class_name = model_name.title()
        model_def = {
            key: val.as_model_definition(model_name=f"{class_name}_{key.title()}") for key, val in self.root.items()
        }
        return create_model(class_name, **model_def, __base__=(RenderTemplateMixIn, ExampleMixIn, YamlMixIn, BaseModel))  # type: ignore[arg-type, type-var, return-value]

    def create_profile_class(self, model_name: str) -> BaseModel:
        """
        create a pydantic-based profile class from this document metamodel
        """
        class_name = model_name.title()
        model_def = {
            key: val.as_profile_definition(model_name=f"{class_name}_{key.title()}") for key, val in self.root.items()
        }
        return create_model(class_name, **model_def, __base__=(ProfileMixIn, YamlMixIn, BaseModel))  # type: ignore[arg-type, type-var, return-value]

    @classmethod
    def document_class_from_file(
        cls,
        model_file: Path,
        exit_on_error: bool = True,
    ) -> BaseModel:
        """
        convenience method to directly create a document model from a file
        """
        return cls.from_yaml(
            model_file,
            exit_on_error=exit_on_error,
        ).create_document_class(model_file.stem)


# resolve forward references
DocumentMetaModelAttribute.model_rebuild()
