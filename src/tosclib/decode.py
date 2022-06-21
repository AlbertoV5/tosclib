"""
Parse XML Elements and return tosclib types.
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
    value = e[1].text
    params = tuple(i.text for i in e[1] if i.text)

    match e.attrib["type"]:
        case "s" if value is not None:
            return (key, value)
        case "b":
            return (key, True if value == "1" else False)
        case "f" if value is not None:
            return (key, float(value))
        case "i" if value is not None:
            return (key, int(value))
        case "r":
            return (key, tuple(int(i) for i in params))
        case "c":
            return (key, tuple(float(i) for i in params))
        case _:
            return None
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


def to_msgconfig(e: Element) -> MsgConfig | None:
    """Checks for enabled, send, receive, feedback, connections.

    Args:
        e (Element): <osc> or <midi> or <local>, etc

    Returns:
        MsgConfig | None: Returns MsgConfig if any Element text is not None
    """
    text = (e[0].text, e[1].text, e[2].text, e[3].text, e[4].text)
    if None in text:
        return None

    return MsgConfig(
        (
            True if text[0] == "1" else False,
            True if text[1] == "1" else False,
            True if text[2] == "1" else False,
            True if text[3] == "1" else False,
            str(text[4]),
        )
    )


def to_trigger(t: Element) -> Trigger | None:
    """Check for Literals on <trigger> children

    Args:
        t (Element): <trigger>

    Returns:
        Trigger | None: Returns Trigger if Literals match.
    """
    var, cond = t[0].text, t[1].text
    match var:
        case "x" | "y" | "touch" | "text":
            match cond:
                case "ANY" | "RISE" | "FALL":
                    return Trigger((var, cond))
                case _:
                    return None
        case _:
            return None


def to_triggers(e: Element) -> Triggers | None:
    """Iterator over to_trigger

    Args:
        e (Element): <triggers>

    Returns:
        Triggers | None: Returns tuple of Trigger
    """
    triggers = []
    for t in e:
        if (trigg := to_trigger(t)) is None:
            return None
        triggers.append(trigg)
    return tuple(triggers)


def to_partial(e: Element) -> Partial | None:
    """Checks if first two elements' text have the required Literals.

    Args:
        e (Element): <partial>

    Returns:
        Partial | None: Returns Partial if Literals match.
    """
    text = tuple(t for i in e if (t := i.text) is not None)
    if None in text:
        return None
    match text:
        case (
            "CONSTANT" | "INDEX" | "VALUE" | "PROPERTY",
            "BOOLEAN" | "INTEGER" | "FLOAT" | "STRING",
            _,
            _,
            _,
        ):
            return Partial(
                (text[0], text[1], text[2], int(text[3]), int(text[4]))  # type: ignore
            )
        case _:
            return None


def to_address(e: Element) -> Address | None:
    """Iterate over elements as Partial

    Args:
        e (Element): <path>

    Returns:
        Address | None: Returns tuple of Partials if they all match.
    """
    address = []
    for p in e:
        if (part := to_partial(p)) is None:
            return None
        address.append(part)
    return tuple(address)


def to_args(e: Element) -> Arguments | None:
    """Iterate over elements as Partial

    Args:
        e (Element): <arguments>

    Returns:
        Arguments | None: Returns tuple of Partials if they all match.
    """
    args = []
    for p in e:
        if (part := to_partial(p)) is None:
            return None
        args.append(part)
    return tuple(args)


def to_midimsg(e: Element) -> MidiMsg | None:
    """Checks if type is one of the valid Literals.

    Args:
        e (Element): <message>

    Returns:
        MidiMsg | None: _description_
    """
    t = e[0].text, e[1].text, e[2].text, e[3].text
    if t[1] is None or t[2] is None or t[3] is None:
        return None
    match t[0]:
        case (
            "NOTE_OFF"
            | "NOTE_ON"
            | "POLYPRESSURE"
            | "CONTROLCHANGE"
            | "PROGRAMCHANGE"
            | "CHANNELPRESSURE"
            | "PITCHBEND"
            | "SYSTEMEXCLUSIVE"
        ):
            return MidiMsg((t[0], int(t[1]), t[2], t[3]))
        case _:
            return None


def to_midivalue(e: Element) -> MidiValue | None:
    """Checks if the type is one of the valid Literals.
    Key is allowed to be None/empty.

    Args:
        e (Element): <value> from <values> from <midi>

    Returns:
        MidiValue | None: Valid MidiValue.
    """
    if (
        (t := e[0].text) is None
        or (x0 := e[2].text) is None
        or (x1 := e[3].text) is None
    ):
        return None
    if (k := e[1].text) is None:
        k = ""
    match t:
        case "CONSTANT" | "INDEX" | "VALUE" | "PROPERTY":

            return MidiValue((t, k, int(x0), int(x1)))
        case _:
            return None


def to_midivals(e: Element) -> MidiValues | None:
    """Iterate through all <value> elements.

    Args:
        e (Element): <values> from <midi>

    Returns:
        MidiValues | None: tuple of MidiValue.
    """
    vals = []
    for v in e:
        if (val := to_midivalue(v)) is None:
            return None
        vals.append(val)
    return tuple(vals)


def to_localsrc(e: Element) -> LocalSrc | None:
    """Checks if type and conversions are valid Literals.

    Args:
        e (Element): <local>

    Returns:
        LocalSrc | None: LocalSrc type.
    """
    t, c = e[2].text, e[3].text
    if (
        (val := e[4].text) is None
        or (x0 := e[5].text) is None
        or (x1 := e[6].text) is None
    ):
        return None
    match t:
        case ("CONSTANT" | "INDEX" | "VALUE" | "PROPERTY"):
            match c:
                case ("BOOLEAN" | "INTEGER" | "FLOAT" | "STRING"):
                    return LocalSrc((t, c, val, int(x0), int(x1)))
                case _:
                    return None
        case _:
            return None


def to_localdst(e: Element) -> LocalDst | None:
    """Checks if type is a valid Literal.

    Args:
        e (Element): <local>

    Returns:
        LocalDst | None: LocalDst type.
    """
    if (typ := e[7].text) is None:
        return None
    var = "" if (var := e[8].text) is None else var
    id = "" if (id := e[9].text) is None else id

    match typ:
        case "CONSTANT" | "INDEX" | "VALUE" | "PROPERTY":
            return LocalDst((typ, var, id))
        case _:
            return None


def to_msg(e: Element) -> Message | None:
    """Checks if the Element is osc,midi,local,etc message.

    Args:
        e (Element): <osc>, <midi>, etc.

    Raises:
        ValueError: If element tag is not valid.

    Returns:
        Message | None: Tuple.
    """
    msg = e.tag
    match msg:
        case "osc":
            if (msgconfig := to_msgconfig(e)) is None:
                return None
            if (triggers := to_triggers(e[5])) is None:
                return None
            if (path := to_address(e[6])) is None:
                return None
            if (arguments := to_args(e[7])) is None:
                return None
            return MessageOSC(("osc", msgconfig, triggers, path, arguments))
        case "midi":
            if (msgconfig := to_msgconfig(e)) is None:
                return None
            if (triggers := to_triggers(e[5])) is None:
                return None
            if (midimsg := to_midimsg(e[6])) is None:
                return None
            if (midivals := to_midivals(e[7])) is None:
                return None
            return MessageMIDI(("midi", msgconfig, triggers, midimsg, midivals))
        case "local":
            if (enabled := e[0].text) is None:
                return None
            if (triggers := to_triggers(e[1])) is None:
                return None
            if (src := to_localsrc(e)) is None:
                return None
            if (dst := to_localdst(e)) is None:
                return None
            return MessageLOCAL(
                ("local", True if enabled == "1" else False, triggers, src, dst)
            )
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


def to_ctrl(e: Element | None) -> Control:
    if e is None:
        raise ValueError(f"{e} is None.")
    if (control := to_typ(e)) is None:
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
                    else:
                        raise ValueError(f"{m} is not a valid Message.")
            case "children":
                for c in n:
                    if (ctrl := to_ctrl(c)) is not None:
                        control.children.append(ctrl)
            case _:
                raise ValueError(f"{n} is not valid")

    return control
