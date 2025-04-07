# standard library imports
import sys
from pathlib import Path

# third party imports

# own imports
from ..shared.new_command import new_command
from model.norm.norm import Norm


def new_norm(
    language: str,
    output: Path | None = None,
    force: bool = False,
):
    """
    create a starting point for a norm definition
    """
    new_command(Norm, output, force)
