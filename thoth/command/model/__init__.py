# standard library imports

# third party imports
import typer

# own imports
from .check_model import check_model
from .new_model import new_model

app = typer.Typer()

app.command("check")(check_model)
app.command("new")(new_model)
