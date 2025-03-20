# standard library imports

# third party imports

# own imports
from model.indicator import Indicator
from .html_norm__common import sub_part, sub_sub_part, sub_sub_part_title
from .html_norm_indicator_conformities import conformities
from .html_norm_indicator_description import description
from .html_norm_indicator_explanation import explanation


def indicator(indicator: Indicator, language: str, _id_prefix: str) -> list:
    title = [
        """<div class="indicator-title">""",
        f"""  {indicator.identifier} {indicator.title[language]}""",
        """</div>""",
    ]
    return sub_part(
        title,
        description(indicator.description, language),
        conformities(indicator.conformities, language, indicator.identifier),
        explanation(indicator.explanation, language),
    )
