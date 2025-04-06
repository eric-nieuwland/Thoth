# standard library imports
from enum import Enum
import re

# third party imports

# own imports


class State(Enum):
    OUTSIDE = "outside"
    IN_DRIVERS = "in drivers"
    IN_INDICATORS = "in indicators"
    IN_INDICATOR_CONFORMITIES = "in indicator conformities"
    IN_INDICATOR_EXPLANATION = "in indicator explanation"
    IN_REFERENCES = "in references"


def yaml_norm_layout_enhancer(text: str) -> str:
    """
    produce a nicer version of a norm in YAML form
    """
    state = State.OUTSIDE
    unindented = re.compile("^[a-z]")
    level_1_sep = ""
    level_2_sep = f"# {'=' * 76}"
    level_3_sep = f"  # {'-' * 42}"
    lines = text.splitlines()
    result: list[str] = []
    _dbg_count = 0

    for line in lines:
        if not line:  # include empty lines without further processing
            result.append(line)
            continue

        # inject separators where appropriate
        if state == State.IN_DRIVERS and line.startswith("- name:"):
            result.append(level_1_sep)
        elif state == State.IN_INDICATORS and line.startswith("- identifier:"):
            result.append(level_2_sep)
        elif state == State.IN_INDICATORS and line == "  conformities:":
            result.append(level_1_sep)
        elif state == State.IN_INDICATOR_CONFORMITIES and line.startswith("  - identifier:"):
            result.append(level_3_sep)
        elif state == State.IN_INDICATOR_CONFORMITIES and line == "  explanation:":
            result.append(level_3_sep)
            result.append(level_1_sep)
        elif state == State.IN_INDICATOR_EXPLANATION and line.startswith("- identifier:"):
            result.append(level_2_sep)
        elif state == State.IN_INDICATOR_EXPLANATION and line == "references:":
            result.append(level_2_sep)
        elif state == State.IN_REFERENCES and line.startswith("- name:"):
            result.append(level_1_sep)

        # change state
        if state == State.OUTSIDE and line == "drivers:":
            state = State.IN_DRIVERS
        elif state == State.IN_DRIVERS and line == "indicators:":
            state = State.IN_INDICATORS
        elif state == State.IN_INDICATORS and line == "  conformities:":
            state = State.IN_INDICATOR_CONFORMITIES
        elif state == State.IN_INDICATOR_CONFORMITIES and line == "  explanation:":
            state = State.IN_INDICATOR_EXPLANATION
        elif state == State.IN_INDICATOR_EXPLANATION and line.startswith("- identifier:"):
            state = State.IN_INDICATORS
        elif state == State.IN_INDICATOR_EXPLANATION and line == "references:":
            state = State.IN_REFERENCES

        # suppress unnecessary output
        if state == State.IN_DRIVERS and line == "  details: null":
            continue
        if state == State.IN_INDICATOR_CONFORMITIES and line == "    guidance: null":
            continue
        if state == State.IN_REFERENCES and line == "  notes: null":
            continue

        if unindented.match(line) and result:  # separate from preceding
            result.append(level_1_sep)

        result.append(line)

    return "\n".join(result)
