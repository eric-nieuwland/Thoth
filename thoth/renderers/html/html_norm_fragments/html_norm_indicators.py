# standard library imports

# third party imports

# own imports
from model.conformity import Conformity
from model.indicator import Indicator
from model.multi_lingual_text import MultiLingualText
from model.norm import Norm
from .html_norm__common import part, part_title, sub_part, sub_sub_part, sub_sub_part_title, table, table_row, table_cell


def _guidance(guidance: MultiLingualText | None, language: str) -> list:
    return [] if not guidance else table_row(
        table_cell(),
        table_cell(f"<em>{guidance[language]}</em>"),
    )


def _conformity(conformity: Conformity, language: str, id_prefix: str) -> list:
    return [
        table_row(
            table_cell(f"{id_prefix}/{conformity.identifier}"),
            table_cell(conformity.description[language]),
        ),
        _guidance(conformity.guidance, language),
    ]


def _conformities(conformities: list[Conformity], language: str, id_prefix: str) -> list:
    return [] if not conformities else table(
        *[_conformity(conformity, language, id_prefix) for conformity in conformities],
    )


def _explanation(explanation: str) -> list:
    return [
        "<div>",
        explanation,
        "</div>",
    ]


def _indicator(indicator: Indicator, language: str, id_prefix: str) -> list:
    return sub_part(
        """  <div class="indicator-title">""",
        f"""   {indicator.identifier} {indicator.title[language]}""",
        """  </div>""",
        """  <div>""",
        f"""   {indicator.description[language]}""",
        """  </div>""",
        sub_sub_part(
            sub_sub_part_title("Conformity indicators"),
            _conformities(indicator.conformities, language, indicator.identifier),
        ),
        sub_sub_part(
            sub_sub_part_title("Explanation"),
            _explanation(indicator.explanation[language]),
        ),
    )


def _indicators(indicators: list[Indicator], language: str, id_prefix: str) -> list:
    return [] if not indicators else [
        line for indicator in indicators for line in _indicator(indicator, language, id_prefix)
    ]

def render(norm: Norm, language: str) -> list:
    return part(
        part_title("indicators"),
        _indicators(norm.indicators, language, norm.identifier),
    )