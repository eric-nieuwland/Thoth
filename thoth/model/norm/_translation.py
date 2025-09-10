# standard library imports

# third party imports

# own imports
from .._translation import select_template_text

__TEMPLATE_DRIVER_TEXT__ = {
    "en": (
        "|[ please name driver ]|",
        "|[ driver detail #{nr} ]|",
    ),
    "nl": (
        "|[ noem driver ]|",
        "|[ driver detail #{nr} ]|",
    ),
}

__TEMPLATE_REFERENCE_TEXT__ = {
    "en": "|[ please name reference ]|",
    "nl": "|[ noem referentie ]|",
}


def template_driver_text(code: str) -> tuple[str, str]:
    return select_template_text(code, __TEMPLATE_DRIVER_TEXT__)


def template_reference_text(code: str) -> str:
    return select_template_text(code, __TEMPLATE_REFERENCE_TEXT__)
