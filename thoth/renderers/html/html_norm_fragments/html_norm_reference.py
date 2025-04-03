# standard library imports

# third party imports

# own imports
from model.norm.reference import Reference
from .html_norm__common import sub_part
from .html_norm_reference_notes import notes
from .html_norm_reference_title import reference_title


def reference(reference: Reference, language: str) -> list:
    return sub_part(
        reference_title(reference, language),
        notes(reference.notes, language),
    )
