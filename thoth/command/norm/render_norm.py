# standard library imports
import sys
from datetime import datetime, timezone
from pathlib import Path

# third party imports
from jinja2 import Environment, PackageLoader

# own imports
from model.norm.norm import Norm
from model.profile.profile import NormRenderProfile

from command.shared.output_format import OutputFormat


def render_norm(
    path: Path,
    language: str,
    profile: Path | None = None,
    output: Path | None = None,
    format: OutputFormat | None = None,
    force: bool = False,
):
    """
    render a norm definition in a document format
    """
    if not path.is_file():
        print(f"so such file - {path}", file=sys.stderr)
        sys.exit(1)

    if format is None and output is None:
        print("need output or format", file=sys.stderr)
        sys.exit(1)

    if format is None:
        suffix = output.suffix  # type: ignore
        if suffix == "":
            print(f"cannot determine format from - {output}", file=sys.stderr)
            sys.exit(1)
        try:
            format = OutputFormat(suffix[1:])
        except ValueError:
            print(f"cannot render - {suffix}", file=sys.stderr)
            sys.exit(1)

    if profile is not None and not profile.exists():
        print(f"so such file - {profile}", file=sys.stderr)
        sys.exit(1)

    if output is not None and output.exists() and not force:
        print(f"file exists - {output}", file=sys.stderr)
        sys.exit(1)

    prof = None if profile is None else NormRenderProfile.from_yaml(profile.open())
    if prof is not None and not prof:
        print(f"profile does not select anything - '{profile}'", file=sys.stderr)
        sys.exit(1)

    norm = Norm.from_yaml(path.open())
    total_count, language_counts = norm.count_multi_lingual()
    if language not in language_counts:
        print(f"language '{language}' not in - {path}", file=sys.stderr)
        sys.exit(1)
    if language_counts[language] < total_count:
        print(
            f"""
WARNING: language '{language}' incomplete in - {path}
         check output for warnings
        """.strip(),
            file=sys.stderr,
        )

    writer = print if output is None else output.write_text

    match format:
        case OutputFormat.HTML:

            env = Environment(
                loader=PackageLoader("thoth", "templates/html/norm"),
            )
            template = env.get_template("norm.html")
            timestamp = datetime.now(tz=timezone.utc)

            html = template.render(
                source=path.name,
                timestamp=timestamp,
                profile=prof,
                norm=norm,
                language=language,
            )
            writer(html)
        case _:
            print(f"cannot render .{format.value}, yet")
