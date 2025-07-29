# standard library imports
import sys
from pathlib import Path

from thoth.command.shared.output_format import OutputFormat

# third party imports
# own imports
from thoth.model.norm.norm import Norm
from thoth.renderers.html import html_render_translation_page


def render_translated_norm(
    path: Path,
    language_1: str,
    language_2: str,
    output: Path | None = None,
    format: OutputFormat | None = None,
    force: bool = False,
) -> None:
    """
    render a norm definition in two languages, side by side
    """
    if not path.is_file():
        print(f"so such file - {path}", file=sys.stderr)
        sys.exit(1)

    if format is None and output is None:
        print("need output or format", file=sys.stderr)
        sys.exit(1)

    if format is None:
        suffix = output.suffix  # type: ignore
        if suffix == "":
            print(f"cannot determine format from - {output}", file=sys.stderr)
            sys.exit(1)
        try:
            format = OutputFormat(suffix[1:])
        except ValueError:
            print(f"cannot render - {suffix}", file=sys.stderr)
            sys.exit(1)

    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)

    norm = Norm.from_yaml(path.open())
    total_count, language_counts = norm.count_multi_lingual()
    if language_1 not in language_counts:
        print(f"language '{language_1}' not in - {path}", file=sys.stderr)
        sys.exit(1)
    if language_2 not in language_counts:
        print(f"language '{language_2}' not in - {path}", file=sys.stderr)
        sys.exit(1)

    writer = print if output is None else output.write_text

    match format:
        case OutputFormat.HTML:
            html = html_render_translation_page.render_translation(norm, language_1, language_2)
            writer(html)
        case _:
            print(f"cannot render .{format.value}, yet")
