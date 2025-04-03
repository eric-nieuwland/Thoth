# standard library imports

# third party imports

# own imports
from model.norm.multi_lingual_text import MultiLingualText
from .html_norm__common import sub_sub_part, sub_sub_part_title


def explanation(text: MultiLingualText, language: str) -> list:
    return sub_sub_part(
        sub_sub_part_title("Explanation"),
        text[language],
    )
