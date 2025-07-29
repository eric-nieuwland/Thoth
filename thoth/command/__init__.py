# standard library imports

# third party imports
import typer

# own imports
from .about import about
from . import norm
from . import profile
from . import template

app = typer.Typer()

app.command("about")(about)

app.add_typer(norm.app, name="norm", help="Norm commands")
app.add_typer(profile.app, name="profile", help="Profile commands")
app.add_typer(template.app, name="template", help="Template commands")
