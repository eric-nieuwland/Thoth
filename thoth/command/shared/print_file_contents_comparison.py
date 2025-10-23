"""
check_with_file_contents - check file contents with text
"""

from __future__ import annotations

# standard library imports
from pathlib import Path

# third party imports

# own imports
from thoth.command.shared.print_changes import print_changes


def print_file_contents_comparison(path: Path, current: str | list[str]) -> None:
    """
    print the comparison of the actual content of a file
    and a possibly changed version of its content

    If they differ, print the changes in a user-friendly way.
    If they do not differ, print "OK".
    """
    with open(path) as f:
        original = f.read()
    if not print_changes(original, current):
        print("OK")
