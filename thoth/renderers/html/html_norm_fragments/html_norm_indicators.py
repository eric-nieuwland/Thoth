# standard library imports

# third party imports

# own imports
from model.norm_definition.indicator import Indicator
from .html_norm__common import part, part_title
from .html_norm_indicator import indicator


def indicators(indicators: list[Indicator], language: str, id_prefix: str) -> list:
    title = part_title("indicators")
    if not indicators:
        return [title]

    return part(
        title,
        [indicator(ind, language, id_prefix) for ind in indicators],
    )
