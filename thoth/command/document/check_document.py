"""
check_document - check syntax of a document
"""

from __future__ import annotations

# standard library imports
from pathlib import Path

# third party imports

# own imports
from thoth.command.shared.arguments_and_options_info import (
    MODEL_OPTION,
    DOCUMENT_PATH_ARGUMENT,
)
from thoth.command.shared.print_file_contents_comparison import print_file_contents_comparison
from thoth.model.meta_model import DocumentMetaModel


def check_document(
    model: Path = MODEL_OPTION,
    path: Path = DOCUMENT_PATH_ARGUMENT,
) -> None:
    """
    check syntax of a document

    Prints a message to help you correct any issue found and "OK" if no issues were found.
    """
    document_class = DocumentMetaModel.document_class_from_file(model)  # derive document class
    copy = document_class.from_yaml(path).as_yaml_text()  # type: ignore[attr-defined]
    # here only if path was successfully loaded
    print_file_contents_comparison(path, copy)
