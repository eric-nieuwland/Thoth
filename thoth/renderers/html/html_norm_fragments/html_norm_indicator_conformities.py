# standard library imports

# third party imports

# own imports
from model.norm.conformity import Conformity
from model.profile import profile
from .html_norm__common import sub_sub_part, sub_sub_part_title, table, table_row, table_cell


def conformities(
    conformities: list[Conformity],
    language: str,
    id_prefix: str,
    prof: profile.Conformities | None = None,
) -> list:
    if prof is not None and not prof:
        return []

    title = sub_sub_part_title("Conformity indicators")
    if not conformities:
        return sub_sub_part(title)

    return sub_sub_part(
        title,
        table(
            *[
                [
                    table_row(
                        table_cell(
                            f"{id_prefix}/{conformity.identifier}"
                            if prof is None or prof.identifier
                            else ""
                        ),
                        table_cell(
                            conformity.description[language]
                            if prof is None or prof.description
                            else ""
                        ),
                    ),
                    []
                    if not conformity.guidance or (prof is not None and not prof.guidance)
                    else table_row(
                        table_cell(),
                        table_cell(f"<em>{conformity.guidance[language]}</em>"),
                    ),
                ]
                for conformity in conformities
            ],
        ),
    )
