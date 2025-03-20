# standard library imports
from pathlib import Path
import sys

# third party imports

# own imports
from model.norm import Norm
from renderers.html.html_render_norm_page import render
from ._shared import OutputFormat, Audience



def audience(
        path: Path,
        language: str,
        audience: Audience = Audience.GEEKS.value,
        output: Path | None = None,
        format: OutputFormat | None = None,
        force: bool = False,
):
    """
    render a norm definition in a document format
    """
    if not path.is_file():
        print(f"so such file - {path}", file=sys.stderr)
        sys.exit(1)

    if format is None and output is None:
        print(f"need output or format", file=sys.stderr)
        sys.exit(1)

    if format is None:
        suffix = output.suffix
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
    if language not in language_counts:
        print(f"language '{language}' not in - {path}", file=sys.stderr)
        sys.exit(1)
    if language_counts[language] < total_count:
        print(f"""
WARNING: language '{language}' incomplete in - {path}
         check output for warnings
        """.strip(), file=sys.stderr)

    writer = print if output is None else output.write_text

    match audience:
        case Audience.MANAGEMENT:
            template = "highlights"
        case Audience.DEVELOPERS:
            template = "with-guidance"
        case Audience.TESTERS:
            template = "checks"
        case Audience.GEEKS:
            template = "complete"
        case _:
            template = "complete"

    match format:
        case OutputFormat.HTML:
            print(f"{template}")
            html = render(norm, language)
            writer(html)
        case _:
            print(f"cannot render .{format.value}, yet")
