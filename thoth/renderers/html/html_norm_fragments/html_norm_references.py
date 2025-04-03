# standard library imports

# third party imports

# own imports
from model.norm.reference import Reference
from .html_norm__common import part, part_title
from .html_norm_reference import reference


def references(references: list[Reference] | None, language: str) -> list:
    title = part_title("references")
    if not references:
        return [title]

    return part(
        title,
        [reference(ref, language) for ref in references],
    )
