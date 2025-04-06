# standard library imports
from __future__ import annotations
from typing import Self

# third party imports
from pydantic import BaseModel

# own imports
from utils.list_joiner import list_joiner
from .conformity import Conformity
from .multi_lingual_text import MultiLingualText
from .utils import count_multi_lingual_helper


class Indicator(BaseModel):
    """
    An SSD norm indicator
    """

    identifier: str
    title: MultiLingualText
    description: MultiLingualText
    conformities: list[Conformity]
    explanation: MultiLingualText

    # checks

    def check_identifiers(self, nrs: list[int]) -> list:
        return [
            f"indicator #{nrs[-1]} has identifier '{self.identifier}'"
            if f"{nrs[-1]:0{len(self.identifier)}d}" != self.identifier
            else [],
            [
                conformity.check_identifiers(nrs + [nr])
                for nr, conformity in enumerate(self.conformities, 1)
            ],
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

    def copy_for_language(self, *languages: str) -> Self:
        """
        A version of this indicator, restricted in languages
        """
        return self.__class__(
            identifier=self.identifier,
            title=self.title.copy_for_language(*languages),
            description=self.description.copy_for_language(*languages),
            conformities=[
                conformity.copy_for_language(*languages) for conformity in self.conformities
            ],
            explanation=self.explanation.copy_for_language(*languages),
        )

    def __or__(self, other: Indicator) -> Indicator:
        return self.join(self, other)

    @classmethod
    def join(cls, indicator1: Indicator, indicator2: Indicator) -> Indicator:
        if not all(
            (
                indicator1.identifier == indicator2.identifier,
                len(indicator1.conformities) == len(indicator2.conformities),
            )
        ):
            raise ValueError("not equally structured")

        return cls(
            identifier=indicator1.identifier,
            title=indicator1.title | indicator2.title,
            description=indicator1.description | indicator2.description,
            conformities=list_joiner(indicator1.conformities, indicator2.conformities),  # type: ignore
            explanation=indicator1.explanation | indicator2.explanation,
        )

    # template / example

    @classmethod
    def template(cls, language: str, identifier: str):
        multi_lingual_text = MultiLingualText.template(language)
        return cls(
            identifier=identifier,
            title=multi_lingual_text,
            description=multi_lingual_text,
            conformities=[
                Conformity.template(language, "01"),
                Conformity.template(language, "02"),
            ],
            explanation=multi_lingual_text,
        )
