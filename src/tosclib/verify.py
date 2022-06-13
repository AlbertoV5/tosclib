"""
Converter functions that verify XML Elements and return tosclib types.
"""

import logging
from .controls import *
from .elements import *
from xml.etree.ElementTree import Element

__all__ = ["to_prop", "to_val", "to_msg", "to_ctrl"]


def to_prop(e: Element) -> Property | None:
    """
    Args:
        Element that is assumed to be a <property>.

    Get the Element attrib "type" and return a Property Type
    that matches it. So "b" becomes a boolean, "f" becomes a float,
    "r" a tuple[int,...], etc.
    """
    if (key := e[0].text) is None:
        return None
    if (typ := e.attrib["type"]) is None:
        return None

    if (value:= e[1].text) is not None:
        params = None
    else:
        params = tuple(i.text for i in e[1] if i.text is not None)

    match typ, value, params:
        case "s", str(value), None:
            return (key, value)
        case "b", "false", None:
            return (key, False)
        case "b", "true", None:
            return (key, True)
        case "f", str(value), None:
            return (key, float(value))
        case "i", str(value), None:
            return (key, int(value))
        case "r", (_, _, _, _):
            return (key, tuple(int(i) for i in params))
        case "c", (_, _, _, _):
            return (key, tuple(float(i) for i in params))
        case _:
            return None


def to_val(e: Element) -> Value | None:
    if (key := e[0].text) is None or (value := e[3].text) is None:
        return None
    if (
        (lock := e[1].text) is None
        or (lcd := e[2].text) is None
        or (pull := e[4].text) is None
    ):
        return None

    match key, value:
        case "x" | "y":
            return (key, bool(int(lock)), bool(int(lcd)), float(value), int(pull))
        case "touch", "true":
            return ("touch", bool(int(lock)), bool(int(lcd)), True, int(pull))
        case "touch", "false":
            return ("touch", bool(int(lock)), bool(int(lcd)), False, int(pull))
        case "text":
            return (key, bool(int(lock)), bool(int(lcd)), str(value), int(pull))
        case _:
            return None


def to_osc(e: Element) -> MessageOSC | None:
    ...


def to_msg(e: Element) -> Message | None:
    ...


def to_typ(e: Element) -> Control | None:
    id = e.attrib["ID"]
    t = e.attrib["type"]
    # match t:
    #     case (
    #         "BOX" | "BUTTON" | "ENCODER" | "FADER" |
    #         "GROUP" | "GRID" | "PAGER" | "LABEL" |
    #         "TEXT" | "RADIO" | "RADIAL" | "RADAR" |
    #         "XY"):
    #         ControlBuilder(t, id)
    #     case ControlList[0]:
    #         ControlBuilder(t, id)

    match t:
        case "BOX":
            return Box(id)
        case "BUTTON":
            return Button(id)
        case "ENCODER":
            return Encoder(id)
        case "FADER":
            return Fader(id)
        case "GROUP":
            return Group(id)
        case "GRID":
            return Grid(id)
        case "PAGER":
            return Pager(id)
        case "LABEL":
            return Label(id)
        case "TEXT":
            return Text(id)
        case "RADIO":
            return Radio(id)
        case "RADIAL":
            return Radial(id)
        case "RADAR":
            return Radar(id)
        case "XY":
            return Xy(id)
        case _:
            return None


def to_ctrl(e: Element) -> Control:
    if (control:= to_typ(e)) is None:
        raise ValueError(f"{e} type is not valid.")
    for n in e:
        match n.tag:
            case "properties":
                for p in n:
                    if (prop := to_prop(p)) is not None:
                        setattr(control, prop[0], prop)
            case "values":
                for v in n:
                    if (val := to_val(v)) is not None:
                        control.values.append(val)
            case "messages":
                for m in n:
                    if (msg := to_msg(m)) is not None:
                        control.messages.append(msg)
            case "children":
                for c in n:
                    if (ctrl := to_ctrl(c)) is not None:
                        control.children.append(ctrl)
            case _:
                raise ValueError(f"{n} is not valid")

    return control

