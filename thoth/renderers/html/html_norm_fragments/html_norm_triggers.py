# standard library imports

# third party imports

# own imports
from model.norm_definition.multi_lingual_text import MultiLingualText
from .html_norm__common import multi_lingual_list, part, part_title


def triggers(triggers: list[MultiLingualText], language: str) -> list:
    return part(
        part_title("triggers"),
        multi_lingual_list(triggers, language),
    )
