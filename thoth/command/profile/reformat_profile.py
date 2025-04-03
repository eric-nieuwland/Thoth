# standard library imports
from pathlib import Path
import sys

# third party imports

# own imports
from model.profile.profile import Profile


def reformat_profile(path: Path, output: Path | None = None, force: bool = False):
    """
    reformat a document profile
    """
    if not path.is_file():
        print(f"no such file - {path}", file=sys.stderr)
        sys.exit(1)

    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)

    writer = print if output is None else output.write_text

    document = Profile.from_yaml(path.open())
    writer(document.as_yaml())
