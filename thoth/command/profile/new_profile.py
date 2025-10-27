"""
new_profile - create a new profile
"""

from __future__ import annotations

# standard library imports

# third party imports

# own imports
from thoth.command.shared.arguments_and_options_info import (
    DOCUMENT_MODEL_PATH_OPTION,
    OUTPUT_PATH_OPTION,
)
from thoth.command.shared.write_output import write_output
from thoth.model.meta_model import DocumentMetaModel


def new_profile(
    model: DOCUMENT_MODEL_PATH_OPTION,
    output: OUTPUT_PATH_OPTION(optional=True) = None,
    force: bool = False,
) -> None:
    """
    create a starting point for a profile
    """
    document_model = DocumentMetaModel.from_yaml(model, exit_on_error=True)
    profile_model = document_model.create_profile_class(model.stem)  # derive profile class
    profile = profile_model.yes_to_all()  # type: ignore[attr-defined] # create profile with all elements enabled
    write_output(profile.as_yaml_text(), destination=output, force=force)
