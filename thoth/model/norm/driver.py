# standard library imports
from typing import Self

# third party imports
from pydantic import BaseModel

# own imports
from ._translation import template_driver_text


class Driver(BaseModel):
    """
    An SSD norm driver
    """

    name: str
    details: list[str] | None = None

    # template / example

    @classmethod
    def template(cls, language: str):
        name, detail = template_driver_text(language)
        return cls(
            name=name,
            details=[
                detail.format(nr=1),
                detail.format(nr=2),
            ],
        )
