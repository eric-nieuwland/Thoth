# standard library imports

# third party imports

# own imports
from model.norm.norm import Norm
from model.profile import profile
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


def norm(norm: Norm, language: str, prof: profile.Profile | None = None) -> list:
    return [
        html_norm_title.title(norm, language) if not prof or prof.title else "",
        html_norm_intro.intro(norm, language) if not prof or prof.intro else "",
        html_norm_scope.scope(norm, language) if not prof or prof.scope else "",
        html_norm_triggers.triggers(norm.triggers, language) if not prof or prof.triggers else "",
        html_norm_criteria.criteria(norm.criteria, language) if not prof or prof.criteria else "",
        (
            html_norm_objectives.objectives(norm.objectives, language)
            if not prof or prof.objectives
            else ""
        ),
        html_norm_risks.risks(norm.risks, language) if not prof or prof.risks else "",
        html_norm_drivers.drivers(
            norm.drivers,
            language,
            None if prof is None else prof.drivers,
        ),
        html_norm_indicators.indicators(
            norm.indicators,
            language,
            norm.identifier,
            None if prof is None else prof.indicators,
        ),
        html_norm_references.references(
            norm.references,
            language,
            None if prof is None else prof.references,
        ),
    ]
