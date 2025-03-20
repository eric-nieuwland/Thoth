# standard library imports

# third party imports

# own imports
from model.norm import Norm
from .html_norm__common import part, part_title
from .html_norm_reference import reference


def references(norm: Norm, language: str) -> list:
    title = part_title("references")
    if not norm.references:
        return [title]

    return part(
        title,
        [reference(ref, language) for ref in norm.references],
    )
