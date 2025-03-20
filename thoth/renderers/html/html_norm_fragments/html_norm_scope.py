# standard library imports

# third party imports

# own imports
from model.norm import Norm
from .html_norm__common import part, part_title


def scope(norm: Norm, language: str) -> list:
    return part(
        part_title("scope"),
        norm.scope[language],
    )
