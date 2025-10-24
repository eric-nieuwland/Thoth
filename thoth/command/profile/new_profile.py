"""
new_profile - create a new profile
"""

from __future__ import annotations

# standard library imports
from pathlib import Path

# third party imports
import typer

# own imports
from thoth.command.shared.write_output import write_output
from thoth.model.meta_model import DocumentMetaModel


def new_profile(
    model: Path = typer.Option(exists=True, readable=True),
    output: Path | None = None,
    force: bool = False,
) -> None:
    """
    create a starting point for a profile
    """
    document_model = DocumentMetaModel.from_yaml(model, exit_on_error=True)
    profile_model = document_model.create_profile_class(model.stem)  # derive profile class
    profile = profile_model.yes_to_all()  # type: ignore[attr-defined] # create profile with all elements enabled
    write_output(profile.as_yaml_text(), destination=output, force=force)
