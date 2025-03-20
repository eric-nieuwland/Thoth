# standard library imports

# third party imports

# own imports
from model.driver import Driver
from model.norm import Norm
from .html_norm__common import part, part_title, sub_part, sub_part_title, table, table_row, table_cell


def _details(details: list[str] | None) -> list:
    if details is None or len(details) == 0:
        return []
    return table(
        *[
            table_row(table_cell(detail)) for detail in details
        ],
    )


def _driver(driver: Driver, _language: str, width: int, nr: int) -> list:
    return [
        f"""<td width="{"*" if nr == 0 else f"{width}%"}">""",
        sub_part_title(driver.name),
        _details(driver.details),
        """</td>""",
    ]


def _drivers(drivers: list[Driver] | None, language: str) -> list:
    if drivers is None or len(drivers) == 0:
        return []
    width = 100 // len(drivers)
    return sub_part(
        """  <table width="100%">""",
        """    <tr>""",
        [_driver(driver, language, width, nr) for nr, driver in enumerate(drivers)],
        """    </tr>""",
        """  </table>""",
    )


def render(norm: Norm, language: str) -> list:
    return part(
        part_title("drivers"),
        _drivers(norm.drivers, language),
    )