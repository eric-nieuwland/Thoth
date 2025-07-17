# standard library imports

# third party imports
import typer

# own imports
from .about import about
from .norm import app as norm_app
from .profile import app as profile_app

app = typer.Typer()

app.command("about")(about)

app.add_typer(norm_app, name="norm", help="Norm commands")
app.add_typer(profile_app, name="profile", help="Profile commands")
