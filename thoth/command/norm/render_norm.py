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
from thoth.model.norm_profile.profile import NormRenderProfile
from thoth.templates import templates_home

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
    template: Path | None = None,
) -> None:
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

    if template is None:
        template = templates_home()
    elif not template.exists() or not template.is_dir():
        print(f"no such directory - {template}", file=sys.stderr)
        sys.exit(1)

    # walk the template directory structure towards the template needed
    template_dir = template / format.value
    template_name = f"norm.{format.value}"
    if not template_dir.is_dir():
        print(f"no template(s) for '{format.value}' - {template}", file=sys.stderr)
        sys.exit(1)
    template_dir = template_dir / "norm"
    if not template_dir.is_dir() or not (template_dir / template_name).is_file():
        print(f"no norm template for '{format.value}' - {template}", file=sys.stderr)
        sys.exit(1)

    timestamp = datetime.now(tz=timezone.utc)
    context = dict(
        source=path.name,
        timestamp=timestamp,
        profile=prof,
        norm=norm,
        language=language,
    )

    renderer = error_renderer
    match format:
        case OutputFormat.HTML:
            renderer = jinja_renderer
        case OutputFormat.DOCX:
            renderer = docx_renderer
        case OutputFormat.MD:
            renderer = jinja_renderer
    renderer(format, template_dir, template_name, context, output)


def error_renderer(
    format: OutputFormat,
    template_dir: Path,
    template_name: str,
    context: dict[str, object],
    output: Path | None,
) -> None:
    _ignore = template_dir, template_name, context, output
    print(f"cannot render .{format.value if format else '???'}, yet")
    sys.exit(1)


def jinja_renderer(
    format: OutputFormat,
    template_dir: Path,
    template_name: str,
    context: dict[str, object],
    output: Path | None,
) -> None:
    _ignore = format
    # prepare rendering by Jinja2
    loader = FileSystemLoader(template_dir)
    md_template = Environment(loader=loader).get_template(template_name)
    # produce rendered norm
    rendered = md_template.render(**context)
    writer = print if output is None else output.write_text
    writer(rendered)


def docx_renderer(
    format: OutputFormat,
    template_dir: Path,
    template_name: str,
    context: dict[str, object],
    output: Path | None,
) -> None:
    _ignore = format
    doc = DocxTemplate(template_dir / template_name)
    doc.render(context)
    doc.save(output)
