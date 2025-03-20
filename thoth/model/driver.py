# standard library imports

# third party imports
from pydantic import BaseModel


class Driver(BaseModel):

    name: str
    details: list[str] | None = None

    @classmethod
    def lorem_ipsum(cls):
        return cls(
            name="driverius namum",
            details=[
                "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
            ]
        )
