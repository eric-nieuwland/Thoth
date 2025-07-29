# standard library imports
from pathlib import Path

# third party imports
# own imports
from thoth.model.norm.norm import Norm


def languages_in_norm(path: Path) -> None:
    """
    which languages are in the document and in howmany translations is each language present?
    """
    norm = Norm.from_yaml(path.open())
    total, language_counts = norm.count_multi_lingual()
    width = len(f"{total}")
    print(f"languages in {path}:")
    for language, count in sorted(language_counts.items()):
        print(f"""- {language} {count:{width}d}/{total}""")
