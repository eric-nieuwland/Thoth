# standard library imports
import sys
from pathlib import Path

# third party imports

# own imports
from ..shared.new_command import new_command
from model.profile.profile import NormRenderProfile


def new_profile(
    output: Path | None = None,
    force: bool = False,
):
    """
    create a starting point for a document profile
    """
    new_command(NormRenderProfile, output, force)
