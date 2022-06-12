from .elements import Value


def test(tup: tuple) -> Value:
    # tup = Value(("x", True, True, 0, 0))
    match tup[0]:
        case ["x" | "y" | "touch" | "text"]:
            return tup
        case _:
            raise TypeError(f"{tup} is not a valid Value.")


test(("a", True, True, 0, 0))
