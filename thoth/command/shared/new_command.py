# standard library imports
import sys
from pathlib import Path

# third party imports

# own imports


def new_command(
    klass,
    output: Path | None = None,
    force: bool = False,
    **kwargs,
) -> None:
    """
    create a starting point for a document
    """
    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)

    writer = print if output is None else output.write_text

    writer(klass.template(**kwargs).as_yaml())
