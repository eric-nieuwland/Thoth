# standard library imports
import sys
from pathlib import Path

# third party imports
# own imports
from thoth.command.shared.output_format import OutputFormat


def new_template(
    output: Path,
    format: OutputFormat | None = None,
    force: bool = False,
):
    """
    create a starting point for a template definition
    """

    if output.exists() and not force:
        print(f"exists - {output}", file=sys.stderr)
        sys.exit(1)
    if output.exists() and not output.is_dir():
        print(f"not a directory - {output}", file=sys.stderr)
        sys.exit(1)

    formats = [f.value for f in ((format,) if format else OutputFormat.all())]

