# standard library imports
from itertools import zip_longest

# third party imports

# own imports
from model.norm.conformity import Conformity
from model.norm.driver import Driver
from model.norm.indicator import Indicator
from model.norm.multi_lingual_text import MultiLingualText, template_text
from model.norm.norm import Norm
from utils.flatten import flatten

from .norm_dimensions import NormDimensions


def _add_missing_languages(norm: Norm, missing: list[str]) -> None:
    for lang in missing:
        lang_text = template_text(lang)
        for mlt in (
            norm.title,
            norm.intro,
            norm.scope,
            *norm.triggers,
            *norm.criteria,
            *norm.objectives,
            *norm.risks,
            *[indicator.title for indicator in norm.indicators],
            *[indicator.description for indicator in norm.indicators],
            *[
                conformity.description
                for indicator in norm.indicators
                for conformity in indicator.conformities
            ],
            *[
                conformity.guidance
                for indicator in norm.indicators
                for conformity in indicator.conformities
                if conformity.guidance is not None
            ],
            *[
                note
                for reference in (norm.references if norm.references else [])
                for note in (reference.notes if reference.notes else [])
            ],
        ):
            mlt.setdefault(lang,lang_text)


def _add_missing_triggers(norm: Norm, missing: int, languages: list[str]) -> None:
    if missing < 1:
        return
    trigger = MultiLingualText(root={lang: template_text(lang) for lang in languages})
    norm.triggers.extend([trigger] * missing)


def _add_missing_criteria(norm: Norm, missing: int, languages: list[str]) -> None:
    if missing < 1:
        return
    criterium = MultiLingualText(root={lang: template_text(lang) for lang in languages})
    norm.criteria.extend([criterium] * missing)


def _add_missing_objectives(norm: Norm, missing: int, languages: list[str]) -> None:
    if missing < 1:
        return
    objective = MultiLingualText(root={lang: template_text(lang) for lang in languages})
    norm.objectives.extend([objective] * missing)


def _add_missing_risks(norm: Norm, missing: int, languages: list[str]) -> None:
    if missing < 1:
        return
    risk = MultiLingualText(root={lang: template_text(lang) for lang in languages})
    norm.risks.extend([risk] * missing)


def _add_missing_drivers(norm: Norm, missing: dict[str, list[str]]) -> None:
    norm.drivers.extend(Driver(name=name, details=details) for name, details in missing.items())


def _add_missing_indicators(norm: Norm, missing: list[int], languages: list[str]) -> None:
    multi_lingual_text = MultiLingualText(root={lang: template_text(lang) for lang in languages})
    indicators = [
        Indicator(
            identifier=f"ID {nr + 1}",
            title=multi_lingual_text,
            description=multi_lingual_text.description,
            conformities=missing[nr],
            explanation=multi_lingual_text,
        )
        for nr in range(len(missing))
    ]
    norm.indicators.extend(indicators)


def _add_missing_references(norm: Norm, missing: int, languages: list[str]s) -> None:
    pass


def _adjust_norm(norm: Norm, missing: NormDimensions, languages: list[str]) -> None:
    _add_missing_languages(norm, missing.languages)
    _add_missing_triggers(norm, missing.triggers, languages)
    _add_missing_criteria(norm, missing.criteria, languages)
    _add_missing_objectives(norm, missing.objectives, languages)
    _add_missing_risks(norm, missing.risks, languages)
    _add_missing_drivers(norm, missing.drivers)
    _add_missing_indicators(norm, missing.indicators, languages)
    _add_missing_references(norm, missing.references, languages)


def equalize_norm_structures(norm1: Norm, norm2: Norm) -> None:
    """
    amend both norms so that they have the same structure
    """
    dim1 = NormDimensions.from_norm(norm1)
    dim2 = NormDimensions.from_norm(norm2)
    if dim1 == dim2:
        return
    target_dim = dim1 | dim2
    if dim1 != target_dim:
        _adjust_norm(norm1, target_dim - dim1, target_dim.languages)
    if dim2 != target_dim:
        _adjust_norm(norm2, target_dim - dim2, target_dim.languages)