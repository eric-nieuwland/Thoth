# standard library imports
from typing import Self

# third party imports
from pydantic import BaseModel

# own imports


class Driver(BaseModel):

    name: str
    details: list[str] | None = None

    # template / example

    @classmethod
    def lorem_ipsum(cls):
        return cls(
            name="driverius namum",
            details=[
                "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
            ]
        )
