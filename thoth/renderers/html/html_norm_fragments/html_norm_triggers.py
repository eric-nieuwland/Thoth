# standard library imports

# third party imports

# own imports
from model.multi_lingual_text import MultiLingualText
from model.norm import Norm
from .html_norm__common import multi_lingual_list, part, part_title


def _triggers(triggers: list[MultiLingualText], language: str) -> list:
    return multi_lingual_list(triggers, language)


def triggers(norm: Norm, language: str) -> list:
    return part(
        part_title("triggers"),
        _triggers(norm.triggers, language),
    )
