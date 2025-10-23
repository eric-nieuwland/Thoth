"""
render_document - render a document
"""

from __future__ import annotations

# standard library imports
from datetime import datetime, timezone
from pathlib import Path
from typing_extensions import Annotated

# third party imports
import jinja2
import typer

# own imports
from thoth.command.shared.write_output import write_output
from thoth.model.meta_model import DocumentMetaModel

MODEL_OPTION = typer.Option(help="document model", exists=True, readable=True)
DOCUMENT_PATH_ARGUMENT = typer.Argument(metavar="DOCUMENT", help="document path", exists=True, readable=True)
PROFILE_OPTION = Annotated[
        Path | None,
        typer.Option(
            help="document profile (default: render everything)",
            exists=True,
            readable=True,
        ),
    ]
TEMPLATE_OPTION = typer.Option(help="template to render with", exists=True, readable=True, resolve_path=True)


def render_document(
    model: Path = MODEL_OPTION,
    path: Path = DOCUMENT_PATH_ARGUMENT,
    profile: PROFILE_OPTION = None,
    template: Path = TEMPLATE_OPTION,
    output: Path | None = None,
    force: bool = False,
) -> None:
    """
    render a document

    Prints a message to help you correct any issue found and "OK" if no issues were found.
    """
    document_model = DocumentMetaModel.from_yaml(model)
    document_class = document_model.create_document_class(model.stem)  # derive document class
    profile_class = document_model.create_profile_class(model.stem)  # derive profile class
    document = document_class.from_yaml(path)
    document_profile = profile_class.from_yaml(profile) if profile else profile_class.yes_to_all()

    loader = jinja2.FileSystemLoader(template.parent)
    data = {
        "document": document,
        "language": "en",
        "profile": document_profile,
        "source": path.name,
        "timestamp": datetime.now(tz=timezone.utc),
    }
    jinja2_template = jinja2.Environment(loader=loader).get_template(template.name)
    rendered = jinja2_template.render(**data)
    write_output(rendered, output, force=force)
