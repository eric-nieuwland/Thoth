# standard library imports
from pathlib import Path

# third party imports

# own imports
from model.norm.norm import Norm
from ..shared.new_command import new_command


def new_norm(
    language: str,
    output: Path | None = None,
    force: bool = False,
):
    """
    create a starting point for a norm definition
    """
    new_command(Norm, output, force)
