"""
check_profile - check syntax of a profile
"""

from __future__ import annotations

# standard library imports
from pathlib import Path

# third party imports
import typer

# own imports
from thoth.model.meta_model import DocumentMetaModel
from thoth.command.shared.print_changes import print_changes


def check_profile(
    model: Path = typer.Option(exists=True, readable=True),
    path: Path = typer.Argument(exists=True, readable=True),
) -> None:
    """
    check syntax of a profile

    Prints a message to help you correct any issue found and "OK" if no issues were found.
    """
    document_model = DocumentMetaModel.from_yaml(model, exit_on_error=True)
    profile_model = document_model.create_profile_class(model.stem)  # derive profile model
    copy = profile_model.from_yaml(path).as_yaml_text()
    # here only if path was successfully loaded
    with open(path) as f:
        original = f.read()
    if not print_changes(original, copy):
        print("OK")
