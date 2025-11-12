"""
check_model - check syntax of a document model
"""

from __future__ import annotations

# standard library imports

# third party imports

# own imports
from thoth.command.shared.arguments_and_options_info import (
    DOCUMENT_PATH_ARGUMENT,
)
from thoth.command.shared.print_file_contents_comparison import print_file_contents_comparison
from thoth.model.document_model import DocumentModel


def check_model(
    path: DOCUMENT_PATH_ARGUMENT,
) -> None:
    """
    check syntax of a document model

    Prints a message to help you correct any issue found and "OK" if no issues were found.
    """
    copy = DocumentModel.from_yaml(path).as_yaml_text()
    # here only if path was successfully loaded
    print_file_contents_comparison(path, copy)
