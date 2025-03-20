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


def split_norm(
        path: Path,
        language: str,
        output: Path | None = None,
        force: bool = False,
):
    """
    split a specific langauge off a norm
    """
    if not path.is_file():
        print(f"so such file - {path}", file=sys.stderr)
        sys.exit(1)

    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)

    norm = Norm.from_yaml(path.open())
    total, language_counts = norm.count_multi_lingual()

    if language not in language_counts and not force:
        print(f"language not in '{path}' - '{language}'", file=sys.stderr)
        sys.exit(1)
    if language_counts[language] != total and not force:
        print(f"language incomplete in '{path}' - '{language}'", file=sys.stderr)
        sys.exit(1)

    writer = print if output is None else output.write_text

    lang_norm = norm.isolate_language(language)
    writer(lang_norm.as_yaml())
