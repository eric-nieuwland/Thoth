# standard library imports

# third party imports

# own imports


__DEFAULT_LANGUAGE__ = "en"

__TEMPLATE_TEXT__ = {
    "en": "|[ please fill with text ]|",
    "nl": "|[ vul hier tekst in ]|",
}


def select_template_text[T](
    code: str,
    templates: dict[str, T],
) -> T:
    return templates[code if code in templates else __DEFAULT_LANGUAGE__]


def template_text(code: str) -> str:
    return select_template_text(code, __TEMPLATE_TEXT__)
