# standard library imports
import sys
from pathlib import Path

# third party imports

# own imports
from model.norm.norm import Norm


def update_norm(
    path1: Path,
    path2: Path,
    output: Path | None = None,
    force: bool = False,
):
    """
    update norm from a second norm
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
        retained_languages = list(set(language_counts1) - shared_languages)
        if len(retained_languages) == 0:
            print(f"'{path2}' completely replaces '{path1}'", file=sys.stderr)
            sys.exit(1)
        _norm1 = norm1.copy_for_language(retained_languages[0])
        retained_languages.pop(0)
        while retained_languages:
            _norm1 = _norm1 | norm1.copy_for_language(retained_languages[0])
            retained_languages.pop(0)
        norm1 = _norm1

    try:
        new_norm = norm1 | norm2
    except ValueError as err:
        print(f"unable to join '{path1}' and '{path2}' - {err}")
        sys.exit(1)

    writer = print if output is None else output.write_text

    writer(new_norm.as_yaml())
