# standard library imports

# third party imports

# own imports
from model.norm.multi_lingual_text import MultiLingualText

from .html_norm__common import classed_div, multi_lingual_list, part, part_title


def risks(risks: list[MultiLingualText], language: str) -> list:
    return classed_div(
        "blue-box",
        *part(
            part_title("risks"),
            multi_lingual_list(risks, language),
        )
    )
