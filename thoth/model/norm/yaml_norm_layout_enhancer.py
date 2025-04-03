# standard library imports
from enum import Enum
import re

# third party imports

# own imports


class State(Enum):
    OUTSIDE = "outside"
    IN_DRIVERS = "in drivers"
    IN_INDICATORS = "in indicators"
    IN_INDICATOR_CONFORMATIES = "in indicator conformaties"
    IN_INDICATOR_EXPLANATION = "in indicator explanation"
    IN_REFERENCES = "in references"

def yaml_norm_layout_enhancer(text: str) -> str:
    """
    produce a nicer version of a norm in YAML form
    """
    state = State.OUTSIDE
    unindented = re.compile("^[a-z]")
    indicator_sep = "=" * 76
    conformity_sep = "-" * 42
    lines = text.splitlines()
    result = []
    _dbg_count = 0
    for line in lines:

        if not line:  # empty line
            result.append(line)
            continue

        if state == State.IN_DRIVERS and line.startswith("- name:"):
            result.append("")
        elif state == State.IN_INDICATORS and line.startswith("- identifier:"):
            result.append(f"# {indicator_sep}")
        elif state == State.IN_INDICATOR_CONFORMATIES and line.startswith("  - identifier:"):
            result.append(f"  # {conformity_sep}")
        elif state == State.IN_REFERENCES and line.startswith("- name:"):
            result.append("")

        if state == State.OUTSIDE and line == "drivers:":
            state = State.IN_DRIVERS
        elif state == State.IN_DRIVERS and line == "indicators:":
            state = State.IN_INDICATORS
        elif state == State.IN_INDICATORS and line == "  conformities:":
            state = State.IN_INDICATOR_CONFORMATIES
            result.append("")
        elif state == State.IN_INDICATOR_CONFORMATIES and line == "  explanation:":
            state = State.IN_INDICATOR_EXPLANATION
            result.append(f"  # {conformity_sep}")
            result.append("")
        elif state == State.IN_INDICATOR_EXPLANATION and line.startswith("- identifier:"):
            state = State.IN_INDICATORS
            result.append(f"# {indicator_sep}")
        elif state == State.IN_INDICATOR_EXPLANATION and line == "references:":
            state = State.IN_REFERENCES
            result.append(f"# {indicator_sep}")

        if state == State.IN_DRIVERS and line == "  details: null":
            continue
        if state == State.IN_INDICATOR_CONFORMATIES and line == "    guidance: null":
            continue
        if state == State.IN_REFERENCES and line == "  notes: null":
            continue

        if unindented.match(line) and result:  # separate from preceding
            result.append("")

        result.append(line)

    return "\n".join(result)
