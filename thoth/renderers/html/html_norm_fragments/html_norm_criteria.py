# standard library imports

# third party imports

# own imports
from model.norm.multi_lingual_text import MultiLingualText
from .html_norm__common import multi_lingual_list, part, part_title


def criteria(criteria: list[MultiLingualText], language: str) -> list:
    return part(
        part_title("criteria"),
        multi_lingual_list(criteria, language),
    )
