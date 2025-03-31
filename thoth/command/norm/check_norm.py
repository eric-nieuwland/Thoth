# standard library imports
from pathlib import Path
import sys

# third party imports

# own imports
from model.norm_definition.norm import Norm


def _report_issues(path: Path, issue_kind: str, issues: list[str]) -> None:
    if issues:
        print(f"{issue_kind} found in '{path}':")
        for issue in issues:
            print(f"  - {issue}")


def check_norm(path: Path):
    """
    check a norm for various issues
    """
    if not path.is_file():
        print(f"so such file - {path}", file=sys.stderr)
        sys.exit(1)

    norm = Norm.from_yaml(path.open())

    inconsistent_identifiers = norm.check_identifiers()
    _report_issues(path, "inconsistent identifiers", inconsistent_identifiers)

    total, language_counts = norm.count_multi_lingual()
    incomplete_translations = list(sorted(lang for lang, count in language_counts.items() if count != total))
    _report_issues(path, "incomplete translations", incomplete_translations)

    if not inconsistent_identifiers and not incomplete_translations:
        print(f"'{path}' seems OK")
