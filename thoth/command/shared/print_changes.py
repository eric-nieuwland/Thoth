"""
suggest_changes_to_original - compare an original and suggested version of a text
"""

from __future__ import annotations

# standard library imports
import re
from difflib import unified_diff
from collections.abc import Iterable, Generator

# third party imports

# own imports


class DiffBlock:
    context: int = 2
    line_nr: int
    text: list[tuple[str, str]]
    last_change: int | None

    def __init__(self, line_nr: int):
        self.line_nr = line_nr
        self.text = []
        self.last_change = None

    def add_line(self, line: str):
        first, line = line[0], line[1:]
        if first not in (" ", "-", "+"):
            raise ValueError(f"Line not recognized - first character is '{first}'")
        stripped = line.strip()
        if first == "-" and (stripped == "" or stripped[0] == "#"):
            first = " "
        if first != " ":
            self.last_change = len(self.text)
        self.text.append((first, line))
        if self.last_change is None and len(self.text) > self.context:
            self.line_nr += len(self.text) - self.context
            self.text = self.text[-self.context:]

    def __iter__(self) -> Generator[str, None, None]:
        if self.last_change is None:
            return
        last_line = min(len(self.text), self.last_change + self.context + 1)
        text = self.text[:last_line]
        line_nr = self.line_nr
        if line_nr > 1:
            yield "  ..."
        for first, line in text:
            if first == "-" and line.strip() == "":
                first = " "
            if first == "+":  #
                lnr = " " * 3
            else:
                lnr = f"{line_nr:3d}"
                line_nr += 1
            yield f"{first} {lnr} {line}"


def human_centric_diff(original: str | list[str], changed: str | list[str]) -> Iterable[str]:
    """
    compare an original and changed version of a text
    present the changes in a user-friendly way
    """
    if isinstance(original, str):
        original = original.splitlines()
    if isinstance(changed, str):
        changed = changed.splitlines()

    diff_block: DiffBlock | None = None
    for line in unified_diff(original, changed, lineterm=""):
        if line in ("--- ", "+++ "):
            continue
        if found := re.match(r"@@ -(?P<first>\d+).* @@", line):
            line_nr = int(found["first"])
            if diff_block:
                yield from diff_block
            diff_block = DiffBlock(line_nr)
            continue
        diff_block.add_line(line)
    if diff_block:
        yield from diff_block


def print_changes(original: str | list[str], changed: str | list[str]) -> bool:
    """
    compare an original and changed version of a text
    If they differ, print the changes in a user-friendly way.
    Return True if changes were found, False if they were not.
    """
    changes = False

    for line in human_centric_diff(original, changed):
        changes = True
        print(line)

    return changes
