"""
copy templates from internal to external location
"""

from __future__ import annotations

# standard library imports
from filecmp import dircmp
from pathlib import Path
from shutil import copytree
from typing import Generator

import sys

# third party imports
# own imports


def _shared_files_helper(dcmp: dircmp) -> Generator[Path, None, None]:
    yield from map(lambda f: Path(dcmp.right) / f, dcmp.common_files)
    for sub_dcmp in dcmp.subdirs.values():
        yield from _shared_files_helper(sub_dcmp)


def shared_files(left: Path, right: Path) -> Generator[Path, None, None]:
    if not left.is_dir() or not right.is_dir():
        return
    yield from map(
        lambda f: f.relative_to(right) if f.is_relative_to(right) else f,
        _shared_files_helper(dircmp(left, right)),
    )


def copy_templates(src: Path, dst: Path, formats: list[str], force: bool = False) -> None:
    """
    copy templates from internal to external location
    be careful not to overwrite existing files by accident
    """

    if dst.is_file():
        print(f"file exists: {dst}")
        sys.exit(1)
    elif dst.is_dir() and not force:
        endangered = [Path(fmt) / file for fmt in formats for file in shared_files(src / fmt, dst / fmt)]
        if len(endangered) > 0:
            print("would overwrite:", file=sys.stderr)
            for file in sorted(endangered):
                print(f" - {file}", file=sys.stderr)
            sys.exit(1)

    for fmt in formats:
        copytree(src / fmt, dst / fmt, dirs_exist_ok=True)
