from __future__ import annotations

# standard library

# third party
from pydantic import RootModel

# own
from .mixins import YamlMixIn
from .multi_lingual_text import MultiLingualText, count_multi_lingual_add, count_multi_lingual_init


class Fragments(YamlMixIn, RootModel):
    root: dict[str, MultiLingualText | Fragments]

    def __getitem__(self, key: str) -> MultiLingualText | Fragments:
        """
        convenience method to bypass the need to mention 'root' and allow direct access to content
        """
        return self.root[key]

    def count_multi_lingual(self) -> tuple[int, dict[str, int]]:
        """
        count the number of multilingual elements and the languages therein
        """
        result: tuple[int, dict[str, int]] = count_multi_lingual_init()
        for element in self.root.values():
            if not hasattr(element, "count_multi_lingual"):
                raise RuntimeError(f"unexpected element {element!r} without 'count_multi_lingual'")
            result = count_multi_lingual_add(result, element.count_multi_lingual())
        return result
