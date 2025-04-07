# standard library imports
from enum import Enum

# third party imports

# own imports


class OutputFormat(Enum):
    HTML = "html"
    DOCX = "docx"


class Audience(Enum):
    MANAGEMENT = "management"
    DEVELOPERS = "developers"
    TESTERS = "testers"
    GEEKS = "geeks"
