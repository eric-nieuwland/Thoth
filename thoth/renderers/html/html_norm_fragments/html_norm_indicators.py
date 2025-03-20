# standard library imports

# third party imports

# own imports
from model.norm import Norm
from .html_norm__common import part, part_title
from .html_norm_indicator import indicator


def indicators(norm: Norm, language: str) -> list:
    title = part_title("indicators")
    if not norm.indicators:
        return [title]

    return part(
        title,
        [indicator(ind, language, norm.identifier) for ind in norm.indicators],
    )
