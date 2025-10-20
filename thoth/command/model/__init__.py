# standard library imports

# third party imports
import typer

# own imports
from .new_model import new_model

app = typer.Typer()

app.command("new")(new_model)
