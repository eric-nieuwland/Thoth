"""
new_model - create a new document model
"""

from __future__ import annotations

# standard library imports

# third party imports

# own imports
from thoth.command.shared.arguments_and_options_info import (
    OUTPUT_PATH_OPTION,
)
from thoth.command.shared.write_output import write_output
from thoth.model.meta_model import DocumentMetaModel


def new_model(
    output: OUTPUT_PATH_OPTION = None,
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
