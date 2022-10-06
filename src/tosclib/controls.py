"""Control factory module"""
from .tosclib import Control, ControlType
from . import properties as ps


def default(ct: ControlType, **kwargs):
    # class BoxProperties(_ControlProperties, _BoxProperties):

    match ct:
        case "BOX":
            ...

    return Control(at_type=ct, **kwargs)
