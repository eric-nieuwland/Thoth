# standard library imports
from typing import Any, Iterable, TypeVar

# third party imports

# own imports


T = TypeVar("T")


def flatten[T](lst: T) -> T:
    """
    remove all embedded levels of lists and tuples
    return the result as a list or tuple, depending on the type of the argument
    """
    if not isinstance(lst, list | tuple):
        return lst
    maker = tuple if isinstance(lst, tuple) else list
    return maker(
        item
        for items in [
            flatten(item) if isinstance(item, list | tuple) else [item]
            for item in lst
        ]
        for item in items
    )
