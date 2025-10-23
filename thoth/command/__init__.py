# standard library imports

# third party imports
import typer

# own imports
from . import (
    document,
    model,
    profile,
    template,
)
from .about import about

app = typer.Typer()

app.command("about")(about)

app.add_typer(document.app, name="document", help="Document commands")
app.add_typer(model.app, name="model", help="Document model commands")
app.add_typer(profile.app, name="profile", help="Document profile commands")
app.add_typer(template.app, name="template", help="Document template commands")
