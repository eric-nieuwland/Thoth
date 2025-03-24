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
        rest: Path | None = None,
        force: bool = False,
):
    """
    split a specific language off a norm
    """
    if not path.is_file():
        print(f"so such file - {path}", file=sys.stderr)
        sys.exit(1)

    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)
    if rest is not None and rest.exists() and not force:
        print(f"file exists - {rest}", file=sys.stderr)
        sys.exit(1)

    norm = Norm.from_yaml(path.open())
    total, language_counts = norm.count_multi_lingual()

    count = language_counts.get(language)
    if count is None and not force:
        print(f"language not in '{path}' - '{language}'", file=sys.stderr)
        sys.exit(1)
    if count is not None and count != total and not force:
        print(f"language incomplete in '{path}' - '{language}'", file=sys.stderr)
        sys.exit(1)

    if output:
        writer = print if str(output).strip() == "-" else output.write_text
        lang_norm = norm.copy_for_language(language)
        writer(lang_norm.as_yaml())

    if output is None and rest and str(rest).strip() == "-":
        print("")
        print(f"--- # selected language '{language}' above - remaining languages below")
        print("")

    if rest:
        retained_languages = [lang for lang in language_counts if lang != language]
        if len(retained_languages) == 0:
            # no languages left -> empty file
            rest.write_text("")
            sys.exit(0)
        if len(retained_languages) == len(language_counts):
            rest_norm = norm  # no need to get smart
        else:
            rest_norm = norm.copy_for_language(retained_languages[0])
            retained_languages.pop(0)
            while retained_languages:
                rest_norm = rest_norm | norm.copy_for_language(retained_languages[0])
                retained_languages.pop(0)

        writer = print if str(rest).strip() == "-" else rest.write_text

        writer(rest_norm.as_yaml())
