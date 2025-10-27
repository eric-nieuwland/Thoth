"""
argument_info - command line arguments and options
"""

from __future__ import annotations

# standard library imports
from pathlib import Path
from typing_extensions import Annotated

# third party imports
import typer

# own imports


def _make_path_annotation(option_or_argument, *, optional=False):
    return Annotated[
        Path | None if optional else Path,
        option_or_argument,
    ]


DOCUMENT_MODEL_PATH_OPTION = Annotated[
    Path,
    typer.Option(metavar="PATH", help="document model", exists=True, readable=True),
]
DOCUMENT_PATH_ARGUMENT = Annotated[
    Path,
    typer.Argument(metavar="PATH", help="document", exists=True, readable=True),
]

def _make_output_path_option(*, optional=False):
    return Annotated[
        Path | None if optional else Path,
        typer.Option(metavar="PATH", help="output", exists=False, readable=False),
    ]
OUTPUT_PATH_OPTION = _make_output_path_option

def _make_render_profile_path_option(*, optional=False):
    return _make_path_annotation(
        typer.Option(
            metavar="PATH",
            help="document profile (default: render everything)",
            exists=True,
            readable=True,
        ),
        optional=optional,
    )
RENDER_PROFILE_PATH_OPTION = _make_render_profile_path_option

RENDER_TEMPLATE_PATH_OPTION = Annotated[
    Path,
    typer.Option(metavar="PATH", help="template to render with", exists=True, readable=True, resolve_path=True),
]
