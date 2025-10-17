# standard library imports

# third party imports
import typer

# own imports
from . import (
    definition,
    norm,
    norm_profile,
    template,
)
from .about import about

app = typer.Typer()

app.command("about")(about)

app.add_typer(definition.app, name="definition", help="Document definition commands")
app.add_typer(norm.app, name="norm", help="Norm commands")
app.add_typer(norm_profile.app, name="norm-profile", help="Norm profile commands")
app.add_typer(template.app, name="template", help="Template commands")
