# standard library imports

# third party imports

# own imports
from model.norm import Norm


def render(norm: Norm, language: str) -> list[str]:
    return [
        """<div class="norm-intro">""",
        norm.intro[language],
        """</div>""",
    ]
