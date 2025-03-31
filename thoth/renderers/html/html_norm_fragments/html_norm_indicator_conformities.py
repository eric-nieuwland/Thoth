# standard library imports

# third party imports

# own imports
from model.norm_definition.conformity import Conformity
from .html_norm__common import sub_sub_part, sub_sub_part_title, table, table_row, table_cell


def conformities(conformities: list[Conformity], language: str, id_prefix: str) -> list:
    title = sub_sub_part_title("Conformity indicators")
    if not conformities:
        return sub_sub_part(title)

    return sub_sub_part(
        title,
        table(
            *[
                [
                    table_row(
                        table_cell(f"{id_prefix}/{conformity.identifier}"),
                        table_cell(conformity.description[language]),
                    ),
                    [] if not conformity.guidance else table_row(
                        table_cell(),
                        table_cell(f"<em>{conformity.guidance[language]}</em>"),
                    ),
                ]
                for conformity in conformities
            ],
        ),
    )
