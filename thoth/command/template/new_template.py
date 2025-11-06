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
from thoth.model.meta_model import DocumentMetaModel
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
    determined_format = determined_format.resolve()
    if output is None and determined_format in FORMAT_REQUIRES_OUTPUT:
        print(f"please use '--output' to save files of format - {determined_format.value}", file=sys.stderr)
        sys.exit(1)
    return determined_format


def new_template(
    model: Path = DOCUMENT_MODEL_PATH_OPTION,
    indent: Annotated[int, typer.Option(min=0, max=8, clamp=True)] = 0,
    output: OUTPUT_PATH_OPTION = None,
    force: bool = False,
    format: Annotated[OutputFormat | None, typer.Option(help="[default: from --output, fallback: txt]")] = None,
) -> None:
    """
    create a starting point for a template

    Output is always plain text, which may be converted to other formats.
    """
    document_class = DocumentMetaModel.document_class_from_file(model)
    document_class.set_indent(indent)  # type: ignore[attr-defined]

    format = determine_format(output, format)

    if format == OutputFormat.DOCX:
        document_class.set_docx_rendering()  # type: ignore[attr-defined]
    template_lines = document_class.render_template()  # type: ignore[attr-defined]
    context = {
        "template": {
            "lines": template_lines.splitlines(),
        },
    }

    if format == OutputFormat.TEXT:
        loader = jinja2.FileSystemLoader(templates_home())
        jinja2_template = jinja2.Environment(loader=loader).get_template("template.txt")
        rendered = jinja2_template.render(**context)
        write_output(rendered, destination=output, force=force)
    elif format == OutputFormat.DOCX:
        meta_template = templates_home() / "template.docx"
        if not meta_template.exists():
            raise FileNotFoundError(meta_template)
        doc = DocxTemplate(meta_template)
        doc.render(context)
        doc.save(output.with_suffix(".docx"))
