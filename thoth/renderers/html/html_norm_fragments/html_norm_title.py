# standard library imports

# third party imports

# own imports
from model.norm import Norm


def title(norm: Norm, language: str) -> list[str]:
    return [
        """<div class="norm-title">""",
        f"  {norm.identifier} - {norm.title[language]}",
        """</div>""",
    ]
