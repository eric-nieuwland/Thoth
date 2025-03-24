# standard library imports

# third party imports
import typer

# own imports
from .about import about
from .languages import languages
from .norm import app as norm_app
from .render import app as render_app


app = typer.Typer()

app.command("about")(about)
app.command("languages")(languages)

app.add_typer(norm_app, name="norm", help="Norm commands")
app.add_typer(render_app, name="render", help="Render documents")
