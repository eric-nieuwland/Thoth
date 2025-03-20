# standard library imports
from typing import Self

# third party imports
from pydantic import BaseModel

# own imports
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

    def isolate_language(self, language: str) -> Self:
        """
        A version of this reference, restricted to a single language
        """
        return self.__class__(
            name=self.name,
            url=self.url,
            notes=[note.isolate_language(language) for note in self.notes] if self.notes else None
        )

    # template / example

    @classmethod
    def lorem_ipsum(cls):
        return cls(
            name="referentia namum",
            url="http://loremipsum.io",
            notes=[
                MultiLingualText.lorem_ipsum(),
            ]
        )
