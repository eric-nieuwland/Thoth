# standard library imports
from __future__ import annotations
from typing import Self

# third party imports
from pydantic import BaseModel

# own imports
from .multi_lingual_text import MultiLingualText
from .utils import count_multi_lingual_helper


class Conformity(BaseModel):

    identifier: str
    description: MultiLingualText
    guidance: MultiLingualText | None = None

    # checks

    def check_identifiers(self, nrs: [int]) -> list:
        return [
            f"conformity #{nrs[-1]} in indicator #{nrs[-2]} has identifier '{self.identifier}'"
            if f"{nrs[-1]:0{len(self.identifier)}d}" != self.identifier else
            [],
        ]

    # split/merge

    def copy_for_language(self, *languages: str) -> Self:
        """
        A version of this conformity, restricted to a single language
        """
        return self.__class__(
            identifier=self.identifier,
            description=self.description.copy_for_language(*languages),
            guidance = self.guidance.copy_for_language(*languages) if self.guidance else None,
        )

    def __or__(self, other: Self) -> Self:
        return self.join(self, other)

    @classmethod
    def join(cls, conformity1: Conformity, conformity2: Conformity) -> Conformity:
        if not all(
            (
                    conformity1.identifier == conformity2.identifier,
                    (conformity1.guidance is None) == (conformity2.guidance is None),
            )
        ):
            raise ValueError("not equally structured")

        return cls(
            identifier=conformity1.identifier,
            description=conformity1.description | conformity2.description,
            guidance=conformity1.guidance | conformity2.guidance if conformity1.guidance else None,
        )

    # multi-lingual

    def count_multi_lingual(self) -> tuple[int, dict[str, int]]:
        """
        count the number of multilingual elements and the languages therein
        """
        return count_multi_lingual_helper(
            (
                self.description,
                self.guidance,
            ),
        )

    # template / example

    @classmethod
    def template(cls, language: str, identifier: str):
        multi_lingual_text = MultiLingualText.template(language)
        return cls(
            identifier=identifier,
            description=multi_lingual_text,
            guidance=multi_lingual_text,
        )
