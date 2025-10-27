"""
argument_and_options_info - shared command line arguments and options typing and documentation
"""

from __future__ import annotations

# standard library imports
from pathlib import Path
from typing_extensions import Annotated

# third party imports
import typer

# own imports


def _make_path_annotation(
    option_or_argument,
    *,
    help,
    optional,
    exists=True,
    readable=True,
    resolve_path=False,
):
    return Annotated[
        Path | None if optional else Path,
        option_or_argument(
            metavar="PATH",
            help=help,
            exists=exists,
            readable=readable,
            resolve_path=resolve_path,
        ),
    ]


DOCUMENT_MODEL_PATH_OPTION = _make_path_annotation(
    typer.Option,
    help="document model",
    optional=True,
)
DOCUMENT_PATH_ARGUMENT = _make_path_annotation(
    typer.Argument,
    help="document",
    optional=False,
)
OUTPUT_PATH_OPTION = _make_path_annotation(
    typer.Option,
    help="output",
    optional=True,
)
RENDER_PROFILE_PATH_ARGUMENT = _make_path_annotation(
    typer.Argument,
    help="document profile",
    optional=False,
)
RENDER_PROFILE_PATH_OPTION = _make_path_annotation(
    typer.Option,
    help="document profile (default: render everything)",
    optional=True,
)
RENDER_TEMPLATE_PATH_OPTION = _make_path_annotation(
    typer.Option,
    help="template to render with",
    resolve_path=True,
    optional=True,
)
