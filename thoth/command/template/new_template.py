# standard library imports
from pathlib import Path

# third party imports
# own imports
from thoth.command.shared.output_format import OutputFormat
from thoth.templates import copy_templates, templates_home


def new_template(
    output: Path,
    format: OutputFormat | None = None,
    force: bool = False,
):
    """
    create a starting point for a template definition
    """

    formats = [f.value for f in ((format,) if format else OutputFormat.all())]

    copy_templates(templates_home(), output, formats, force=force)
