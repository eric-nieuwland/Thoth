"""
example_mixin - mix-in for Pydantic classes to add the ability to create examples of instances in YAML format
"""

from __future__ import annotations

# standard library
from types import UnionType
from typing import Any, Self, get_args, get_origin

# third party
from pydantic import BaseModel, RootModel

# own


EXAMPLES = {
    bool: True,
    int: 42,
    float: 3.14,
    str: "Lorem ipsum dolor sit amet",
}


class ExampleMixIn:
    """
    mix-in for Pydantic classes to add the ability to create examples of instances in YAML format
    """

    @staticmethod
    def field_type_base_and_default(field) -> tuple[Any, Any, Any]:
        if (origin := get_origin(field.annotation)) is not None:
            return origin, get_args(field.annotation), field.default
        return field.annotation, None, field.default

    @classmethod
    def _example_yaml_value_for(cls, kind, base, stack) -> Any:
        if kind in EXAMPLES:
            return EXAMPLES[kind]
        elif hasattr(kind, "_example_yaml_dict"):
            return kind._example_yaml_dict(stack)
        elif kind is UnionType:
            for sub_base in base:
                try:
                    return cls._example_yaml_value_for(sub_base, None, stack)
                except ValueError:
                    pass
            if type(None) in base:
                return None
        elif kind is list and base is not None:
            example = cls._example_yaml_value_for(base[0], None, stack)
            return [
                example,
                example,
            ]
        raise ValueError("no example for %s %s", kind, base)

    @classmethod
    def _as_example_yaml_dict_root_model(cls, stack = []) -> dict:
        root = cls.model_fields["root"]
        kind, base, _ = cls.field_type_base_and_default(root)
        if kind is dict and base is not None:
            key_type, val_type = base
            if key_type is str and hasattr(val_type, "_example_yaml_dict"):
                return {
                    key: val_type._example_yaml_dict(stack) for key in ("foo", "bar")
                }
        raise ValueError("cannot make an example dict for %s", cls.__name__)

    @classmethod
    def _as_example_yaml_dict_base_model(cls, stack = []) -> dict:
        result = {}
        for field_name, field_def in cls.model_fields.items():
            if field_name in stack:
                continue
            kind, base, _ = cls.field_type_base_and_default(field_def)
            result[field_name] = cls._example_yaml_value_for(kind, base, stack + [field_name])
        return result

    @classmethod
    def _example_yaml_dict(cls, stack = []) -> dict:
        if issubclass(cls, RootModel):
            return cls._as_example_yaml_dict_root_model(stack)
        if issubclass(cls, BaseModel):
            return cls._as_example_yaml_dict_base_model(stack)
        raise TypeError(f"cannot create an example dict for {cls.__name__}")

    @classmethod
    def example(cls) -> Self:
        arg = cls._example_yaml_dict()
        instance = cls.model_validate(arg)
        return instance
