# standard library imports

# third party imports

# own imports
from model.norm.reference import Reference
from model.profile import profile
from .html_norm__common import sub_part
from .html_norm_reference_notes import notes
from .html_norm_reference_title import reference_title


def reference(reference: Reference, language: str, prof: profile.References | None = None) -> list:
    if prof is not None and not prof:
        return []

    return sub_part(
        reference_title(reference, language, prof),
        notes(reference.notes, language) if prof is None or prof.notes else "",
    )
