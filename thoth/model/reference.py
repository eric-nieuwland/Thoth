# standard library imports

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
