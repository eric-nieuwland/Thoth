# standard library imports

# third party imports

# own imports
from model.norm import Norm
from .html_norm__common import part, part_title, sub_part
from .html_norm_driver import driver


def drivers(norm: Norm, language: str) -> list:
    title = part_title("drivers")
    if norm.drivers is None or len(norm.drivers) == 0:
        return [title]

    width = 100 // len(norm.drivers)
    return part(
        title,
        sub_part(
            """<table width="100%">""",
            "  <tr>",
            [
                [
                    f"""    <td width="{"*" if nr == 0 else f"{width}%"}">""",
                    driver(drvr, language),
                    """    </td>""",
                ]
                for nr, drvr in enumerate(norm.drivers)
            ],
            "  </tr>",
            "</table>",
        ),
    )
