import numpy as np


def flatten(t):
    return [item for sublist in t for item in sublist]


def list_to_lower(t):
    return [s.lower() for s in t]


def remove_duplicates(t):
    return list(set(t))


def maybeMakeNumber(s):
    """Returns a string 's' into a integer if possible, a float if needed or
    returns it as is."""

    # handle None, "", 0
    if not s:
        return None
    try:
        f = float(s)
        i = int(f)
        return i if f == i else f
    except ValueError:
        return s
