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
from thoth.command.shared.arguments_and_options_info import (
    DOCUMENT_MODEL_PATH_OPTION,
    DOCUMENT_PATH_ARGUMENT,
    FRAGMENT_PATH_OPTION,
    OUTPUT_PATH_OPTION,
    RENDER_PROFILE_PATH_OPTION,
    RENDER_TEMPLATE_PATH_OPTION,
)
from thoth.command.shared.output_format import OutputFormat
from thoth.command.shared.write_output import write_output
from thoth.model.document_model import DocumentModel
from thoth.model.fragments import Fragments
from thoth.utils.iso_639 import is_iso_639_language_code

FORMAT_REQUIRES_OUTPUT = {
    OutputFormat.DOCX,
}


def _notify(message: str) -> None:
    typer.echo(message, err=True)


def _quit_with_message(message: str) -> None:
    _notify(message)
    sys.exit(1)


def determine_format(
    template: Path,
    output: Path | None = None,
    format: OutputFormat | None = None,
) -> OutputFormat:
    determined_format = format or OutputFormat.from_path(template) or OutputFormat.from_path(output)
    if determined_format is None:
        _quit_with_message("need format from '--format', '--output', or '--template'")
    determined_format = determined_format.resolve()  # type: ignore[union-attr]
    if output is None and determined_format in FORMAT_REQUIRES_OUTPUT:
        _quit_with_message(f"please use '--output' to save files of format - {determined_format.value}")
    return determined_format


def check_language_code(value: str):
    if value is not None and not is_iso_639_language_code(value):
        raise typer.BadParameter(f"unknown language code '{value}'")
    return value


def determine_language(
    language: str | None,
    document,
    document_path: Path,
    fragments: Fragments | None,
    fragments_path: Path | None,
) -> str | None:
    document_total_count, document_language_counts = document.count_multi_lingual()
    document_languages = set(document_language_counts.keys())

    if fragments:
        fragments_total_count, fragments_language_counts = fragments.count_multi_lingual()
        fragments_languages = set(fragments_language_counts.keys())
    else:
        fragments_total_count, fragments_language_counts = 0, {}
        fragments_languages = set()

    if not document_languages and not fragments_languages:
        return None

    if document_languages and fragments:
        available_languages = list(sorted(document_languages & fragments_languages))
    else:
        available_languages = list(sorted(document_languages | fragments_languages))

    if document_languages and len(available_languages) == 0:
        _quit_with_message(
            (
                "no language selected, document and fragments do not share languages"
                if fragments
                else "no language selected, document contains no languages"
            )
        )

    if language is None and document_languages and len(available_languages) > 1:
        language_names = [f"'{lang}'" for lang in available_languages]
        languages = (
            " and ".join(language_names)
            if len(language_names) == 2
            else ", ".join(language_names[:-1]) + f", and {language_names[-1]}"
        )
        _quit_with_message(
            (
                f"no language selected, document and fragments contain languages {languages}"
                if fragments
                else f"no language selected, document contains languages {languages}"
            )
        )

    if language is None and available_languages:
        language = available_languages[0]
        _notify(f"NOTE: language '{language}' automatically selected")

    errors: list[str] = []
    warnings: list[str] = []
    if document_languages:
        if language not in document_language_counts:
            errors.append(f"{document_path}")
        elif document_language_counts[language] < document_total_count:
            warnings.append(f"{document_path}")
    if fragments:
        if language not in fragments_language_counts:
            errors.append(f"{fragments_path}")
        elif fragments_language_counts[language] < fragments_total_count:
            warnings.append(f"{fragments_path}")
    if errors:
        _quit_with_message(f"language '{language}' not in - {', '.join(errors)}")
    if warnings:
        _notify(
            f"""
WARNING: language '{language}' incomplete in - {", ".join(warnings)}
     check output for warnings
            """.strip(),
        )

    return language


LANGUAGE_OPTION = Annotated[str | None, typer.Argument(help="language to render", callback=check_language_code)]


def render_document(
    model: DOCUMENT_MODEL_PATH_OPTION,
    path: DOCUMENT_PATH_ARGUMENT,
    template: RENDER_TEMPLATE_PATH_OPTION,
    language: LANGUAGE_OPTION = None,
    fragments: FRAGMENT_PATH_OPTION = None,
    profile: RENDER_PROFILE_PATH_OPTION = None,
    output: OUTPUT_PATH_OPTION = None,
    force: bool = False,
    format: Annotated[OutputFormat | None, typer.Option(help="[default: from --template or --output]")] = None,
) -> None:
    """
    render a document

    Prints a message to help you correct any issue found and "OK" if no issues were found.
    """

    document_model = DocumentModel.from_yaml(model)
    document_class = document_model.create_document_class(model.stem)  # derive document class
    profile_class = document_model.create_profile_class(model.stem)  # derive profile class
    document = document_class.from_yaml(path)  # type: ignore[attr-defined]
    document_profile = profile_class.from_yaml(profile) if profile else profile_class.yes_to_all()  # type: ignore[attr-defined]
    text_fragments = Fragments.from_yaml(fragments) if fragments else None

    language = determine_language(language, document, path, text_fragments, fragments)

    format = determine_format(template, output, format)

    context = {
        "document": document,
        "fragments": text_fragments,
        "language": language,
        "profile": document_profile,
        "source": path.name,
        "timestamp": datetime.now(tz=timezone.utc),
    }

    if format == OutputFormat.TEXT:
        loader = jinja2.FileSystemLoader(template.parent)
        jinja2_template = jinja2.Environment(loader=loader).get_template(template.name)
        rendered = jinja2_template.render(**context)
        write_output(rendered, destination=output, force=force)
    elif format == OutputFormat.DOCX:
        doc = DocxTemplate(template)
        doc.render(context)
        doc.save(output)
