# standard library imports

# third party imports
import typer

# own imports
from . import (
    model,
    profile,
    # old
    old_norm,
    old_norm_profile,
    old_template,
)
from .about import about

app = typer.Typer()

app.command("about")(about)

app.add_typer(model.app, name="model", help="Document model commands")
app.add_typer(profile.app, name="profile", help="Document profile commands")
# old
app.add_typer(old_norm.app, name="old-norm", help="Norm commands")
app.add_typer(old_norm_profile.app, name="norm-profile", help="Norm profile commands")
app.add_typer(old_template.app, name="old-template", help="Template commands")
