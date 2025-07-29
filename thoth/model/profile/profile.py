from __future__ import annotations

# standard library imports
import sys
from typing import Self

# third party imports
import yaml  # type: ignore
from pydantic import BaseModel
from yaml.scanner import ScannerError  # type: ignore

# own imports


class DriversRenderProfile(BaseModel):
    """
    which elements of Drivers to render
    """

    name: bool
    details: bool

    def __bool__(self) -> bool:
        return any(
            (
                self.name,
                self.details,
            )
        )

    # template / example

    @classmethod
    def template(cls) -> Self:
        """
        A template/example.
        """
        return cls.yes_to_all()

    @classmethod
    def yes_to_all(cls) -> Self:
        """
        Select every part of a driver
        """
        return cls(
            name=True,
            details=True,
        )


class ConformitiesRenderProfile(BaseModel):
    """
    which elements of Conformities to render
    """

    identifier: bool
    description: bool
    guidance: bool

    def __bool__(self) -> bool:
        return any(
            (
                self.identifier,
                self.description,
                self.guidance,
            )
        )

    # template / example

    @classmethod
    def template(cls) -> Self:
        """
        A template/example.
        """
        return cls.yes_to_all()

    @classmethod
    def yes_to_all(cls) -> Self:
        """
        Select every part of a conformity
        """
        return cls(
            identifier=True,
            description=True,
            guidance=True,
        )


class IndicatorsRenderProfile(BaseModel):
    """
    which elements of Indicators to render
    """

    identifier: bool
    title: bool
    description: bool
    conformities: ConformitiesRenderProfile
    explanation: bool

    def __bool__(self) -> bool:
        return any(
            (
                self.identifier,
                self.title,
                self.description,
                self.conformities,
                self.explanation,
            )
        )

    # template / example

    @classmethod
    def template(cls) -> Self:
        """
        A template/example.
        """
        return cls.yes_to_all()

    @classmethod
    def yes_to_all(cls) -> Self:
        """
        Select every part of an indicator
        """
        return cls(
            identifier=True,
            title=True,
            description=True,
            conformities=ConformitiesRenderProfile.yes_to_all(),
            explanation=True,
        )


class ReferencesRenderProfile(BaseModel):
    """
    which elements of References to render
    """

    name: bool
    url: bool
    notes: bool

    def __bool__(self) -> bool:
        return any(
            (
                self.name,
                self.url,
                self.notes,
            )
        )

    # template / example

    @classmethod
    def template(cls) -> Self:
        """
        A template/example.
        """
        return cls.yes_to_all()

    @classmethod
    def yes_to_all(cls) -> Self:
        """
        Select every part of a reference
        """
        return cls(
            name=True,
            url=True,
            notes=True,
        )


class NormRenderProfile(BaseModel):
    """
    which elements of a Norm to render
    """

    identifier: bool
    title: bool
    intro: bool
    scope: bool
    triggers: bool
    criteria: bool
    objectives: bool
    risks: bool
    drivers: DriversRenderProfile
    indicators: IndicatorsRenderProfile
    references: ReferencesRenderProfile

    def __bool__(self) -> bool:
        return any(
            (
                self.identifier,
                self.title,
                self.intro,
                self.scope,
                self.triggers,
                self.criteria,
                self.objectives,
                self.risks,
                self.drivers,
                self.indicators,
                self.references,
            )
        )

    # template / example

    @classmethod
    def template(cls) -> Self:
        """
        A template/example.
        """
        return cls.yes_to_all()

    @classmethod
    def yes_to_all(cls) -> Self:
        """
        Selects every part of a norm
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
            drivers=DriversRenderProfile.yes_to_all(),
            indicators=IndicatorsRenderProfile.yes_to_all(),
            references=ReferencesRenderProfile.yes_to_all(),
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
        return yaml.safe_dump(  # type: ignore[no-any-return]
            self.model_dump(by_alias=True),
            default_flow_style=False,
            sort_keys=False,
        )
