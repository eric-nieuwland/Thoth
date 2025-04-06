# standard library imports

# third party imports

# own imports
from model.norm.reference import Reference
from model.profile import profile
from .html_norm__common import classed_div


def reference_title(
    reference: Reference,
    _language: str,
    prof: profile.ReferencesRenderProfile | None = None,
) -> list[str]:
    name = reference.name if prof is None or prof.name else ""
    url = reference.url if reference.url and (prof is None or prof.url) else ""
    if not name and not url:
        return []

    return classed_div(
        "reference",
        f"{name}{'' if not url else f' - <a href="{url}">{url}</a>'}",
    )
