"""
template_mixin - mix-in for Pydantic classes to add the ability to create a template to be rendered with Jinja2
"""

from __future__ import annotations

# standard library
from types import UnionType
from typing import Any, get_args, get_origin

# third party
from pydantic import BaseModel, RootModel

# own
from ..multi_lingual_text import MultiLingualText


class RenderTemplateMixIn:
    """
    mix-in for Pydantic classes to add the ability to create a template to be rendered with Jinja2
    """

    _INDENT_PREFIX = " " * 4

    @classmethod
    def set_indent(cls, indent: int | str) -> None:
        """
        set the indent of ALL rendering templates - not just the class into which this was mixed in
        """
        if isinstance(indent, str):
            RenderTemplateMixIn._INDENT_PREFIX = indent
        elif isinstance(indent, int):
            RenderTemplateMixIn._INDENT_PREFIX = " " * indent
        else:
            raise TypeError(f"cannot set indent to {indent.__class__.__name__}")

    @classmethod
    def indent(cls, text: str | list[str]) -> str | list[str]:
        """
        indent a text or a number of texts
        """
        if isinstance(text, str):
            return "\n".join(f"{cls._INDENT_PREFIX}{line}" for line in text.splitlines())
        if isinstance(text, list):
            return [cls.indent(t) for t in text]
        raise TypeError(f"cannot indent {text.__class__.__name__}")

    @staticmethod
    def singular(plural: str) -> str:
        """simple attempt to turn a plural into a singular"""
        if plural.endswith("ies"):
            return f"{plural[:-3]}y"
        if plural.endswith("s"):
            return plural[:-1]
        return plural

    @staticmethod
    def field_type_base(field) -> tuple[Any, Any]:
        if (origin := get_origin(field.annotation)) is not None:
            return origin, get_args(field.annotation)
        return field.annotation, None

    @classmethod
    def _render_template_from_value(
        cls,
        document_var: str,
        profile_var: str,
        kind,
        base,
        *,
        include_profile_check: bool = True,
    ) -> list[str]:
        head: list[str] = []
        body: list[str] = []
        tail: list[str] = []
        if hasattr(kind, "render_template"):
            body.append(kind.render_template(document_var, profile_var))
        elif kind is UnionType:
            # multiple bases - use first
            if type(None) in base:  # optional value - suppress if absent
                head.append(f"{{% if {document_var} %}}")
                tail.insert(0, f"{{% endif %}}")
                selected_kind = [b for b in base if b is not type(None)][0]
            else:
                selected_kind = base[0]
            body.extend(
                cls._render_template_from_value(
                    document_var, profile_var, selected_kind, None, include_profile_check=False
                )
            )
        elif kind is list and base is not None:
            loop_var = cls.singular(document_var.split(".")[-1])
            head.append(f"{{% for {loop_var} in {document_var} %}}")
            tail.insert(0, f"{{% endfor %}}")
            body.extend(
                cls._render_template_from_value(loop_var, profile_var, base[0], None, include_profile_check=False)
            )
        elif kind is MultiLingualText:
            body.append(f"{{{{ {document_var}[language] }}}}")
        else:
            body.append(f"{{{{ {document_var} }}}}")
        if len(head) > 0 or len(tail) > 0:
            body = cls.indent(body)
        if include_profile_check:
            body = cls.indent(head + body + tail)
            head = [f"{{% if {profile_var} %}}"]
            tail = [f"{{% endif %}}"]
        return head + body + tail

    @classmethod
    def _render_template_from_root_model(cls, document_var: str, profile_var: str) -> list[str]:
        root = cls.model_fields["root"]
        kind, base = cls.field_type_base(root)
        result: list[str] = []
        result.extend(f"{{# no code for rendering template for {document_var}, yet #}}")
        return result

    @classmethod
    def _render_template_from_base_model(cls, document_var: str, profile_var: str) -> list[str]:
        result: list[str] = []
        for field_name, field_def in cls.model_fields.items():
            kind, base = cls.field_type_base(field_def)
            result.extend(
                cls._render_template_from_value(
                    f"{document_var}.{field_name}",
                    f"{profile_var}.{field_name}",
                    kind,
                    base,
                )
            )
        return result

    @classmethod
    def render_template(cls, document_var: str | None = None, profile_var: str | None = None) -> str:
        document_var = document_var or "document"
        profile_var = profile_var or "profile"
        if issubclass(cls, RootModel):
            return "\n".join(cls._render_template_from_root_model(document_var, profile_var))
        if issubclass(cls, BaseModel):
            return "\n".join(cls._render_template_from_base_model(document_var, profile_var))
        raise TypeError(f"cannot create a template for {cls.__name__}")

    def count_multi_lingual_root_model(self, obj) -> tuple[int, dict[str, int]]:
        """
        count the number of multilingual elements and the languages therein
        """
        return 0, {}

    def count_multi_lingual_base_model(self, obj) -> tuple[int, dict[str, int]]:
        """
        count the number of multilingual elements and the languages therein
        """
        result = 0, {}
        for field_name, field_def in obj.model_fields.items():
            kind, base = self.field_type_base(field_def)
            if kind == list:
                result = add_counts(result, self.count_multi_lingual_list(getattr(obj, field_name)))
            else:
                print(f"don't know how to count {kind}")
        return result

    def count_multi_lingual_list(self, lst) -> tuple[int, dict[str, int]]:
        """
        count the number of multilingual elements and the languages therein
        """
        result = 0, {}
        for element in lst:
            if hasattr(element, "count_multi_lingual"):
                result = add_counts(result, element.count_multi_lingual())
            elif isinstance(element, RootModel):
                result = add_counts(result, self.count_multi_lingual_root_model(element))
            elif isinstance(element, BaseModel):
                result = add_counts(result, self.count_multi_lingual_base_model(element))
        return result

    def count_multi_lingual(self) -> tuple[int, dict[str, int]]:
        """
        count the number of multilingual elements and the languages therein
        """
        if isinstance(self, RootModel):
            return self.count_multi_lingual_root_model(self)
        if isinstance(self, BaseModel):
            return self.count_multi_lingual_base_model(self)
        raise TypeError(f"cannot count multilingual elements in {self.__class__.__name__}")


def add_counts(
    a: tuple[int, dict[str, int]],
    b: tuple[int, dict[str, int]],
) -> tuple[int, dict[str, int]]:
    return a[0] + b[0], {key: a[1].get(key, 0) + b[1].get(key, 0) for key in set(a[1]) | set(b[1])}
