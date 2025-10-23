# standard library imports

# third party imports
import typer

# own imports
from .check_norm import check_norm
from .languages_in_norm import languages_in_norm
from .new_norm import new_norm
from .reformat_norm import reformat_norm
from .render_norm import render_norm
from .render_translated_norm import render_translated_norm
from .split_norm import split_norm
from .update_norm import update_norm
from .xcheck_norm import xcheck_norm

app = typer.Typer()

app.command("check")(check_norm)
app.command("languages")(languages_in_norm)
app.command("new")(new_norm)
app.command("reformat")(reformat_norm)
app.command("render")(render_norm)
app.command("render-translated")(render_translated_norm)
app.command("split")(split_norm)
app.command("update")(update_norm)
app.command("xcheck")(xcheck_norm)
