# standard library imports

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
