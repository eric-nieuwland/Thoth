"""
new_template - create a new template
"""

from __future__ import annotations

# standard library imports
from pathlib import Path
from typing_extensions import Annotated

# third party imports
import typer

# own imports
from thoth.command.shared.arguments_and_options_info import (
    DOCUMENT_MODEL_PATH_OPTION,
)
from thoth.command.shared.write_output import write_output
from thoth.model.meta_model import DocumentMetaModel


def new_template(
    model: Path = DOCUMENT_MODEL_PATH_OPTION,
    indent: Annotated[int, typer.Option(min=0, max=8, clamp=True)] = 0,
    output: Path | None = None,
    force: bool = False,
) -> None:
    """
    create a starting point for a template
    """
    document = DocumentMetaModel.document_class_from_file(model)
    document.set_indent(indent)  # type: ignore[attr-defined]
    template = document.render_template()  # type: ignore[attr-defined]
    write_output(template, destination=output, force=force)
