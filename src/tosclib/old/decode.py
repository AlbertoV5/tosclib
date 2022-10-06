"""
Parse XML Elements and return tosclib types.
"""
import uuid
from .core import *
from .factory import (
    local,
    localdst,
    localsrc,
    midi,
    midimsg,
    midival,
    msgconfig,
    osc,
    partial,
    property,
    trigger,
    value,
)


__all__ = ["to_property", "to_value", "to_message", "to_ctrl"]


class ParseXML(Exception):
    """Base Error when parsing XML files"""

    def __init__(self, e: Element, msg: str):
        """Element, Functions and Error specific message."""
        self.message = f"Could not parse {e} as Control. {msg}"
        super().__init__(self.message)


class ParseXMLValueError(ParseXML):
    def __init__(self, e: Element, value: str):
        """Value Errors such as None Types.

        Args:
            e (Element): Element that was being parsed when the exception ocurred.
            f (str): Name of the function where the exception ocurred.
            value (str): Specific cause of exception.
        """
        super().__init__(e, f"{value} has an invalid value.")


class ParseXMLKeyError(ParseXML):
    def __init__(self, e: Element, value: str, keys: tuple):
        """Key Errors when string doesn't match any Key in a tuple/list/set.

        Args:
            e (Element): Element that was being parsed when the exception ocurred.
            f (str): Name of the function where the exception ocurred.
            keys (tuple): Keys that failed to be parsed.
        """
        super().__init__(e, f"Key of {value} wasn't found in {keys}.")


def to_property(e: Element) -> Property:
    """Parse key, value, params and type attrib.

    Args:
        e (Element): <property> under <properties>

    Raises:
        ParseXMLKeyError: If type is not in PROPERTY_TYPES.
        ParseXMLValueError: If key is None.
        ParseXMLValueError: If type, value are None.

    Returns:
        Property: If all valid.
    """
    key, value = (e[i].text for i in range(0, 2))
    type = e.attrib["type"]

    if key is None:
        raise ParseXMLValueError(e, "key")
    if value is None:
        value = ""
        params = tuple(i.text for i in e[1] if i.text is not None)

    if type is PROPERTY_TYPES.BOOLEAN:
        return property(key, eval_bool(value))
    elif type is PROPERTY_TYPES.COLOR:
        return property(key, tuple(float(i) for i in params))
    elif type is PROPERTY_TYPES.FLOAT:
        return property(key, float(value))
    elif type is PROPERTY_TYPES.INTEGER:
        return property(key, int(value))
    elif type is PROPERTY_TYPES.FRAME:
        return property(key, tuple(float(i) for i in params))
    elif type is PROPERTY_TYPES.STRING:
        return property(key, value)
    else:
        raise ParseXMLKeyError(e, "type", PROPERTY_TYPES)


def to_value(e: Element) -> Value:
    """Pase key, locked, locked_default, default, pull

    Args:
        e (Element): <value> under <values> under <node>

    Raises:
        ParseXMLKeyError: If key is not in VALUE_KEYS.
        ParseXMLValueError: If default is None.
        ParseXMLValueError: If pull is None.

    Returns:
        Value: If all valid.
    """
    key, locked, lock_def, default, pull = (e[i].text for i in range(0, 5))

    if not is_value_key(key):
        raise ParseXMLKeyError(e, "key", VALUE_KEYS)
    if default is None or pull is None:
        raise ParseXMLValueError(e, "default or pull")

    if key == VALUE_KEYS.X or key == VALUE_KEYS.Y:
        return value(
            key, eval_bool(locked), eval_bool(lock_def), float(default), int(pull)
        )
    elif key == VALUE_KEYS.PAGE:
        return value(
            key, eval_bool(locked), eval_bool(lock_def), int(default), int(pull)
        )
    elif key == VALUE_KEYS.TOUCH:
        return value(
            key, eval_bool(locked), eval_bool(lock_def), eval_bool(default), int(pull)
        )
    else:
        return value(key, eval_bool(locked), eval_bool(lock_def), default, int(pull))


