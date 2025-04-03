# standard library imports
from __future__ import annotations
import sys
from typing import Self

# third party imports
from pydantic import BaseModel
import yaml
from yaml.scanner import ScannerError

# own imports


class Drivers(BaseModel):

    name: bool
    details: bool

    @classmethod
    def template(cls) -> Self:
        """
        Drivers definition to serve as a template/example.
        """
        return cls(
            name=True,
            details=True,
        )


class Conformities(BaseModel):

    identifier: bool
    description: bool
    guidance: bool

    # template / example

    @classmethod
    def template(cls) -> Self:
        """
        Conformities definition to serve as a template/example.
        """
        return cls(
            identifier=True,
            description=True,
            guidance=True,
        )


class Indicators(BaseModel):

    identifier: bool
    title: bool
    description: bool
    conformities: Conformities
    explanation: bool

    # template / example

    @classmethod
    def template(cls) -> Self:
        """
        Indicators definition to serve as a template/example.
        """
        return cls(
            identifier=True,
            title=True,
            description=True,
            conformities=Conformities.template(),
            explanation=True,
        )


class References(BaseModel):

    name: bool
    url: bool
    notes: bool

    # template / example

    @classmethod
    def template(cls) -> Self:
        """
        Indicators definition to serve as a template/example.
        """
        return cls(
            name=True,
            url=True,
            notes=True,
        )


class Profile(BaseModel):

    identifier: bool
    title: bool
    intro: bool
    scope: bool
    triggers: bool
    criteria: bool
    objectives: bool
    risks: bool
    drivers: Drivers
    indicators: Indicators
    references: References

    # template / example

    @classmethod
    def template(cls) -> Self:
        """
        Document definition to serve as a template/example.
        """
        return cls(
            identifier=True,
            title=True,
            intro=True,
            scope=True,
            triggers=True,
            criteria=True,
            objectives=True,
            risks=True,
            drivers=Drivers.template(),
            indicators=Indicators.template(),
            references=References.template(),
        )

    # YAML interface

    @classmethod
    def from_yaml(cls, yaml_src, exit_on_error: bool = True) -> Self:
        """
        create a Norm from its YAML definition
        """
        try:
            return cls.model_validate(yaml.safe_load(yaml_src))
        except ScannerError as err:
            if exit_on_error:
                print(f"error loading document: {err}")
                sys.exit(1)
            else:
                raise ScannerError(str(err)) from None

    def as_yaml(self) -> str:
        """
        the YAML definition of this norm
        """
        return yaml.safe_dump(
            self.model_dump(by_alias=True),
            default_flow_style=False,
            sort_keys=False,
        )
