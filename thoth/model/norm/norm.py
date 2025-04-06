# standard library imports
from __future__ import annotations
import sys
from typing import Self

# third party imports
from pydantic import BaseModel
import yaml  # type: ignore
from yaml.scanner import ScannerError  # type: ignore

# own imports
from utils.flatten import flatten
from utils.list_joiner import list_joiner
from .yaml_norm_layout_enhancer import yaml_norm_layout_enhancer
from .driver import Driver
from .indicator import Indicator
from .multi_lingual_text import MultiLingualText
from .reference import Reference
from .utils import count_multi_lingual_helper


class Norm(BaseModel):
    """
    An SSD norm
    """

    identifier: str
    title: MultiLingualText
    intro: MultiLingualText
    scope: MultiLingualText
    triggers: list[MultiLingualText]
    criteria: list[MultiLingualText]
    objectives: list[MultiLingualText]
    risks: list[MultiLingualText]
    drivers: list[Driver] | None = None
    indicators: list[Indicator]
    references: list[Reference] | None = None

    # checks

    def check_identifiers(self) -> list | tuple:
        return flatten(
            [indicator.check_identifiers([nr]) for nr, indicator in enumerate(self.indicators, 1)]
        )

    # multi-lingual

    def count_multi_lingual(self) -> tuple[int, dict[str, int]]:
        """
        count the number of multilingual elements and the languages therein
        """
        return count_multi_lingual_helper(
            (
                self.title,
                self.intro,
                self.scope,
                self.triggers,
                self.criteria,
                self.objectives,
                self.risks,
                self.indicators,
                self.references,
            ),
        )

    # split/merge

    def copy_for_language(self, *languages: str) -> Self:
        """
        A version of this norm, restricted in languages
        """
        return self.__class__(
            identifier=self.identifier,
            title=self.title.copy_for_language(*languages),
            intro=self.intro.copy_for_language(*languages),
            scope=self.scope.copy_for_language(*languages),
            triggers=[trigger.copy_for_language(*languages) for trigger in self.triggers],
            criteria=[criterium.copy_for_language(*languages) for criterium in self.criteria],
            objectives=[objective.copy_for_language(*languages) for objective in self.objectives],
            risks=[risk.copy_for_language(*languages) for risk in self.risks],
            drivers=self.drivers,
            indicators=[indicator.copy_for_language(*languages) for indicator in self.indicators],
            references=(
                [reference.copy_for_language(*languages) for reference in self.references]
                if self.references
                else None
            ),
        )

    def __or__(self, other: Norm) -> Norm:
        return self.join(self, other)

    @classmethod
    def join(cls, norm1: Norm, norm2: Norm) -> Norm:
        if not all(
            (
                norm1.identifier == norm2.identifier,
                len(norm1.triggers) == len(norm2.triggers),
                len(norm1.criteria) == len(norm2.criteria),
                len(norm1.objectives) == len(norm2.objectives),
                len(norm1.risks) == len(norm2.risks),
                norm1.drivers == norm2.drivers,
                len(norm1.indicators) == len(norm2.indicators),
                (
                    (norm1.references is None and norm2.references is None)
                    or (
                        norm1.references is not None
                        and norm2.references is not None
                        and len(norm1.references) == len(norm2.references)
                    )
                ),
            )
        ):
            raise ValueError("not equally structured")

        return cls(
            identifier=norm1.identifier,
            title=norm1.title | norm2.title,
            intro=norm1.intro | norm2.intro,
            scope=norm1.scope | norm2.scope,
            triggers=list_joiner(norm1.triggers, norm2.triggers),  # type: ignore
            criteria=list_joiner(norm1.criteria, norm2.criteria),  # type: ignore
            objectives=list_joiner(norm1.objectives, norm2.objectives),  # type: ignore
            risks=list_joiner(norm1.risks, norm2.risks),  # type: ignore
            drivers=norm1.drivers,
            indicators=list_joiner(norm1.indicators, norm2.indicators),  # type: ignore
            references=(
                list_joiner(norm1.references, norm2.references) if norm1.references else None
            ),
        )

    # template / example

    @classmethod
    def template(cls, language: str) -> Self:
        """
        Norm with random content to serve as a template/example.
        """
        multi_lingual_text = MultiLingualText.template(language)
        return cls(
            identifier="|[ norm identifier ]|",
            title=multi_lingual_text,
            intro=multi_lingual_text,
            scope=multi_lingual_text,
            triggers=[
                multi_lingual_text,
            ],
            criteria=[
                multi_lingual_text,
            ],
            objectives=[
                multi_lingual_text,
            ],
            risks=[
                multi_lingual_text,
            ],
            drivers=[
                Driver.template(language),
            ],
            indicators=[
                Indicator.template(language, "01"),
                Indicator.template(language, "02"),
            ],
            references=[
                Reference.template(language),
            ],
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
                print(f"error loading norm: {err}")
                sys.exit(1)
            else:
                raise ScannerError(str(err)) from None

    def as_yaml(self) -> str:
        """
        the YAML definition of this norm
        """
        return yaml_norm_layout_enhancer(
            yaml.safe_dump(
                self.model_dump(by_alias=True),
                default_flow_style=False,
                sort_keys=False,
            )
        )
