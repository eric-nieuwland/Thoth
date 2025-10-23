from __future__ import annotations

# standard library
from pathlib import Path
from random import choice
from typing import Any

# third party
from pydantic import BaseModel, RootModel, create_model, model_validator

# own
from .mixins import ExampleMixIn, YamlMixIn, ProfileMixIn, RenderTemplateMixIn
from .multi_lingual_text import MultiLingualText


TYPES = {
    "bool": bool,
    "int": int,
    "float": float,
    "str": str,
    "multilingual": MultiLingualText,
}

YAML_EXAMPLES = {
    "bool": ("true", "false"),
    "int": ("42", "-1", "1984"),
    "float": ("2.71828183", "3.14159265"),
    "str": ("Lorem ipsum dolor sit amet",),
    "multilingual": None,
}



class DocumentMetaModelAttribute(ExampleMixIn, YamlMixIn, BaseModel):
    default: str | None = None
    description: str | None = None
    repeated: bool = False
    required: bool = False
    struct: DocumentMetaModel | None = None
    type: str | None = None

    @model_validator(mode="after")
    def _require_known_type(self):
        """Ensure 'type' is a known type, if defined."""
        has_type = self.type is not None

        if has_type and self.type not in TYPES:
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
    def _require_type_has_default_or_required(self):
        """Ensure 'struct' has no default value."""
        has_type = self.type is not None
        has_default = self.default is not None
        is_repeated = self.repeated
        is_required = self.required is not None

        if has_type and not is_repeated and not is_required and not has_default:
            raise ValueError('Need default value for not required field.')

        if has_type and not is_repeated and is_required and has_default:
            raise ValueError('Default value for required field is meaningless.')

        return self

    @model_validator(mode="after")
    def _require_either_struct_or_type(self):
        """Ensure exactly one of 'struct' and 'type' is present."""
        has_struct = self.struct is not None
        has_type = self.type is not None

        if not (has_struct or has_type):
            raise ValueError('Need either "struct" or "type".')

        if has_struct and has_type:
            raise ValueError('Need either "struct" or "type", not both.')

        return self

    @classmethod
    def _example_yaml_dict(cls, stack = []) -> dict:
        result = {
            "description": cls._example_yaml_value_for(str, None, stack + ["description"]),
            "repeated": cls._example_yaml_value_for(bool, None, stack + ["repeated"]),
            "required": (required := cls._example_yaml_value_for(bool, None, stack + ["required"])),
        }
        if cls.__name__ not in stack:
            result["struct"] = cls._example_yaml_value_for(DocumentMetaModel, None, stack + [cls.__name__])
        else:
            kind = result["type"] = choice(list(TYPES))
            if (examples := YAML_EXAMPLES[kind]) and not required:
                result["default"] = choice(examples)
        return result

    def as_model_definition(self, model_name: str = "") -> Any | tuple[str, Any]:
        attribute_default: Any
        attribute_type: Any

        if self.struct:
            attribute_type = self.struct.create_document_class(model_name=model_name)
        else:
            attribute_type = TYPES.get(self.type)  # type: ignore[arg-type]
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

    def create_document_class(self, model_name: str) -> Any:
        """
        create a pydantic-based document class from this document metamodel
        """
        class_name = model_name.title()
        model_def = {
            key: val.as_model_definition(model_name=f"{class_name}_{key.title()}")
            for key, val in self.root.items()
        }
        return create_model(class_name, **model_def, __base__=(RenderTemplateMixIn, ExampleMixIn, YamlMixIn, BaseModel))  # type: ignore[arg-type]

    def create_profile_class(self, model_name: str) -> Any:
        """
        create a pydantic-based profile class from this document metamodel
        """
        class_name = model_name.title()
        model_def = {
            key: val.as_profile_definition(model_name=f"{class_name}_{key.title()}")
            for key, val in self.root.items()
        }
        return create_model(class_name, **model_def, __base__=(ProfileMixIn, YamlMixIn, BaseModel))  # type: ignore[arg-type]

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
