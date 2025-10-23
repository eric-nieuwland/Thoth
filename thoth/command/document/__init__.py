# standard library imports

# third party imports
import typer

# own imports
from .check_document import check_document
from .new_document import new_document

app = typer.Typer()

app.command("check")(check_document)
app.command("new")(new_document)
