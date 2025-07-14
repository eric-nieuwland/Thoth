# standard library imports

# third party imports
import typer

# own imports
from .new_profile import new_profile
from .reformat_profile import reformat_profile

app = typer.Typer()

app.command("new")(new_profile)
app.command("reformat")(reformat_profile)
