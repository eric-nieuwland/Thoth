# standard library imports

# third party imports

# own imports
from model.norm.indicator import Indicator
from model.profile import profile
from .html_norm__common import sub_part, title_div
from .html_norm_indicator_conformities import conformities
from .html_norm_indicator_description import description
from .html_norm_indicator_explanation import explanation


def indicator(indicator: Indicator, language: str, _id_prefix: str, prof: profile.Indicators | None = None) -> list:
    if prof is not None and not prof:
        return []

    identifier = indicator.identifier if prof is None or prof.identifier else ""
    title = indicator.title[language] if prof is None or prof.title else ""
    title_ = title_div("indicator-title", f"{identifier} {title}") if identifier or title else ""
    return sub_part(
        title_,
        description(indicator.description, language) if prof is None or prof.description else "",
        conformities(indicator.conformities, language, indicator.identifier, None if prof is None else prof.conformities),
        explanation(indicator.explanation, language) if prof is None or prof.explanation else "",
    )
