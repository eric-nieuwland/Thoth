# standard library imports

# third party imports

# own imports

def list_joiner(lst1: list | None, lst2: list | None) -> list | None:
    if lst1 is None and lst2 is None:
        return None
    if lst1 is None or lst2 is None:
        raise ValueError("cannot join list and None")
    if len(lst1) != len(lst2):
        raise ValueError("cannot join lists of different lengths")
    return [item1 | item2 for item1, item2 in zip(lst1, lst2)]
