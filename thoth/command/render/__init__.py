# standard library imports

# third party imports
import typer

# own imports
from .render_norm import render_norm
from .render_translation import render_translation


app = typer.Typer()
app.command("norm")(render_norm)
app.command("translation")(render_translation)
