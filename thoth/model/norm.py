# standard library imports
from typing import Self

# third party imports
from pydantic import BaseModel
import yaml

# own imports
from utils.flatten import flatten
from utils.yaml_norm_beautifier import yaml_norm_beautifier
from .driver import Driver
from .indicator import Indicator
from .meta import Meta
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
