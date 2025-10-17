# standard library imports

# third party imports
import typer

# own imports


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
