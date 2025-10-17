# standard library imports

# third party imports
import typer

# own imports
from .new_definition import new_definition

app = typer.Typer()

app.command("new")(new_definition)
