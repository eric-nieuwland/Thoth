# standard library imports
from datetime import datetime

# third party imports

# own imports
from model.norm import Norm
from utils.flatten import flatten
from .html_norm_fragments import html_styles, html_norm


def footer() -> list[str]:
    return [
        """<div class="footer">""",
        datetime.now().strftime("  rendered by Thoth on %Y/%m/%d at %H:%M"),
        """</div>""",
    ]


def render(norm: Norm, language: str) -> str:
    return "\n".join(
        flatten(
            [
                "<html>",
                "  <head>",
                html_styles.render(),
                "  </head>",
                "  <body>",
                html_norm.render(norm, language),
                footer(),
                "  </body>",
                "</html>",
            ],
        )
    )
