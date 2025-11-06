"""
suggest_changes_to_original - compare an original and suggested version of a text
"""

from __future__ import annotations

# standard library imports
import re
from difflib import unified_diff
from collections.abc import Iterable

# third party imports

# own imports


def human_centric_diff(original: str | list[str], changed: str | list[str]) -> Iterable[str]:
    """
    compare an original and changed version of a text
    present the changes in a user-friendly way
    """
    if isinstance(original, str):
        original = original.splitlines()
    if isinstance(changed, str):
        changed = changed.splitlines()

    line_nr = 0  # keep IDE and QA tools happy
    for line in unified_diff(original, changed, lineterm=""):
        if line in ("--- ", "+++ "):
            continue
        if found := re.match(r"@@ -(?P<first>\d+).* @@", line):
            line_nr = int(found["first"])
            if line_nr > 1:
                yield "  ..."
            continue
        first = line[0]
        line = line[1:]
        if first == "+":  #
            lnr = " " * 3
        else:
            lnr = f"{line_nr:3d}"
            line_nr += 1
        yield f"{first} {lnr} {line}"


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
