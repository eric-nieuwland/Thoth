# standard library imports

# third party imports
from pydantic import BaseModel

# own imports
from .multi_lingual_text import MultiLingualText
from .utils import count_multi_lingual_helper


class Conformity(BaseModel):

    identifier: str
    description: MultiLingualText
    guidance: MultiLingualText | None = None

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
