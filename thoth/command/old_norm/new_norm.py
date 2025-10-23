# standard library imports
from pathlib import Path

# third party imports
# own imports
from thoth.model.norm.norm import Norm

from ..shared.new_command import new_command


def new_norm(
    language: str,
    output: Path | None = None,
    force: bool = False,
) -> None:
    """
    create a starting point for a norm definition
    """
    new_command(Norm, output, force, language=language)
