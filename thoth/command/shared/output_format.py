"""
output formats supported by Thoth
"""

from __future__ import annotations

# standard library imports
from enum import Enum

# third party imports
# own imports


class OutputFormat(Enum):
    HTML = "html"
    DOCX = "docx"
    MD = "md"
    TEXT = "txt"

    @classmethod
    def all(cls) -> tuple[OutputFormat, ...]:
        return tuple(cls)

    def resolve(self) -> OutputFormat:
        if self in (OutputFormat.HTML, OutputFormat.MD):
            return OutputFormat.TEXT
        return self
