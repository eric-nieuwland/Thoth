# standard library imports
from __future__ import annotations
from typing import Self

# third party imports
from pydantic import BaseModel
import yaml

# own imports
from utils.flatten import flatten
from utils.list_joiner import list_joiner
from utils.yaml_norm_beautifier import yaml_norm_beautifier
from .driver import Driver
from .indicator import Indicator
from .multi_lingual_text import MultiLingualText
from .reference import Reference
from .utils import count_multi_lingual_helper


class Norm(BaseModel):

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

    def check_identifiers(self) -> list:
        return flatten([indicator.check_identifiers([nr]) for nr, indicator in enumerate(self.indicators, 1)])

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

    def isolate_language(self, language: str) -> Self:
        """
        A version of this norm, restricted to a single language
        """
        return self.__class__(
            identifier=self.identifier,
            title=self.title.isolate_language(language),
            intro=self.intro.isolate_language(language),
            scope=self.scope.isolate_language(language),
            triggers=[trigger.isolate_language(language) for trigger in self.triggers],
            criteria=[criterium.isolate_language(language) for criterium in self.criteria],
            objectives=[objective.isolate_language(language) for objective in self.objectives],
            risks=[risk.isolate_language(language) for risk in self.risks],
            drivers=self.drivers,
            indicators=[indicator.isolate_language(language) for indicator in self.indicators],
            references=[reference.isolate_language(language) for reference in self.references] if self.references else None,
        )

    def __or__(self, other: Self) -> Self:
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
                    (norm1.references is None and norm2.references is None) or
                    len(norm1.references) == len(norm2.references)
                ),
            )
        ):
            raise ValueError("not equally structured")

        return cls(
            identifier=norm1.identifier,
            title=norm1.title | norm2.title,
            intro=norm1.intro | norm2.intro,
            scope=norm1.scope | norm2.scope,
            triggers=list_joiner(norm1.triggers, norm2.triggers),
            criteria=list_joiner(norm1.criteria, norm2.criteria),
            objectives=list_joiner(norm1.objectives, norm2.objectives),
            risks=list_joiner(norm1.risks, norm2.risks),
            drivers=norm1.drivers,
            indicators=list_joiner(norm1.indicators, norm2.indicators),
            references=list_joiner(norm1.references, norm2.references) if norm1.references else None,
        )

    # template / example

    @classmethod
    def lorem_ipsum(cls) -> Self:
        """
        Norm with random content to serve as a template/example.
        """
        multi_lingual_text = MultiLingualText.lorem_ipsum()
        return cls(
            identifier="identifioram normii",
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
                Driver.lorem_ipsum(),
            ],
            indicators=[
                Indicator.lorem_ipsum(),
                Indicator.lorem_ipsum(),
            ],
            references=[
                Reference.lorem_ipsum(),
            ],
        )

    # YAML interface

    @classmethod
    def from_yaml(cls, yaml_src) -> Self:
        """
        create a Norm from its YAML definition
        """
        return cls.model_validate(yaml.safe_load(yaml_src))

    def as_yaml(self) -> str:
        """
        the YAML definition of this norm
        """
        return yaml_norm_beautifier(
            yaml.safe_dump(
                self.model_dump(by_alias=True),
                default_flow_style=False,
                sort_keys=False,
            )
        )
