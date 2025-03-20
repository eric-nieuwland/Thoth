# standard library imports
from typing import Self

# third party imports
from pydantic import RootModel, model_validator


__all__ = [
    "MultiLingualText",
]


__LANGUAGE_CODES__ = {
    # TODO: this should come from the outside, e.g. the configuration
    "en",
    "nl",
}


class MultiLingualText(RootModel):
    """
    A text string in several languages
    """
    root: dict[str, str]

    @model_validator(mode="after")
    def check_values(self) -> Self:
        for key in self.root:
            self.__check_language_code__(key)
        return self

    @staticmethod
    def __check_language_code__(code: str):
        if code not in __LANGUAGE_CODES__:
            raise ValueError(f"'{code}' is not a valid language code")

    def __str__(self):
        return f"""<T|{
            "; ".join(f"'{language}': '{text}'" for language, text in sorted(self.root.items()))
        }|T>""".strip()

    def __repr__(self):
        texts = "".join(f"\n  |{language}| '{text}'" for language, text in sorted(self.root.items()))
        return f"""<{self.__class__.__name__}:{"".join(texts)}{"\n" if texts else ""}>""".strip()

    def __getitem__(self, language: str) -> str:
        return self.root.get(
            language,
            f"""WARNING: text not available in '{language}'; text available in {
                ", ".join(f"'{lang}'" for lang in sorted(self.root.keys()))
            }""",
        ).strip()

    def __setitem__(self, language: str, text: str):
        self.__check_language_code__(language)
        if language in self.root:
            raise KeyError(f"Text for '{language}' already set to '{self.root[language]}'")
        self.root[language] = text

    # multi-lingual

    def count_multi_lingual(self) -> tuple[int, dict[str, int]]:
        return 1, {language: 1 for language in self.root}

    # template / example

    @classmethod
    def lorem_ipsum(cls) -> Self:
        return cls(
            root={
                "en": "Lorem ipsum odor amet, consectetuer adipiscing elit.",
                "nl": "Ut odio quis primis tortor phasellus nisl aptent auctor a.",
            }
        )
