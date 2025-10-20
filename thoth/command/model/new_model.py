"""
new_model - create a new document model
"""

from __future__ import annotations

# standard library imports
from pathlib import Path

# third party imports

# own imports
from thoth.model.meta_model import DocumentMetaModel
from thoth.command.shared.write_output import write_output


def new_model(
    output: Path | None = None,
    force: bool = False,
) -> None:
    """
    create a starting point for a document model
    """
    write_output(
        DocumentMetaModel.example().as_yaml_text(),
        destination=output,
        force=force,
    )
