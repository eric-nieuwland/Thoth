# standard library imports

# third party imports
import typer

# own imports
from .check_fragments import check_fragments
from .new_fragments import new_fragments

app = typer.Typer()

app.command("check")(check_fragments)
app.command("new")(new_fragments)
