"""
argument_info - command line arguments and options
"""

from __future__ import annotations

# standard library imports
from pathlib import Path
from typing_extensions import Annotated

# third party imports
import typer


MODEL_OPTION = typer.Option(help="document model", exists=True, readable=True)
DOCUMENT_PATH_ARGUMENT = typer.Argument(metavar="DOCUMENT", help="document path", exists=True, readable=True)
LANGUAGE_ARGUMENT = typer.Argument(help="language to render", exists=True, readable=True, callback=check_language_code)
PROFILE_OPTION = Annotated[
    Path | None,
    typer.Option(
        help="document profile (default: render everything)",
        exists=True,
        readable=True,
    ),
]
TEMPLATE_OPTION = typer.Option(help="template to render with", exists=True, readable=True, resolve_path=True)
