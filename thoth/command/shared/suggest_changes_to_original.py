"""
suggest_changes_to_original - compare an original and suggested version of a text
"""

from __future__ import annotations

# standard library imports
from difflib import unified_diff
import re

# third party imports

# own imports


def suggest_changes_to_original(original: str | list[str], suggested: str | list[str]) -> bool:
    """
    compare an original and suggested version of a text
    If they differ, present the suggested changes in a user-friendly way.
    Return True if changes were suggested, False if they were not.
    """
    if isinstance(original, str):
        original = original.splitlines()
    if isinstance(suggested, str):
        suggested = suggested.splitlines()
    changes = False
    line_nr = 0  # keep IDE and QA tools happy
    for line in unified_diff(original, suggested, lineterm=""):
        changes = True
        if line in ("--- ", "+++ "):
            continue
        if found := re.match(r"@@ -(?P<first>\d+),.* @@", line):
            line_nr = int(found["first"])
            if line_nr > 1:
                print("  ...")
            continue
        first = line[0]
        line = line[1:]
        print(f"{first} {line_nr:3d} {line}")
        line_nr += 1
    return changes
