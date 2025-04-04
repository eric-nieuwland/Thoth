# standard library imports
from pathlib import Path
import sys

# third party imports

# own imports
from model.profile.profile import Profile


def new_profile(
        output: Path | None = None,
        force: bool = False,
):
    """
    create a starting point for a document profile
    """
    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)

    writer = print if output is None else output.write_text

    writer(Profile.template().as_yaml())
