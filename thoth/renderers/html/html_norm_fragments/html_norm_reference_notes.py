# standard library imports

# third party imports

# own imports
from model.norm.multi_lingual_text import MultiLingualText
from .html_norm__common import multi_lingual_list


def notes(notes: list[MultiLingualText], language: str) -> list:
    return multi_lingual_list(notes, language)
