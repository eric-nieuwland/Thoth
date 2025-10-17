# standard library imports
import sys
from pathlib import Path

# third party imports

# own imports


def write_output(
    output,
    destination: Path | None = None,
    force: bool = False,
) -> None:
    """
    write output to file or stdout
    """
    if destination is not None and destination.exists() and not force:
        print(f"file exists - {destination}", file=sys.stderr)
        sys.exit(1)

    writer = print if destination is None else destination.write_text

    writer(output)
