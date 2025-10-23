"""
json_mixin - mix-in for Pydantic classes to add the ability to instantiate a model from JSON
"""

from __future__ import annotations

# standard library
from pathlib import Path
from typing import Self
import sys

# third party
from pydantic import ValidationError

# own


EXPECTED = {
    "bool_parsing": "true or false",
    "bool_type": "true or false",
    "float_parsing": "floating point number",
    "int_from_float": "integer number - this looks like a floating point number",
    "int_parsing": "integer number",
    "list_type": "list expected",
    "model_type": "attribute definition",
    "string_type": "string value",
    "value_error": None,
}


def _make_error_key(parts):
    """
    make error key
    int parts are list indexes, Python starts at 0 (zero), humans count from 1 (one)
    """
    return ".".join(f"{part + 1}" if isinstance(part, int) else str(part) for part in parts)


def print_pydantic_validation_errors(error: ValidationError):
    """
    a more user-friendly version of pydantic validation errors
    """
    num_errors = error.error_count()
    if num_errors < 1:
        return

    key_errors = {
        _make_error_key(err["loc"][:-1]): err
        for err in error.errors()
        if err["loc"][-1] == "[key]"
    }
    value_errors = {
        key: err
        for err in error.errors()
        if err["loc"][-1] != "[key]"
           and (key := _make_error_key(err["loc"])) not in key_errors
    }

    s = "" if len(key_errors) + len(value_errors) < 2 else "S"
    print(f"""=== ERROR{s} ===""")

    for key, _ in key_errors.items():
        print(f"""key {key}:""")
        print("""  invalid name""")

    if key_errors and value_errors:
        print()

    for key, err in value_errors.items():
        expected = EXPECTED.get(err["type"], f"""{err["type"]} - {err["msg"]}""")
        actual = f"""{err["input"]}"""
        print(f"""value {key}:""")
        if expected is None:
            fmt, *args = err["ctx"]["error"].args
            print(f"""  error: {fmt % tuple(args)}""")
        else:
            print(f"""  expected: {expected}""")
            print(f"""  actual:   {actual!r}""")


class JsonMixIn:
    """
    mix-in for Pydantic classes to add the ability to instantiate a model from JSON
    """

    @classmethod
    def from_json_definition(
        cls,
        json_definition,
        exit_on_error: bool = True,
    ) -> Self:
        """
        create instance from a JSON definition
        """
        try:
            return cls.model_validate(json_definition)  # type: ignore[attr-defined]
        except ValidationError as err:
            if exit_on_error:
                print_pydantic_validation_errors(err)
                sys.exit(1)
            else:
                raise err from None

    def as_json_definition(self) -> str:
        """
        the JSON definition of this instance
        """
        return self.model_dump(by_alias=True)

    @classmethod
    def from_json(
        cls,
        json_file: Path,
        exit_on_error: bool = True,
    ) -> Self:
        """
        create instance from a JSON definition file
        """
        with open(json_file) as f:
            return cls.from_json_definition(f, exit_on_error=exit_on_error)
