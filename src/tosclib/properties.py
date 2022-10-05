from .tosclib import Property


def name(value=""):
    return Property(at_type="s", key="name", value=value)


def tag(value=""):
    return Property(at_type="s", key="tag", value=value)


def frame(value=(640, 480, 0, 0)):
    return Property(at_type="r", key="frame", value=value)


def color(value=(0.2, 0.2, 0.2, 1.0)):
    return Property(at_type="c", key="color", value=value)


def locked(value=False):
    return Property(at_type="b", key="locked", value=value)


def interactive(value=True):
    return Property(at_type="b", key="interactive", value=value)


def background(value=True):
    return Property(at_type="b", key="background", value=value)


# def x(value = 0):
#     return Value(name="x", default=value)

# def y(value = 0):
#     return Value(name="y", default=value)
