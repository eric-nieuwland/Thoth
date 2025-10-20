# standard library imports
from pathlib import Path
import sys

# third party imports
# own imports
from thoth.model.meta_model import DocumentMetaModel
from thoth.command.shared.write_output import write_output


def new_model(
    output: Path | None = None,
    force: bool = False,
) -> None:
    """
    create a starting point for a norm definition
    """
    write_output(
        DocumentMetaModel.example().as_yaml_definition(),
        destination=output,
        force=force,
    )
