# standard library imports
import sys
from pathlib import Path

# third party imports

# own imports
from ..shared.reformat_command import reformat_command
from model.profile.profile import NormRenderProfile


def reformat_profile(path: Path, output: Path | None = None, force: bool = False):
    """
    reformat a document profile
    """
    reformat_command(NormRenderProfile, path, output, force)
