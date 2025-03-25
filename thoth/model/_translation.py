# standard library imports

# third party imports

# own imports


__DEFAULT_LANGUAGE__ = "en"

__TEMPLATE_TEXT__ = {
    "en": "|[ please fill with text ]|",
    "nl": "|[ vul hier tekst in ]|",
}

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


def _select_template_text(code: str, templates: dict, default_code: str):
    return templates[code if code in templates else default_code]


def template_text(code: str) -> str:
    return _select_template_text(code, __TEMPLATE_TEXT__, __DEFAULT_LANGUAGE__)


def template_driver_text(code: str) -> str:
    return _select_template_text(code, __TEMPLATE_DRIVER_TEXT__, __DEFAULT_LANGUAGE__)


def template_reference_text(code: str) -> str:
    return _select_template_text(code, __TEMPLATE_REFERENCE_TEXT__, __DEFAULT_LANGUAGE__)
