# standard library imports
import sys
from pathlib import Path

# third party imports
# own imports
from thoth.model.norm.norm import Norm
from thoth.process.norm.compare_norm_structures import compare_norm_structures


def _report_issues(
    path1: Path,
    path2: Path,
    issue_kind: str,
    issues: list[str] | tuple[str, ...],
) -> None:
    if issues:
        print(f"{issue_kind} found in '{path1}' <-> '{path2}':")
        for issue in issues:
            extra = len(issue) - len(stripped := issue.lstrip())
            print(f"  {' ' * extra}- {stripped}")


def xcheck_norm(path1: Path, path2: Path):
    """
    check whether two norm definitions match
    """
    if not path1.is_file():
        print(f"so such file - {path1}", file=sys.stderr)
        sys.exit(1)
    if not path2.is_file():
        print(f"so such file - {path2}", file=sys.stderr)
        sys.exit(1)

    norm1 = Norm.from_yaml(path1.open())
    norm2 = Norm.from_yaml(path2.open())

    differences = compare_norm_structures(norm1, norm2)

    _report_issues(path1, path2, "differences", differences)
