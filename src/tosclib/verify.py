"""
Converter functions that verify XML Elements and return tosclib types.
"""

import logging
from .controls import *
from .elements import *
from xml.etree.ElementTree import Element

__all__ = ["to_prop", "to_val", "to_msg", "to_typ", "to_ctrl"]


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



def to_msgconfig(e: Element) -> MsgConfig | None:
    text = (
        e[0].text, e[1].text, e[2].text, e[3].text, e[4].text
    )
    if None in text:
        return None

    return MsgConfig((
        True if text[0] == "1" else False,
        True if text[1] == "1" else False,
        True if text[2] == "1" else False,
        True if text[3] == "1" else False,
        str(text[4])
    ))

def to_trigger(t:Element)-> Trigger | None:
    """Check for Literals on <trigger> children

    Args:
        t (Element): <trigger>

    Returns:
        Trigger | None: Returns Trigger if Literals match.
    """
    if (var:=t[0].text) is None or (cond:=t[1].text) is None:
        return None
    match var,cond:
        case( 
            "x" | "y" | "touch" | "text",
            "ANY" | "RISE" | "FALL"):
            return var,cond # type: ignore
        case _:
            return None

def to_triggers(e:Element)-> Triggers | None:
    """Iterator over to_trigger

    Args:
        e (Element): <triggers>

    Returns:
        Triggers | None: Returns tuple of Trigger
    """
    triggers = []
    for t in e:
        if (trigg:=to_trigger(t)) is None:
            return None
        triggers.append(trigg)
    return tuple(triggers)

def to_partial(e:Element)-> Partial | None:
    """Checks if first two elements' text have the required Literals.

    Args:
        e (Element): <partial>

    Returns:
        Partial | None: Returns Partial if Literals match.
    """
    text = tuple(t for i in e if (t:=i.text) is not None)
    if None in text:
        return None
    match text:
        case (
            "CONSTANT"| "INDEX" | "VALUE"| "PROPERTY",
            "BOOLEAN" | "INTEGER" | "FLOAT" | "STRING",
            _, _, _):
            return Partial(( # type: ignore
                text[0],
                text[1],
                text[2],
                int(text[3]),
                int(text[4])
                ))
        case _:
            return None
    


def to_address(e:Element)-> Address | None:
    """Iterate over elements as Partial

    Args:
        e (Element): <path>

    Returns:
        Address | None: Returns tuple of Partials if they all match.
    """
    address = []
    for p in e:
        if (part:=to_partial(p)) is None:
            return None
        address.append(part)
    return tuple(address)

def to_args(e:Element)-> Arguments | None:
    """Iterate over elements as Partial

    Args:
        e (Element): <arguments>

    Returns:
        Arguments | None: Returns tuple of Partials if they all match.
    """
    args = []
    for p in e:
        if (part:=to_partial(p)) is None:
            return None
        args.append(part)
    return tuple(args)

def to_msg(e: Element) -> Message | None:
    msg = e.tag
    match msg:
        case "osc":
            if (msgconfig:= to_msgconfig(e)) is None:
                return None
            if (triggers:= to_triggers(e[5])) is None:
                return None
            if (path:= to_address(e[6])) is None:
                return None
            if (arguments:= to_args(e[7])) is None:
                return None
            return MessageOSC((msgconfig,triggers,path,arguments))
        # case "midi":
        #     if (msgconfig:= to_msgconfig(e)) is None:
        #             return None
        #     if (triggers:= to_triggers(e)) is None:
        #         return None
        #     return MessageMIDI((msgconfig,))
        # case "local":
        #     return MessageLOCAL(())
        case _:
            raise ValueError(f"{e} is not a valid message.")


def to_typ(e: Element) -> Control | None:
    id = e.attrib["ID"]
    match e.attrib["type"]:
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

