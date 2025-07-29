# standard library imports
import sys
from datetime import datetime, timezone
from pathlib import Path

# third party imports
from docxtpl import DocxTemplate  # type: ignore[import-untyped]
from jinja2 import Environment, FileSystemLoader

from thoth.command.shared.output_format import OutputFormat

# own imports
from thoth.model.norm.norm import Norm
from thoth.model.profile.profile import NormRenderProfile
from thoth import templates


FORMAT_REQUIRES_OUTPUT = {
    OutputFormat.DOCX,
}


def render_norm(
    path: Path,
    language: str,
    profile: Path | None = None,
    output: Path | None = None,
    format: OutputFormat | None = None,
    force: bool = False,
):
    """
    render a norm definition in a document format
    """
    if not path.is_file():
        print(f"no such file - {path}", file=sys.stderr)
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

    if output is None and format in FORMAT_REQUIRES_OUTPUT:
        print(
            f"please use '--output' to save files of format - {format.value}",
            file=sys.stderr,
        )
        sys.exit(1)

    if profile is not None and not profile.exists():
        print(f"so such file - {profile}", file=sys.stderr)
        sys.exit(1)

    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)

    if profile is None:
        prof = NormRenderProfile.yes_to_all()
    else:
        prof = NormRenderProfile.from_yaml(profile.open())
        if not prof:
            print(f"profile does not select anything - '{profile}'", file=sys.stderr)
            sys.exit(1)

    norm = Norm.from_yaml(path.open())
    total_count, language_counts = norm.count_multi_lingual()
    if language not in language_counts:
        print(f"language '{language}' not in - {path}", file=sys.stderr)
        sys.exit(1)
    if language_counts[language] < total_count:
        print(
            f"""
WARNING: language '{language}' incomplete in - {path}
         check output for warnings
        """.strip(),
            file=sys.stderr,
        )

    timestamp = datetime.now(tz=timezone.utc)
    context = dict(
        source=path.name,
        timestamp=timestamp,
        profile=prof,
        norm=norm,
        language=language,
    )

    match format:
        case OutputFormat.HTML:
            # prepare rendering by Jinja2
            loader = FileSystemLoader(templates.home() / "html" / "norm")
            template = Environment(loader=loader).get_template("norm.html")
            # produce rendered norm
            html = template.render(**context)
            writer = print if output is None else output.write_text
            writer(html)
        case OutputFormat.DOCX:
            template = templates.home() / "docx" / "norm" / "norm.docx"
            doc = DocxTemplate(template)
            doc.render(context)
            doc.save(output)  # type: ignore
        case _:
            print(f"cannot render .{format.value if format else "???"}, yet")
