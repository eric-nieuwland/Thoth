# standard library imports
from pathlib import Path
import sys

# third party imports

# own imports
from model.norm import Norm


def _report_issues(path: Path, issue_kind: str, issues: list[str]) -> None:
    if issues:
        print(f"{issue_kind} found in '{path}':")
        for issue in issues:
            print(f"  - {issue}")


def reformat_norm(path: Path, output: Path | None = None, force: bool = False):
    """
    reformat a norm
    """
    if not path.is_file():
        print(f"so such file - {path}", file=sys.stderr)
        sys.exit(1)

    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)

    writer = print if output is None else output.write_text

    norm = Norm.from_yaml(path.open())
    writer(norm.as_yaml())
