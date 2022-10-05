"""Property factory module"""
from .tosclib import Property


def boolean(key, value):
    return Property(at_type="b", key=key, value=value)


def float(key, value):
    return Property(at_type="f", key=key, value=value)


def int(key, value):
    return Property(at_type="i", key=key, value=value)


def string(key, value):
    return Property(at_type="s", key=key, value=value)


def name(value=""):
    return Property(at_type="s", key="name", value=value)


def tag(value=""):
    return Property(at_type="s", key="tag", value=value)


def frame(key="frame", value=(640, 480, 0, 0)):
    return Property(at_type="r", key=key, value=value)


def color(key="color", value=(0.2, 0.2, 0.2, 1.0)):
    return Property(at_type="c", key=key, value=value)


# def x(value = 0):
#     return Value(name="x", default=value)

# def y(value = 0):
#     return Value(name="y", default=value)
