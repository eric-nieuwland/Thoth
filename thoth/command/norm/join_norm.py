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


def join_norm(
        path1: Path,
        path2: Path,
        output: Path | None = None,
        force: bool = False,
):
    """
    join two norms iff they only differ in language
    """
    if not path1.is_file():
        print(f"so such file - {path1}", file=sys.stderr)
        sys.exit(1)
    if not path2.is_file():
        print(f"so such file - {path2}", file=sys.stderr)
        sys.exit(1)

    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)

    norm1 = Norm.from_yaml(path1.open())
    norm2 = Norm.from_yaml(path2.open())
    total1, language_counts1 = norm1.count_multi_lingual()
    total2, language_counts2 = norm2.count_multi_lingual()

    shared_languages = set(language_counts1) & set(language_counts2)
    if shared_languages:
        print(f"shared languages '{"', '".join(sorted(shared_languages))}'", file=sys.stderr)
        sys.exit(1)

    try:
        new_norm = norm1 | norm2
    except ValueError as err:
        print(f"unable to join '{path1}' and '{path2}' - {err}")
        sys.exit(1)

    writer = print if output is None else output.write_text

    writer(new_norm.as_yaml())
