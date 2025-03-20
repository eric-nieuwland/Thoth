# standard library imports

# third party imports

# own imports
from model.multi_lingual_text import MultiLingualText


def description(text: MultiLingualText, language: str) -> list:
    return [
        "<div>",
        text[language],
        "</div>",
    ]
