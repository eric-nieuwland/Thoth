# standard library imports

# third party imports

# own imports
from model.multi_lingual_text import MultiLingualText
from model.norm import Norm
from .html_norm__common import multi_lingual_list, part, part_title


def _risks(risks: list[MultiLingualText], language: str) -> list:
    return multi_lingual_list(risks, language)


def risks(norm: Norm, language: str) -> list:
    return part(
        part_title("risks"),
        _risks(norm.risks, language),
    )
