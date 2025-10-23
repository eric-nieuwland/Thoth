# standard library imports
import sys
from pathlib import Path

# third party imports
# own imports
from thoth.model.norm.norm import Norm


def split_norm(
    path: Path,
    language: str,
    output: Path | None = None,
    rest: Path | None = None,
    force: bool = False,
) -> None:
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

    output_writer = None if output is None else (print if str(output).strip() == "-" else output.write_text)
    rest_writer = None if rest is None else (print if str(rest).strip() == "-" else rest.write_text)

    norm = Norm.from_yaml(path.open())
    total, language_counts = norm.count_multi_lingual()

    count = language_counts.get(language)
    if count is None and not force:
        print(f"language not in '{path}' - '{language}'", file=sys.stderr)
        sys.exit(1)
    if count is not None and count != total and not force:
        print(f"language incomplete in '{path}' - '{language}'", file=sys.stderr)
        sys.exit(1)

    if output_writer:
        lang_norm = norm.copy_for_language(language)
        output_writer(lang_norm.as_yaml())

    if output_writer == print and rest_writer == print:
        print(f"\n\n--- # selected language '{language}' above - remaining languages below\n\n")

    if rest_writer:
        retained_languages = [lang for lang in language_counts if lang != language]
        if len(retained_languages) > 0:  # non-empty rest
            rest_norm = (
                norm if len(retained_languages) == len(language_counts) else norm.copy_for_language(*retained_languages)
            )
            rest_writer(rest_norm.as_yaml())
