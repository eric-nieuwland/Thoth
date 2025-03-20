# standard library imports

# third party imports

# own imports
from model.driver import Driver
from .html_norm__common import sub_part_title, table, table_row, table_cell


def driver(driver: Driver, _language: str) -> list:
    title = sub_part_title(driver.name)
    if driver.details is None or len(driver.details) == 0:
        return [title]

    return [
        title,
        table(
            *[table_row(table_cell(detail)) for detail in driver.details],
        ),
    ]
