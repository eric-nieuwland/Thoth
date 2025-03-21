# standard library imports

# third party imports
import typer

# own imports
from .check_norm import check_norm
from .join_norm import join_norm
from .reformat_norm import reformat_norm
from .render_norm import render_norm
from .split_norm import split_norm
from .xcheck_norm import xcheck_norm


app = typer.Typer()
app.command("check")(check_norm)
app.command("join")(join_norm)
app.command("reformat")(reformat_norm)
app.command("render")(render_norm)
app.command("split")(split_norm)
app.command("xcheck")(xcheck_norm)
