# standard library imports
import sys
from pathlib import Path

# third party imports

# own imports


def reformat_command(
    klass,
    path: Path,
    output: Path | None = None,
    force: bool = False,
) -> None:
    """
    reformat a document
    """
    if not path.is_file():
        print(f"no such file - {path}", file=sys.stderr)
        sys.exit(1)

    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)

    writer = print if output is None else output.write_text

    document = klass.from_yaml(path.open())
    writer(document.as_yaml())
