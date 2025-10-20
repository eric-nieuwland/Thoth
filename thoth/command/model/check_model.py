"""
check_model - check syntax of a document model
"""

from __future__ import annotations

# standard library imports
from pathlib import Path

# third party imports

# own imports
from thoth.model.meta_model import DocumentMetaModel
from thoth.command.shared.suggest_changes_to_original import suggest_changes_to_original


def check_model(
    path: Path,
) -> None:
    """
    check syntax of a document model
    """
    copy = DocumentMetaModel.from_yaml(path).as_yaml_text()
    # here only if path was successfully loaded
    with (open(path) as f):
        original = f.read()
    if not suggest_changes_to_original(original, copy):
        print("OK")
