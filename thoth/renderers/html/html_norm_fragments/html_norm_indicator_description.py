# standard library imports

# third party imports

# own imports
from model.multi_lingual_text import MultiLingualText
from .html_norm__common import classed_div


def description(text: MultiLingualText, language: str) -> list:
    return classed_div("sub-sub-part", text[language])
