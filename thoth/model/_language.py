# standard library imports

# third party imports

# own imports


__LANGUAGE_CODES__ = {
    # TODO: this should come from the outside, e.g. the configuration
    "en",
    "nl",
}


def is_known_language(code: str) -> bool:
    # return code in __LANGUAGE_CODES__
    return len(code) == 2


def known_language_or_error(code: str) -> None:
    if not is_known_language(code):
        raise ValueError(f"'{code}' is not a known language code")
