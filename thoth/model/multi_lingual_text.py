# standard library imports
from __future__ import annotations
from typing import Self

# third party imports
from pydantic import RootModel, model_validator

# own imports
from ._language import known_language_or_error, template_text


class MultiLingualText(RootModel):
    """
    A text string in several languages
    """
    root: dict[str, str]

    @model_validator(mode="after")
    def check_values(self) -> Self:
        for key in self.root:
            known_language_or_error(key)
        for key, value in self.root.items():
            self.root[key] = " ".join(line.strip() for line in value.splitlines())
        return self

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
        known_language_or_error(language)
        if language in self.root:
            raise KeyError(f"Text for '{language}' already set to '{self.root[language]}'")
        self.root[language] = text

    # multi-lingual

    def count_multi_lingual(self) -> tuple[int, dict[str, int]]:
        return 1, {language: 1 for language in self.root}

    # split/merge

    def copy_for_language(self, *languages: str) -> Self:
        """
        A version of this text, restricted in languages
        """
        return self.__class__(
            {
                language: self.root.get(language, template_text(language))
                for language in languages
            }
        )

    def __or__(self, other: Self) -> Self:
        return self.join(self, other)

    @classmethod
    def join(cls, text1: MultiLingualText, text2: MultiLingualText) -> MultiLingualText:
        if len(set(text1.root) & set(text2.root)) > 0:
            raise ValueError("language overlap")
        # keep languages in alphabetical order
        return cls(root=dict(sorted([*text1.root.items(), *text2.root.items()])))

    # template / example

    @classmethod
    def template(cls, language: str) -> Self:
        return cls(
            root={
                language: template_text(language),
            }
        )
