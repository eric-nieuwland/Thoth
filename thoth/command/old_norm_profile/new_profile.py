# standard library imports
from pathlib import Path

# third party imports
# own imports
from thoth.model.norm_profile.profile import NormRenderProfile

from ..shared.new_command import new_command


def new_profile(
    output: Path | None = None,
    force: bool = False,
) -> None:
    """
    create a starting point for a document profile
    """
    new_command(NormRenderProfile, output, force)
