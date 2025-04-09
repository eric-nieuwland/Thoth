# standard library imports

# third party imports

# own imports
from model.norm.multi_lingual_text import MultiLingualText

from .html_norm__common import classed_div, multi_lingual_list, part, part_title


def criteria(criteria: list[MultiLingualText], language: str) -> list:
    return classed_div(
        "blue-box",
        *part(
            part_title("criteria"),
            multi_lingual_list(criteria, language),
        )
    )
