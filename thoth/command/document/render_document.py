"""
render_document - render a document
"""

from __future__ import annotations

# standard library imports
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing_extensions import Annotated

# third party imports
import jinja2
import typer
from docxtpl import DocxTemplate  # type: ignore[import-untyped]

# own imports
from thoth.command.shared.output_format import OutputFormat
from thoth.command.shared.write_output import write_output
from thoth.model.meta_model import DocumentMetaModel

MODEL_OPTION = typer.Option(help="document model", exists=True, readable=True)
DOCUMENT_PATH_ARGUMENT = typer.Argument(metavar="DOCUMENT", help="document path", exists=True, readable=True)
LANGUAGE_ARGUMENT = typer.Argument(help="language to render", exists=True, readable=True)
PROFILE_OPTION = Annotated[
    Path | None,
    typer.Option(
        help="document profile (default: render everything)",
        exists=True,
        readable=True,
    ),
]
TEMPLATE_OPTION = typer.Option(help="template to render with", exists=True, readable=True, resolve_path=True)


FORMAT_REQUIRES_OUTPUT = {
    OutputFormat.DOCX,
}


def path_to_format(path: Path | None) -> OutputFormat | None:
    if path is None:
        return None
    try:
        return OutputFormat(path.suffix[1:])
    except ValueError:
        return None


def determine_format(
    template: Path,
    output: Path | None = None,
    format: OutputFormat | None = None,
) -> OutputFormat:
    determined_format = format or path_to_format(template) or path_to_format(output)
    if determined_format is None:
        print("need format from '--format', '--output', or '--template'", file=sys.stderr)
        sys.exit(1)
    determined_format = determined_format.resolve()
    if output is None and determined_format in FORMAT_REQUIRES_OUTPUT:
        print(f"please use '--output' to save files of format - {determined_format.value}", file=sys.stderr)
        sys.exit(1)
    return determined_format


def handle_language(document, path, language) -> None:
    total_count, language_counts = document.count_multi_lingual()
    if language not in language_counts:
        print(f"language '{language}' not in - {path}", file=sys.stderr)
        sys.exit(1)
    if language_counts[language] < total_count:
        print(
            f"""
    WARNING: language '{language}' incomplete in - {path}
             check output for warnings
            """.strip(),
            file=sys.stderr,
        )


def render_document(
    model: Path = MODEL_OPTION,
    path: Path = DOCUMENT_PATH_ARGUMENT,
    language: str = LANGUAGE_ARGUMENT,
    profile: PROFILE_OPTION = None,
    template: Path = TEMPLATE_OPTION,
    output: Path | None = None,
    force: bool = False,
    format: OutputFormat | None = None,
) -> None:
    """
    render a document

    Prints a message to help you correct any issue found and "OK" if no issues were found.
    """

    format = determine_format(template, output, format)

    document_model = DocumentMetaModel.from_yaml(model)
    document_class = document_model.create_document_class(model.stem)  # derive document class
    profile_class = document_model.create_profile_class(model.stem)  # derive profile class
    document = document_class.from_yaml(path)  # type: ignore[attr-defined]
    document_profile = profile_class.from_yaml(profile) if profile else profile_class.yes_to_all()  # type: ignore[attr-defined]

    handle_language(document, path, language)

    context = {
        "document": document,
        "language": language,
        "profile": document_profile,
        "source": path.name,
        "timestamp": datetime.now(tz=timezone.utc),
    }

    if format == OutputFormat.TEXT:
        loader = jinja2.FileSystemLoader(template.parent)
        jinja2_template = jinja2.Environment(loader=loader).get_template(template.name)
        rendered = jinja2_template.render(**context)
        write_output(rendered, output, force=force)
    elif format == OutputFormat.DOCX:
        doc = DocxTemplate(template)
        doc.render(context)
        doc.save(output)
