# standard library imports
import sys
from pathlib import Path

# third party imports

# own imports
from .write_output import write_output


def new_command(
    klass,
    destination: Path | None = None,
    force: bool = False,
    **kwargs,
) -> None:
    """
    create a starting point for a document
    """
    write_output(klass.template(**kwargs).as_yaml(), destination=destination, force=force)
