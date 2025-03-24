# standard library imports

# third party imports

# own imports
from model.driver import Driver
from .html_norm__common import part, part_title, sub_part
from .html_norm_driver import driver


def _equal_width_horizontal_layout(elements: list) -> list:
    if len(elements) == 0:
        return []
    width = 100 // len(elements)
    return [
        """<table width="100%">""",
        "  <tr>",
        [
            [
                f"""    <td width="{"*" if nr == 0 else f"{width}%"}">""",
                element,
                """    </td>""",
            ]
            for nr, element in enumerate(elements)
        ],
        "  </tr>",
        "</table>",
    ]


def drivers(drivers: list[Driver] | None, language: str) -> list:
    title = part_title("drivers")
    if drivers is None or len(drivers) == 0:
        return [title]

    return part(
        title,
        _equal_width_horizontal_layout(
            [
                driver(drvr, language) for nr, drvr in enumerate(drivers)
            ]
        ),
    )
