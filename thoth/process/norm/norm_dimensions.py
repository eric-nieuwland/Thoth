from __future__ import annotations

# standard library imports
from dataclasses import dataclass
from itertools import zip_longest

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
    drivers: list[int]
    indicators: list[int]
    references: int

    @classmethod
    def from_norm(cls, norm: Norm) -> NormDimensions:
        languages = list(sorted(set(norm.count_multi_lingual()[1])))
        triggers = len(norm.triggers)
        criteria = len(norm.criteria)
        objectives = len(norm.objectives)
        risks = len(norm.risks)
        drivers = [
            len(driver.details) if driver and driver.details else 0
            for driver in (norm.drivers if norm.drivers else [])
        ]
        indicators = [
            len(indicator.conformities) if indicator else 0
            for indicator in norm.indicators
        ]
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
        drivers = [
            max(nr_details_1, nr_details_2)
            for nr_details_1, nr_details_2 in zip_longest(self.drivers, other.drivers, fillvalue=0)
        ]
        indicators = [
            max(nr_conf_1, nr_conf_2)
            for nr_conf_1, nr_conf_2 in zip_longest(self.indicators, other.indicators, fillvalue=0)
        ]
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
