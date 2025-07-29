"""
templates - rendering templates for various formats
"""

from __future__ import annotations

from pathlib import Path

from .copy_templates import copy_templates


def templates_home():
    """
    the home of the templates
    """
    return Path(__file__).parent
