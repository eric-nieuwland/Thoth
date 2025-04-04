# standard library imports
from typing import Any, Never
from functools import reduce

# third party imports

# own imports


def reducer(
        a: tuple[int, dict[str, int]],
        b: tuple[int, dict[str, int]],
) -> tuple[int, dict[str, int]]:
    return a[0] + b[0], {key: a[1].get(key, 0) + b[1].get(key, 0) for key in set(a[1]) | set(b[1])}


def count_multi_lingual_helper(arg: Any) -> tuple[int, dict[str, int]]:
    if arg is None:  # don't be fooled by optional elements
        return 0, {}
    if hasattr(arg, "count_multi_lingual"):
        return arg.count_multi_lingual()
    if isinstance(arg, dict):
        return count_multi_lingual_helper(tuple(arg.values()))
    if isinstance(arg, list | set | tuple):
        return reduce(reducer, map(count_multi_lingual_helper, arg), (0, {}))  # type: ignore
    raise TypeError(f"cannot check translations in {arg.__class__.__name__}")
