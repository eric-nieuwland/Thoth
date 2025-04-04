# standard library imports

# third party imports

# own imports


def flatten(lst: list | tuple) -> list | tuple:
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
