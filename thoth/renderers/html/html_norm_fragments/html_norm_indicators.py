# standard library imports

# third party imports

# own imports
from model.norm.indicator import Indicator
from model.profile import profile

from .html_norm__common import part, part_title
from .html_norm_indicator import indicator


def indicators(
    indicators: list[Indicator],
    language: str,
    id_prefix: str,
    prof: profile.IndicatorsRenderProfile | None = None,
) -> list:
    if prof is not None and not prof:
        return []

    title = part_title("indicators")
    if not indicators:
        return [title]

    return part(
        title,
        [indicator(ind, language, id_prefix, prof) for ind in indicators],
    )
