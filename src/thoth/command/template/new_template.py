"""
new_template - create a new template
"""

from __future__ import annotations

# standard library imports
import sys
from pathlib import Path
from typing_extensions import Annotated

# third party imports
import jinja2
import typer
from docxtpl import DocxTemplate  # type: ignore[import-untyped]

# own imports
from thoth.command.shared.arguments_and_options_info import (
    DOCUMENT_MODEL_PATH_OPTION,
    OUTPUT_PATH_OPTION,
)
from thoth.command.shared.output_format import OutputFormat
from thoth.command.shared.write_output import write_output
from thoth.model.document_model import DocumentModel
from thoth.templates import templates_home

FORMAT_REQUIRES_OUTPUT = {
    OutputFormat.DOCX,
}
DEFAULT_FORMAT = OutputFormat.TEXT


def determine_format(
    output: Path | None = None,
    format: OutputFormat | None = None,
) -> OutputFormat:
    determined_format = format or OutputFormat.from_path(output)
    if determined_format is None:
        return DEFAULT_FORMAT
    if output is None and determined_format in FORMAT_REQUIRES_OUTPUT:
        print(f"please use '--output' to save files of format - {determined_format.value}", file=sys.stderr)
        sys.exit(1)
    return determined_format


def new_template(
    model: DOCUMENT_MODEL_PATH_OPTION,
    indent: Annotated[int, typer.Option(min=0, max=8, clamp=True)] = 0,
    output: OUTPUT_PATH_OPTION = None,
    force: bool = False,
    format: Annotated[OutputFormat | None, typer.Option(help="[default: from --output, fallback: txt]")] = None,
) -> None:
    """
    create a starting point for a template

    Output is always plain text, which may be converted to other formats.
    """
    document_class = DocumentModel.document_class_from_file(model)
    document_class.set_indent(indent)  # type: ignore[attr-defined]

    format = determine_format(output, format)

    template = templates_home() / f"template.{format.value}"
    if not template.exists():
        raise FileNotFoundError(template)

    if format == OutputFormat.DOCX:
        document_class.set_docx_rendering()  # type: ignore[attr-defined]

    template_lines = document_class.render_template()  # type: ignore[attr-defined]
    context = {
        "template": {
            "lines": template_lines.splitlines(),
        },
    }

    if format == OutputFormat.DOCX:
        doc = DocxTemplate(template)
        doc.render(context)
        doc.save(output.with_suffix(".docx"))
    else:
        loader = jinja2.FileSystemLoader(template.parent)
        jinja2_template = jinja2.Environment(loader=loader).get_template(template.name)
        rendered = jinja2_template.render(**context)
        write_output(rendered, destination=output, force=force)
