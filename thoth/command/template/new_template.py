"""
new_template - create a new template
"""

from __future__ import annotations

# standard library imports
from pathlib import Path
from typing_extensions import Annotated
import sys

# third party imports
import typer

# own imports
from thoth.command.shared.arguments_and_options_info import (
    DOCUMENT_MODEL_PATH_OPTION,
)
from thoth.command.shared.output_format import OutputFormat
from thoth.command.shared.write_output import write_output
from thoth.model.meta_model import DocumentMetaModel

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
    output: Path | None = None,
    force: bool = False,
    format: Annotated[OutputFormat | None, typer.Option(help="[default: from --output, fallback: txt]")] = None,
) -> None:
    """
    create a starting point for a template

    Output is always plain text, which may be converted to other formats.
    """
    document = DocumentMetaModel.document_class_from_file(model)
    document.set_indent(indent)  # type: ignore[attr-defined]
    determined_format = determine_format(output, format)
    if determined_format is OutputFormat.DOCX:
        document.set_docx_rendering()
    template = document.render_template()  # type: ignore[attr-defined]
    write_output(template, destination=output, force=force)
