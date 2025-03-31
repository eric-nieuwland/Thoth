# standard library imports
from __future__ import annotations
from typing import Self

# third party imports
from pydantic import BaseModel

# own imports
from utils.list_joiner import list_joiner
from ._translation import template_reference_text
from .multi_lingual_text import MultiLingualText
from .utils import count_multi_lingual_helper


class Reference(BaseModel):

    name: str
    url: str | None = None
    notes: list[MultiLingualText] | None = None

    # multi-lingual

    def count_multi_lingual(self) -> tuple[int, dict[str, int]]:
        """
        count the number of multilingual elements and the languages therein
        """
        return count_multi_lingual_helper(
            (
                self.notes,
            ),
        )

    # split/merge

    def copy_for_language(self, language: str) -> Self:
        """
        A version of this reference, restricted to a single language
        """
        return self.__class__(
            name=self.name,
            url=self.url,
            notes=[note.copy_for_language(language) for note in self.notes] if self.notes else None
        )

    def __or__(self, other: Self) -> Self:
        return self.join(self, other)

    @classmethod
    def join(cls, reference1: Reference, reference2: Reference) -> Reference:
        if not all(
            (
                reference1.name == reference2.name,
                reference1.url == reference2.url,
                (
                    (reference1.notes is None and reference2.notes is None) or
                    len(reference1.notes) == len(reference2.notes)
                ),
            )
        ):
            raise ValueError("not equally structured")

        return cls(
            name=reference1.name,
            url=reference1.url,
            notes=list_joiner(reference1.notes, reference2.notes),
        )

    # template / example

    @classmethod
    def template(cls, language: str):
        return cls(
            name=template_reference_text(language),
            url="https://optional.url",
            notes=[
                MultiLingualText.template(language),
            ]
        )
