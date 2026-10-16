"""
output formats supported by Thoth
"""

from __future__ import annotations

# standard library imports
from enum import Enum
from pathlib import Path

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

    @classmethod
    def from_path(cls, path: Path | None) -> OutputFormat | None:
        if path is None:
            return None
        try:
            return cls(path.suffix[1:])
        except ValueError:
            return None

    def resolve(self) -> OutputFormat:
        if self in (OutputFormat.HTML, OutputFormat.MD):
            return OutputFormat.TEXT
        return self
