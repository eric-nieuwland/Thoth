# standard library imports
from pathlib import Path

# third party imports

# own imports
from model.norm.norm import Norm
from ..shared.reformat_command import reformat_command


def reformat_norm(path: Path, output: Path | None = None, force: bool = False):
    """
    reformat a norm
    """
    reformat_command(Norm, path, output, force)
