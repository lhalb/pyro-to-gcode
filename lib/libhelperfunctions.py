def flatten(t):
    return [item for sublist in t for item in sublist]


def list_to_lower(t):
    return [s.lower() for s in t]


def remove_duplicates(t):
    return list(set(t))
