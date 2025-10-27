"""
check_profile - check syntax of a profile
"""

from __future__ import annotations

# standard library imports
from pathlib import Path

# third party imports
import typer

# own imports
from thoth.command.shared.arguments_and_options_info import (
    DOCUMENT_MODEL_PATH_OPTION,
    RENDER_PROFILE_PATH_OPTION,
)
from thoth.command.shared.print_file_contents_comparison import print_file_contents_comparison
from thoth.model.meta_model import DocumentMetaModel


def check_profile(
    model: DOCUMENT_MODEL_PATH_OPTION,
    path: RENDER_PROFILE_PATH_OPTION(),
) -> None:
    """
    check syntax of a profile

    Prints a message to help you correct any issue found and "OK" if no issues were found.
    """
    document_model = DocumentMetaModel.from_yaml(model, exit_on_error=True)
    profile_model = document_model.create_profile_class(model.stem)  # derive profile model
    copy = profile_model.from_yaml(path).as_yaml_text()  # type: ignore[attr-defined]
    # here only if path was successfully loaded
    print_file_contents_comparison(path, copy)
