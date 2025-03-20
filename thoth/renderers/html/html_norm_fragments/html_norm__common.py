# standard library imports

# third party imports

# own imports
from model.multi_lingual_text import MultiLingualText


# lists

def multi_lingual_list(texts: list[MultiLingualText], language: str) -> list:
    return [] if not texts else mono_lingual_list([text[language] for text in texts])


def mono_lingual_list(texts: list[str]) -> list:
    return [] if not texts else [
        """<ul>""",
        [f"<li>{text}</li>" for text in texts],
        """</ul>""",
    ]


# divs

def classed_div(div_class: str, *lst: str) -> list:
    return [
        f"""<div class="{div_class}">""" if div_class else "<div>",
        lst,
        f"""</div>""",
    ]

def title_div(div_class: str, title:str) -> list[str]:
    return classed_div(div_class, f"<p>{title}</p>")


# parts

def part(*lst) -> list:
    return classed_div("part", *lst)


def part_title(title: str) -> list:
    return title_div("part-title", title)


def sub_part(*lst) -> list:
    return classed_div("sub-part", *lst)


def sub_part_title(title: str) -> list:
    return title_div("sub-part-title", title)


def sub_sub_part(*lst) -> list:
    return classed_div("sub-sub-part", *lst)


def sub_sub_part_title(title: str) -> list:
    return title_div("sub-sub-part-title", title)


# tables

def table(*rows) -> list:
    return [
        "<table>",
        rows,
        "</table>",
    ]


def table_row(*cells) -> list:
    return [
        "<tr>",
        cells,
        "</tr>",
    ]


def table_cell(*content) -> list:
    if len(content) == 0:
        return ["<td/>"]
    return [
        "<td>",
        content,
        "</td>",
    ]
