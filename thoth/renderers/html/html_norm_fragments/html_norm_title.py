# standard library imports

# third party imports

# own imports
from model.norm.norm import Norm
from .html_norm__common import classed_div


def title(norm: Norm, language: str) -> list[str]:
    return classed_div("norm-title", f"{norm.identifier} - {norm.title[language]}")