def to_msgconfig(e: Element) -> MsgConfig:
    """Parse enabled, send, receive, feedback, connections.

    Args:
        e (Element): <osc> or <midi>

    Raises:
        ParseXMLValueError: If connections is None.

    Returns:
        MsgConfig: If any is None, they default to False or '00000'.
    """
    enab, send, receive, fbk = (eval_bool(e[i].text) for i in range(0, 4))
    connections = "00000" if e[4].text is None else e[4].text

    return msgconfig(enab, send, receive, fbk, connections)


def to_trigger(e: Element) -> Trigger:
    """Parses var, condition.

    Args:
        e (Element): <trigger> under <triggers>

    Raises:
        ParseXMLKeyError: If var is not in VALUE_KEYS.
        ParseXMLKeyError: If condition is not in TRIGGER_TYPES.

    Returns:
        Trigger: If all valid.
    """
    var, condition = (e[i].text for i in range(0, 2))

    if not is_value_key(var):
        raise ParseXMLKeyError(e, "var", VALUE_KEYS)
    if not is_trigger_type(condition):
        raise ParseXMLKeyError(e, "condition", TRIGGER_TYPES)

    return trigger(var, condition)


def to_partial(e: Element) -> Partial:
    """Parses type, conversion, value, scale_min, scale_max.

    Args:
        e (Element): <partial> under <path> or <arguments>

    Raises:
        ParseXMLValueError: If scale_min or scale_max are None.
        ParseXMLKeyError: If type is not in PARTIAL_TYPES.
        ParseXMLKeyError: If conversion is not in PARTIAL_CONVERSIONS.

    Returns:
        Partial: If all valid.
    """
    type, conv, value, s_min, s_max = (e[i].text for i in range(0, 5))

    if not is_partial_type(type):
        raise ParseXMLKeyError(e, "type", PARTIAL_TYPES)
    if not is_conversion_type(conv):
        raise ParseXMLKeyError(e, "conversion", CONVERSION_TYPES)
    if s_min is None or s_max is None:
        raise ParseXMLValueError(e, "scale_min or scale_max")
    if value is None:
        value = ""

    return partial(type, conv, value, int(s_min), int(s_max))


def to_midimsg(e: Element) -> MidiMsg:
    """Parse type, channel, data1, data2

    Args:
        e (Element): <message> under <midi>

    Raises:
        ParseXMLValueError: If channel, data1 or data2 are None.
        ParseXMLKeyError: If type is not in MIDI_MESSAGE_TYPE.

    Returns:
        MidiMsg: If all valid.
    """
    type, chan, data1, data2 = (e[i].text for i in range(0, 4))

    if not is_midi_msg_type(type):
        raise ParseXMLKeyError(e, "type", MIDI_MESSAGE_TYPES)
    if chan is None or data1 is None or data2 is None:
        raise ParseXMLValueError(e, "channel or data1 or data2")

    return midimsg(type, int(chan), data1, data2)


def to_midivalue(e: Element) -> MidiValue:
    """Parse type, key, scale_min, scale_max.

    Args:
        e (Element): <value> under <values> under <midi>

    Raises:
        ParseXMLKeyError: If type is not in PARTIAL_TYPES.
        ParseXMLValueError: If scale_min or scale_max are None.

    Returns:
        MidiValue: If all valid.
    """
    type, key, s_min, s_max = (e[i].text for i in range(0, 4))

    if not is_partial_type(type):
        raise ParseXMLKeyError(e, "type", PARTIAL_TYPES)
    if s_min is None or s_max is None:
        raise ParseXMLValueError(e, "scale_min or scale_max")
    if key is None:
        key = ""

    return midival(key, type, int(s_min), int(s_max))


