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

    @classmethod
    def all(cls) -> tuple[OutputFormat, ...]:
        return tuple(cls)
