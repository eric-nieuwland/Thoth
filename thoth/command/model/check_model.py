"""
check_model - check syntax of a document model
"""

from __future__ import annotations

# standard library imports
from pathlib import Path

# third party imports
import typer

# own imports
from thoth.model.meta_model import DocumentMetaModel
from thoth.command.shared.print_changes import print_changes


def check_model(
    path: Path = typer.Argument(exists=True, readable=True),
) -> None:
    """
    check syntax of a document model

    Prints a message to help you correct any issue found and "OK" if no issues were found.
    """
    copy = DocumentMetaModel.from_yaml(path).as_yaml_text()
    # here only if path was successfully loaded
    with (open(path) as f):
        original = f.read()
    if not print_changes(original, copy):
        print("OK")