def to_localsrc(e: Element) -> LocalSrc:
    """Parse type, conversion, value, scale_min, scale_max.

    Args:
        e (Element): <local> from <messages>

    Raises:
        ParseXMLKeyError: If type is not in PARTIAL_TYPES.
        ParseXMLKeyError: If conversion is not in CONVERSION_TYPES.
        ParseXMLValueError: If value, scale_min or scale_max are None.

    Returns:
        LocalSrc: If all valid.
    """
    type, conv, value, s_min, s_max = (e[i].text for i in range(2, 6))

    if not is_partial_type(type):
        raise ParseXMLKeyError(e, "to_localsrc", PARTIAL_TYPES)
    if not is_conversion_type(conv):
        raise ParseXMLKeyError(e, "to_localsrc", CONVERSION_TYPES)
    if s_min is None or s_max is None:
        raise ParseXMLValueError(e, "s_min, scale_max")
    if value is None:
        value = ""

    return localsrc(type, conv, value, int(s_min), int(s_max))


def to_localdst(e: Element) -> LocalDst:
    """Parse the Type, Var and ID of Destination/Target.

    Args:
        e (Element):

    Raises:
        ParseXMLError: If Type is not in PARTIAL_TYPES or None.

    Returns:
        LocalDst:
    """
    type, var, id = (e[i].text for i in range(7, 10))

    if not is_partial_type(type):
        raise ParseXMLKeyError(e, "type", PARTIAL_TYPES)
    if var is None or id is None:
        raise ParseXMLValueError(e, "var, or id")

    return localdst(type, var, id)


def to_message(e: Element) -> Message:
    """Parse osc, midi, local.

    Args:
        e (Element): <osc>, <midi>, <local> under <messages>.

    Raises:
        ParseXMLKeyError: If e.tag is not OSC, MIDI, LOCAL.

    Returns:
        Message: If all sub parsing is valid.
    """
    message_type = e.tag
    if message_type not in MESSAGE_TYPES:
        raise ParseXMLKeyError(e, "message", MESSAGE_TYPES)

    if message_type == MESSAGE_TYPES.OSC:
        msgconfig = to_msgconfig(e)
        triggers = tuple(to_trigger(t) for t in e[5])
        path = tuple(to_partial(p) for p in e[6])
        arguments = tuple(to_partial(a) for a in e[7])
        return osc(msgconfig, triggers, path, arguments)

    elif message_type == MESSAGE_TYPES.MIDI:
        msgconfig = to_msgconfig(e)
        triggers = tuple(to_trigger(t) for t in e[5])
        midimsg = to_midimsg(e[6])
        midivals = tuple(to_midivalue(v) for v in e[7])
        return midi(msgconfig, triggers, midimsg, midivals)

    elif message_type == MESSAGE_TYPES.LOCAL:
        enabled = eval_bool(e[0].text)
        triggers = tuple(to_trigger(t) for t in e[5])
        src = to_localsrc(e)
        dst = to_localdst(e)
        return local(enabled, triggers, src, dst)
    else:
        raise ParseXMLKeyError(e, message_type, MESSAGE_TYPES)


def to_ctrl(node: Element) -> Control:
    """Recursively parses an XML Element Tree and returns a Control.

    Args:
        element (Element | None): XML Element.

    Raises:
        ValueError: In case the function receives a None type.
        ParseXMLError: In case the XML tag is not valid.

    Returns:
        Control: Valid Control if no exceptions were raised.
    """
    type = node.attrib["type"]
    if not is_control_type(type):
        raise ParseXMLKeyError(node, "type", CONTROL_TYPES)
    control = CONTROLS[type](id=uuid.UUID(node.attrib["ID"]))

    for branch in node:
        tag = branch.tag
        if tag == PROPERTIES:
            for property in branch:
                p = to_property(property)
                control.props[p[0]] = p[1]
        elif tag == VALUES:
            for value in branch:
                v = to_value(value)
                control.values[v[0]] = v
        elif tag == MESSAGES:
            for message in branch:
                control.messages.append(to_message(message))
        elif tag == CHILDREN:
            for child in branch:
                control.children.append(to_ctrl(child))
        else:
            raise ParseXMLValueError(branch, tag)

    return control