# standard library imports
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

    def isolate_language(self, language: str) -> Self:
        """
        A version of this conformity, restricted to a single language
        """
        return self.__class__(
            identifier=self.identifier,
            description=self.description.isolate_language(language),
            guidance = self.guidance.isolate_language(language) if self.guidance else None,
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
    def lorem_ipsum(cls):
        multi_lingual_text = MultiLingualText.lorem_ipsum()
        return cls(
            identifier="identia conformus",
            description=multi_lingual_text,
            guidance=multi_lingual_text,
        )
