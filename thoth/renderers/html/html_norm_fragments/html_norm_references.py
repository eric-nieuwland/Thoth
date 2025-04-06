# standard library imports

# third party imports

# own imports
from model.norm.reference import Reference
from model.profile import profile
from .html_norm__common import part, part_title
from .html_norm_reference import reference


def references(
    references: list[Reference] | None,
    language: str,
    prof: profile.References | None = None,
) -> list:
    if prof is not None and not prof:
        return []

    title = part_title("references")
    if not references:
        return [title]

    return part(
        title,
        [reference(ref, language, prof) for ref in references],
    )
