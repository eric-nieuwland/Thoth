# standard library imports

# third party imports
import typer

# own imports
from .check_document import check_document
from .new_document import new_document
from .render_document import render_document

app = typer.Typer()

app.command("check")(check_document)
app.command("new")(new_document)
app.command("render")(render_document)
