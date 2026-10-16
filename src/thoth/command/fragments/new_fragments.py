"""
new_model - create a new document model
"""

from __future__ import annotations

# standard library imports

# third party imports

# own imports
from thoth.command.shared.arguments_and_options_info import (
    OUTPUT_PATH_OPTION,
)
from thoth.command.shared.write_output import write_output


def new_fragments(
    output: OUTPUT_PATH_OPTION = None,
    force: bool = False,
) -> None:
    """
    create a starting point for fragments
    """
    fragments = """
title:
  en: Single source multiple format output document management
  nl: Enkelvoudige bron, meervoudige opmaak documentbeheer
chapters:
  one:
    en: Chapter One
    nl: Hoofdstuk Een
  two:
    en: Chapter Two
    nl: Hoofdstuk Twee
copyright:
  en: Trusties of the Unicorn
  nl: Jut en Jul
    """
    write_output(
        fragments,
        destination=output,
        force=force,
    )
