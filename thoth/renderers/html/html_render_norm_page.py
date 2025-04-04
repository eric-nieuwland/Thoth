# standard library imports
from datetime import datetime

# third party imports

# own imports
from model.norm.norm import Norm
from model.profile import profile
from utils.flatten import flatten
from .html_norm_fragments import html_styles, html_norm


def footer(source: str, language: str) -> list[str]:
    return [
        """<div class="footer">""",
        f"rendered by Thoth on {datetime.now().strftime("%Y/%m/%d at %H:%M")} in '{language}' from {source}",
        """</div>""",
    ]


def render(source: str, norm: Norm, language: str, prof: profile.Profile | None = None) -> str:
    if prof is not None and not prof:
        return ""

    return "\n".join(
        flatten(
            [
                "<html>",
                "<head>",
                html_styles.styles(),
                "</head>",
                "<body>",
                html_norm.norm(norm, language, prof),
                footer(source, language),
                "</body>",
                "</html>",
            ],
        )
    )
