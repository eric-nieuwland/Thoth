"""
new_document - create a new document
"""

from __future__ import annotations

# standard library imports
from pathlib import Path

# third party imports
import typer

# own imports
from thoth.command.shared.write_output import write_output
from thoth.model.meta_model import DocumentMetaModel


def new_document(
    model: Path = typer.Option(exists=True, readable=True),
    output: Path | None = None,
    force: bool = False,
) -> None:
    """
    create a starting point for a document
    """
    document_class = DocumentMetaModel.document_class_from_file(model)
    document = document_class.example(detect_loop=False)
    write_output(document.as_yaml_text(), destination=output, force=force)
