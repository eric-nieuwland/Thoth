# standard library imports

# third party imports
import typer

# own imports
from .about import about
from .languages import languages
from .lorem_ipsum import lorem_ipsum
from .render import app as render_app


app = typer.Typer()

app.command("about")(about)
app.command("languages")(languages)
app.command("lorem-ipsum")(lorem_ipsum)

app.add_typer(render_app, name="render", help="Render documents")
