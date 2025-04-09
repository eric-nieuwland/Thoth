# standard library imports

# third party imports

# own imports
from model.norm.driver import Driver
from model.profile import profile

from .html_norm__common import sub_part_title, table, table_cell, table_row


def driver(
    driver: Driver,
    _language: str,
    prof: profile.DriversRenderProfile | None = None,
) -> list:
    title = sub_part_title(driver.name) if not prof or prof.name else ""
    if driver.details is None or len(driver.details) == 0:
        return [title]
    if prof and not prof.details:
        return [title]

    return [
        title,
        table(
            klass="driver-table",
            *[table_row(table_cell(detail)) for detail in driver.details],
        ),
    ]
