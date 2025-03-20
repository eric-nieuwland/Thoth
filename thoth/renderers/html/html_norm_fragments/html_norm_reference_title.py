# standard library imports

# third party imports

# own imports
from model.reference import Reference
from .html_norm__common import classed_div


def reference_title(reference: Reference, _language: str) -> list[str]:
    return classed_div(
        "reference",
        f"{reference.name}{'' if not reference.url else f' - <a href="{reference.url}">{reference.url}</a>'}",
    )
