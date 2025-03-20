# standard library imports

# third party imports

# own imports
from model.multi_lingual_text import MultiLingualText
from model.norm import Norm
from .html_norm__common import multi_lingual_list, part, part_title


def _criteria(criteria: list[MultiLingualText], language: str) -> list[str]:
    return multi_lingual_list(criteria, language)


def criteria(norm: Norm, language: str) -> list:
    return part(
        part_title("criteria"),
        _criteria(norm.criteria, language),
    )
