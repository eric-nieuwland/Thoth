# standard library imports
from itertools import zip_longest

# third party imports
# own imports
from thoth.model.norm.conformity import Conformity
from thoth.model.norm.driver import Driver
from thoth.model.norm.indicator import Indicator
from thoth.model.norm.norm import Norm
from thoth.utils.flatten import flatten


def _x_difference(what: str, v1, v2) -> list:
    return [f"{what}: {v1} <-> {v2}"] if v1 != v2 else []


def _x_identifier(id1: str, id2: str) -> list:
    return _x_difference("identifier", id1, id2)


def _x_drivers(
    drivers1: list[Driver] | None,
    drivers2: list[Driver] | None,
) -> list:
    if drivers1 is None:
        drivers1 = []
    if drivers2 is None:
        drivers2 = []
    return [_x_difference("driver", d1, d2) for d1, d2 in zip_longest(drivers1, drivers2, fillvalue="--")]


def _x_conformity(
    conformity1: Conformity | None,
    conformity2: Conformity | None,
) -> list:
    what = "  conformity/identifier"
    if conformity1 is None and conformity2 is None:
        return []
    if conformity1 is None:
        return _x_difference(what, "--", conformity2.identifier)  # type: ignore
    if conformity2 is None:
        return _x_difference(what, conformity1.identifier, "--")
    return _x_difference(what, conformity1.identifier, conformity2.identifier)


def _x_conformities(
    conformities1: list[Conformity],
    conformities2: list[Conformity],
) -> list:
    return [_x_conformity(d1, d2) for d1, d2 in zip_longest(conformities1, conformities2, fillvalue=None)]


def _x_indicator(
    indicator1: Indicator | None,
    indicator2: Indicator | None,
) -> list:
    what = "indicator/identifier"
    if indicator1 is None and indicator2 is None:
        return []
    if indicator1 is None:
        return _x_difference(what, "--", indicator2.identifier)  # type: ignore
    if indicator2 is None:
        return _x_difference(what, indicator1.identifier, "--")
    return [
        _x_difference(what, indicator1.identifier, indicator2.identifier),
        _x_conformities(indicator1.conformities, indicator2.conformities),
    ]


def _x_indicators(indicators1: list[Indicator], indicators2: list[Indicator]) -> list:
    return [_x_indicator(d1, d2) for d1, d2 in zip_longest(indicators1, indicators2, fillvalue=None)]


def compare_norm_structures(norm1: Norm, norm2: Norm) -> list:
    """
    check whether two norm structures match
    """
    return flatten(  # type: ignore[return-value]
        [
            _x_identifier(norm1.identifier, norm2.identifier),
            _x_drivers(norm1.drivers, norm2.drivers),
            _x_indicators(norm1.indicators, norm2.indicators),
        ]
    )
