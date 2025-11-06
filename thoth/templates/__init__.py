"""
templates - rendering templates for various formats
"""

from __future__ import annotations

from pathlib import Path


def templates_home():
    """
    the home of the templates
    """
    return Path(__file__).parent
