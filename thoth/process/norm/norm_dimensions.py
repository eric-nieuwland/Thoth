from __future__ import annotations

# standard library imports
from dataclasses import dataclass
from itertools import zip_longest

from babel.plural import value_node

from model.norm import driver
# third party imports

# own imports
from model.norm.norm import Norm


@dataclass
class NormDimensions:
    languages: list[str]
    triggers: int
    criteria: int
    objectives: int
    risks: int
    drivers: dict[str, list[str]]
    indicators: dict[str, list[str]]
    references: int

    @classmethod
    def from_norm(cls, norm: Norm) -> NormDimensions:
        languages = list(sorted(set(norm.count_multi_lingual()[1])))
        triggers = len(norm.triggers)
        criteria = len(norm.criteria)
        objectives = len(norm.objectives)
        risks = len(norm.risks)
        drivers = {
            driver.name: [detail for detail in driver.details] if driver.details else []
            for driver in (norm.drivers if norm.drivers else [])
        }
        indicators = {
            indicator.identifier: [ conformity.identifier for conformity in indicator.conformities]
            for indicator in norm.indicators
        }
        references = len(norm.references) if norm.references else 0
        return cls(
            languages=languages,
            triggers=triggers,
            criteria=criteria,
            objectives=objectives,
            risks=risks,
            drivers=drivers,
            indicators=indicators,
            references=references,
        )

    def __or__(self, other) -> NormDimensions:
        if not isinstance(other, self.__class__):
            raise TypeError("can only '|' with another %s", self.__class__.__name__)

        languages = list(sorted(set(self.languages) | set(other.languages)))
        triggers = max(self.triggers, other.triggers)
        criteria = max(self.criteria, other.criteria)
        objectives = max(self.objectives, other.objectives)
        risks = max(self.risks, other.risks)
        drivers = {
            key: list(sorted(set(self.drivers.get(key, [])) | set(other.drivers.get(key, []))))
            for key in sorted(set(self.drivers) | set(other.drivers))
        }
        indicators = {
            key: list(sorted(set(self.indicators.get(key, [])) | set(other.indicators.get(key, []))))
            for key in sorted(set(self.indicators) | set(other.indicators))
        }
        references = max(self.references, other.references)

        return self.__class__(
            languages=languages,
            triggers=triggers,
            criteria=criteria,
            objectives=objectives,
            risks=risks,
            drivers=drivers,
            indicators=indicators,
            references=references,
        )

    def __sub__(self, other) -> NormDimensions:
        if not isinstance(other, self.__class__):
            raise TypeError("can only '-' with another %s", self.__class__.__name__)

        languages = list(sorted(set(self.languages) - set(other.languages)))
        triggers = max(self.triggers - other.triggers, 0)
        criteria = max(self.criteria - other.criteria, 0)
        objectives = max(self.objectives - other.objectives, 0)
        risks = max(self.risks - other.risks, 0)
        drivers = {
            key: list(sorted(values))
            for key in sorted(self.drivers)
            if len(values := set(self.drivers.get(key, [])) - set(other.drivers.get(key, []))) > 0
        }
        indicators = {
            key: list(sorted(values))
            for key in sorted(self.indicators)
            if len(values := set(self.indicators.get(key, [])) - set(other.indicators.get(key, []))) > 0
        }
        references = max(self.references - other.references, 0)

        return self.__class__(
            languages=languages,
            triggers=triggers,
            criteria=criteria,
            objectives=objectives,
            risks=risks,
            drivers=drivers,
            indicators=indicators,
            references=references,
        )

