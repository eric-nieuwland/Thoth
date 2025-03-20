# standard library imports

# third party imports

# own imports
from model.norm import Norm
from . import html_norm_criteria
from . import html_norm_drivers
from . import html_norm_indicators
from . import html_norm_intro
from . import html_norm_objectives
from . import html_norm_references
from . import html_norm_risks
from . import html_norm_scope
from . import html_norm_title
from . import html_norm_triggers


def render(norm: Norm, language: str) -> list:
    return [
        html_norm_title.render(norm, language),
        html_norm_intro.render(norm, language),
        html_norm_scope.render(norm, language),
        html_norm_triggers.render(norm, language),
        html_norm_criteria.render(norm, language),
        html_norm_objectives.render(norm, language),
        html_norm_risks.render(norm, language),
        html_norm_drivers.render(norm, language),
        html_norm_indicators.render(norm, language),
        html_norm_references.render(norm, language),
    ]
