# standard library imports

# third party imports

# own imports
from model.multi_lingual_text import MultiLingualText
from model.norm import Norm
from .html_norm__common import multi_lingual_list, part, part_title


def _objectives(objectives: list[MultiLingualText], language: str) -> list:
    return multi_lingual_list(objectives, language)


def render(norm: Norm, language: str) -> list:
    return part(
        part_title("objectives"),
        _objectives(norm.objectives, language),
    )
