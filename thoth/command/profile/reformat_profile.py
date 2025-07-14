# standard library imports
from pathlib import Path

# third party imports
# own imports
from thoth.model.profile.profile import NormRenderProfile

from ..shared.reformat_command import reformat_command


def reformat_profile(path: Path, output: Path | None = None, force: bool = False):
    """
    reformat a document profile
    """
    reformat_command(NormRenderProfile, path, output, force)
