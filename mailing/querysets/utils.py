def get_or_none(object_or_none):
    if object_or_none.exists():
        return object_or_none.get()
    return None
