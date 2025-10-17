"""
yaml_mixin - mix-in for Pydantic classes to add the ability to instantiate a model from YAML
"""

from __future__ import annotations

# standard library
from pathlib import Path
from typing import Self
import sys

# third party
from yaml.scanner import ScannerError
import yaml

# own
from .json_mixin import JsonMixIn


def print_yaml_errors(error: ScannerError):
    """
    a more user-friendly version of YAML scanner errors
    """
    print("=== ERROR ===")
    print(error)


class YamlMixIn(JsonMixIn):
    """
    mix-in for Pydantic classes to add the ability to instantiate a model from YAML
    uses JSON as an intermediary format
    """

    @classmethod
    def from_yaml_definition(
        cls,
        yaml_definition,
        exit_on_error: bool = True,
    ) -> Self:
        """
        create instance from a YAML definition
        """
        try:
            return cls.from_json_definition(
                yaml.safe_load(yaml_definition),
                exit_on_error=exit_on_error,
            )
        except ScannerError as err:
            if exit_on_error:
                print_yaml_errors(err)
                sys.exit(1)
            else:
                raise err from None

    @classmethod
    def _remove_nones(cls, data: dict) -> dict:
        result = {}
        for key, value in data.items():
            if value is None:
                continue
            result[key] = cls._remove_nones(value) if isinstance(value, dict) else value
        return result

    def as_yaml_definition(self) -> str:
        """
        the YAML definition of this instance
        """
        return yaml.safe_dump(
            self._remove_nones(self.as_json_definition()),
            default_flow_style=False,
            sort_keys=False,
        )

    @classmethod
    def from_yaml(
        cls,
        yaml_file: Path,
        exit_on_error: bool = True,
    ) -> Self:
        """
        create instance from a YAML definition file
        """
        with open(yaml_file) as f:
            return cls.from_yaml_definition(f, exit_on_error=exit_on_error)
