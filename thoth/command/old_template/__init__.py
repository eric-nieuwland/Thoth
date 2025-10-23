# standard library imports

# third party imports
import typer

# own imports
from .new_template import new_template

app = typer.Typer()

app.command("new")(new_template)
