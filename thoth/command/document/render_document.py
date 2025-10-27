"""
render_document - render a document
"""

from __future__ import annotations

# standard library imports
import sys
from datetime import datetime, timezone
from pathlib import Path

# third party imports
import jinja2
import typer
from docxtpl import DocxTemplate  # type: ignore[import-untyped]

# own imports
from thoth.command.shared.arguments_and_options_info import (
    DOCUMENT_MODEL_PATH_OPTION,
    DOCUMENT_PATH_ARGUMENT,
    OUTPUT_PATH_OPTION,
    RENDER_PROFILE_PATH_OPTION,
    RENDER_TEMPLATE_PATH_OPTION,
)
from thoth.command.shared.output_format import OutputFormat
from thoth.command.shared.write_output import write_output
from thoth.model.meta_model import DocumentMetaModel
from thoth.utils.iso_639 import is_iso_639_language_code

FORMAT_REQUIRES_OUTPUT = {
    OutputFormat.DOCX,
}


def determine_format(
    template: Path,
    output: Path | None = None,
    format: OutputFormat | None = None,
) -> OutputFormat:
    determined_format = format or OutputFormat.from_path(template) or OutputFormat.from_path(output)
    if determined_format is None:
        print("need format from '--format', '--output', or '--template'", file=sys.stderr)
        sys.exit(1)
    determined_format = determined_format.resolve()
    if output is None and determined_format in FORMAT_REQUIRES_OUTPUT:
        print(f"please use '--output' to save files of format - {determined_format.value}", file=sys.stderr)
        sys.exit(1)
    return determined_format


def check_language_code(value: str):
    if not is_iso_639_language_code(value):
        raise typer.BadParameter(f"unknown language code '{value}'")
    return value


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


LANGUAGE_ARGUMENT = typer.Argument(help="language to render", exists=True, readable=True, callback=check_language_code)


def render_document(
    model: DOCUMENT_MODEL_PATH_OPTION,
    path: DOCUMENT_PATH_ARGUMENT,
    template: RENDER_TEMPLATE_PATH_OPTION,
    language: str = LANGUAGE_ARGUMENT,
    profile: RENDER_PROFILE_PATH_OPTION = None,
    output: OUTPUT_PATH_OPTION(optional=True) = None,
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
