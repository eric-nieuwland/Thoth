# standard library imports

# third party imports
import typer

# own imports
from .check_profile import check_profile
from .new_profile import new_profile

app = typer.Typer()

app.command("check")(check_profile)
app.command("new")(new_profile)
