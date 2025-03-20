# standard library imports
from typing import Self

# third party imports
from pydantic import BaseModel

# own imports
from .conformity import Conformity
from .multi_lingual_text import MultiLingualText
from .utils import count_multi_lingual_helper


class Indicator(BaseModel):

    identifier: str
    title: MultiLingualText
    description: MultiLingualText
    conformities: list[Conformity]
    explanation: MultiLingualText

    # checks

    def check_identifiers(self, nrs: list[int]) -> list:
        return [
            f"indicator #{nrs[-1]} has identifier '{self.identifier}'"
            if f"{nrs[-1]:0{len(self.identifier)}d}" != self.identifier else
            [],
            [conformity.check_identifiers(nrs + [nr]) for nr, conformity in enumerate(self.conformities, 1)],
        ]

    # multi-lingual

    def count_multi_lingual(self) -> tuple[int, dict[str, int]]:
        """
        count the number of multilingual elements and the languages therein
        """
        return count_multi_lingual_helper(
            (
                self.title,
                self.description,
                self.conformities,
                self.explanation,
            ),
        )

    # split/merge

    def isolate_language(self, language: str) -> Self:
        """
        A version of this indicator, restricted to a single language
        """
        return self.__class__(
            identifier=self.identifier,
            title=self.title.isolate_language(language),
            description=self.description.isolate_language(language),
            conformities=[conformity.isolate_language(language) for conformity in self.conformities],
            explanation = self.explanation.isolate_language(language),
        )

    # template / example

    @classmethod
    def lorem_ipsum(cls):
        multi_lingual_text = MultiLingualText.lorem_ipsum()
        conformity = Conformity.lorem_ipsum()
        return cls(
            identifier="identificatio indicatros",
            title=multi_lingual_text,
            description=multi_lingual_text,
            conformities=[
                conformity,
                conformity,
            ],
            explanation=multi_lingual_text,
        )
