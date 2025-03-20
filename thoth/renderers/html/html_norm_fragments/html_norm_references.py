# standard library imports

# third party imports

# own imports
from model.multi_lingual_text import MultiLingualText
from model.norm import Norm
from model.reference import Reference
from .html_norm__common import multi_lingual_list, part, part_title, sub_part


def _reference_title(reference: Reference, _language: str) -> list[str]:
    return [
        """    <div class="reference">""",
        f"      {reference.name}{'' if not reference.url else f' - <a href="{reference.url}">{reference.url}</a>'}",
        """    </div>""",
    ]


def _notes(notes: list[MultiLingualText], language: str) -> list:
    return multi_lingual_list(notes, language)


def _reference(reference: Reference, language: str) -> list:
    return sub_part(
        _reference_title(reference, language),
        _notes(reference.notes, language),
    )


def _references(references: list[Reference], language: str) -> list:
    return [] if not references else [
        line for reference in references for line in _reference(reference, language)
    ]


def render(norm: Norm, language: str) -> list:
    return part(
        part_title("references"),
        _references(norm.references, language),
    )
