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


def norm(norm: Norm, language: str) -> list:
    return [
        html_norm_title.title(norm, language),
        html_norm_intro.intro(norm, language),
        html_norm_scope.scope(norm, language),
        html_norm_triggers.triggers(norm.triggers, language),
        html_norm_criteria.criteria(norm.criteria, language),
        html_norm_objectives.objectives(norm.objectives, language),
        html_norm_risks.risks(norm.risks, language),
        html_norm_drivers.drivers(norm.drivers, language),
        html_norm_indicators.indicators(norm.indicators, language, norm.identifier),
        html_norm_references.references(norm.references, language),
    ]
