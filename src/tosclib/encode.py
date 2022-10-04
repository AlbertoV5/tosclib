"""
Python Typed-hinted-tuples to XML Converters
"""

import logging
from typing import Callable
from .core import *
from .factory import *
from xml.etree.ElementTree import Element, SubElement

__all__ = [
    # Property
    "property_matcher",
    "xml_property",
    # Value
    "xml_value",
    # Message
    "xml_msgconfig",
    "xml_triggers",
    "xml_partials",
    "xml_midimsg",
    "xml_midivals",
    "xml_localSrc",
    "xml_localDst",
    "xml_message",
    # Node
    "xml_control",
]


def SENTINEL(origin: Callable, msg: str = None) -> Element:
    """Returns None/Invalid XML Element to allow chaining."""
    e = Element("none")
    e.text = str(origin)
    logging.warning(
        f"""Sentinel :
        <{e.tag}> {msg}, from {origin}."""
    )
    return e


def property_matcher(prop: Property, property: Element, value: Element) -> Element:
    """Specialized function to modify XML Elements with Property

    Args:
        prop (Property): Property
        property (Element): <property>
        value (Element): <value>

    Returns:
        Element: Modified <property>
    """
    val = prop[1]
    match val:
        case bool() if val is True:
            property.attrib = {"type": "b"}
            value.text = "1"
        case bool():
            property.attrib = {"type": "b"}
            value.text = "0"
        case str():
            property.attrib = {"type": "s"}
            value.text = str(val)
        case int():
            property.attrib = {"type": "i"}
            value.text = str(val)
        case float():
            property.attrib = {"type": "f"}
            value.text = str(val)
        case tuple():
            if isinstance(val[0], int):
                property.attrib = {"type": "r"}
                keys = ("x", "y", "w", "h")
            else:
                property.attrib = {"type": "c"}
                keys = ("r", "g", "b", "a")
            for k, n in zip(keys, val):
                SubElement(value, k).text = str(n)
        case _:
            return SENTINEL(xml_property, prop[0])
    return property


def xml_property(prop: Property) -> Element:
    """Get a Property type tuple and return XML Element

    Args:
        prop (Property): Tuple to convert to XML

    Returns:
        Element: <property> with <key> and <value>
    """
    property = Element("property")
    SubElement(property, "key").text = prop[0]
    value = SubElement(property, "value")
    return property_matcher(prop, property, value)


def xml_value(val: Value) -> Element:
    """Get a Value type tuple and return an XML Element

    Args:
        val (Value): Value type tuple

    Returns:
        Element: <value> with <key>, <locked>, etc ...
    """
    k, v = val[0], val[3]

    value = Element("value")
    SubElement(value, "key").text = k
    SubElement(value, "locked").text = "1" if val[1] is True else "0"
    SubElement(value, "lockedDefaultCurrent").text = "1" if val[2] is True else "0"

    match k, v:
        case "x" | "y" | "text", float() | str():
            SubElement(value, "default").text = str(v)
        case "touch", bool():
            SubElement(value, "default").text = "1" if v is True else "0"
        case _:
            return SENTINEL(xml_value)

    SubElement(value, "defaultPull").text = str(val[4])

    return value


def xml_msgconfig(parent: Element, msg: MsgConfig) -> Element:
    """XML message config converter. Returns parent, expects <osc> or <midi>, etc"""
    SubElement(parent, "enabled").text = str(int(msg[0]))
    SubElement(parent, "send").text = str(int(msg[1]))
    SubElement(parent, "receive").text = str(int(msg[2]))
    SubElement(parent, "feedback").text = str(int(msg[3]))
    SubElement(parent, "connections").text = msg[4]
    return parent


def xml_triggers(parent: Element, trigs: tuple[Trigger, ...]) -> Element:
    """XML tuple Trigger converter. Returns parent, expects <triggers>"""
    for t in trigs:
        trigger = SubElement(parent, "trigger")
        SubElement(trigger, "var").text = t[0]
        SubElement(trigger, "condition").text = t[1]
    return parent


def xml_partials(parent: Element, parts: tuple[Partial, ...]) -> Element:
    """XML tuple of Partial converter. Returns parent, expects <arguments> or <path>, etc"""
    for p in parts:
        partial = SubElement(parent, "partial")
        SubElement(partial, "type").text = p[0]
        SubElement(partial, "conversion").text = p[1]
        SubElement(partial, "value").text = p[2]
        SubElement(partial, "scaleMin").text = str(p[3])
        SubElement(partial, "scaleMax").text = str(p[4])
    return parent


def xml_midimsg(parent: Element, msg: MidiMsg) -> Element:
    """XML midi messages converter. Returns <message>"""
    message = SubElement(parent, "message")
    SubElement(message, "type").text = msg[0]
    SubElement(message, "channel").text = str(msg[1])
    SubElement(message, "data1").text = msg[2]
    SubElement(message, "data2").text = msg[3]
    return parent


def xml_midivals(parent: Element, vals: tuple[MidiValue, ...]) -> Element:
    """XML midi values converter. Returns parent, expects <values>"""
    for v in vals:
        value = SubElement(parent, "value")
        SubElement(value, "type").text = v[0]
        SubElement(value, "key").text = v[1]
        SubElement(value, "scaleMin").text = str(v[2])
        SubElement(value, "scalemax").text = str(v[3])
    return parent


def xml_localSrc(parent: Element, msg: LocalSrc) -> Element:
    """XML local source converter. Returns parent, expects <local>, etc"""
    SubElement(parent, "type").text = msg[0]
    SubElement(parent, "conversion").text = msg[1]
    SubElement(parent, "value").text = msg[2]
    SubElement(parent, "scaleMin").text = str(msg[3])
    SubElement(parent, "scaleMax").text = str(msg[4])
    return parent


def xml_localDst(parent: Element, msg: LocalDst) -> Element:
    """XML local destination converter. Returns parent, expects <local>, etc"""
    SubElement(parent, "dstType").text = msg[0]
    SubElement(parent, "dstVar").text = msg[1]
    SubElement(parent, "dstID").text = str(msg[2])
    return parent


def _xml_osc(message: Element, msg: MessageOSC) -> Element:
    xml_msgconfig(message, msg[1])
    xml_triggers(SubElement(message, "triggers"), msg[2])
    xml_partials(SubElement(message, "path"), msg[3])
    xml_partials(SubElement(message, "arguments"), msg[4])
    return message


def _xml_midi(message: Element, msg: MessageMIDI) -> Element:
    xml_msgconfig(message, msg[1])
    xml_triggers(SubElement(message, "triggers"), msg[2])
    xml_midimsg(message, msg[3])
    xml_midivals(SubElement(message, "values"), msg[4])
    return message


def _xml_local(message: Element, msg: MessageLOCAL) -> Element:
    SubElement(message, "enabled").text = "1" if msg[1] is True else "0"
    xml_triggers(SubElement(message, "triggers"), msg[2])
    xml_localSrc(message, msg[3])
    xml_localDst(message, msg[4])
    return message


def xml_message(msg: MessageOSC | MessageMIDI | MessageLOCAL) -> Element:
    """Get any Message tuple and returns corresponding XML Element

    Args:
        msg (MessageOSC | MessageMIDI | MessageLOCAL): Any Message tuple.

    Returns:
        Element: Return either <osc>, <midi>, etc.
    """
    message = Element(msg[0])

    if msg[0] == "osc":
        _xml_osc(message, msg)
    elif msg[0] == "midi":
        _xml_midi(message, msg)
    elif msg[0] == "local":
        _xml_local(message, msg)
    else:
        return SENTINEL()
    # https://github.com/python/mypy/issues/12533
    # match msg[0]:
    #     case "osc":
    #         _xml_osc(message, msg)
    #     case "midi":
    #         _xml_midi(message, msg)
    #     case "local":
    #         _xml_local(message, msg)
    #     case _:
    #         return None
    return message


def xml_control(control: Control) -> Element:
    """Convert Control to XML node, recursive for children.

    Args:
        control (Control): Fader, Button, Group, etc.

    Returns:
        Element: XML Element from Control.
    """
    node = Element("node")
    node.attrib = {"type": control.type, "ID": str(control.id)}
    SubElement(node, "properties")
    SubElement(node, "values")
    SubElement(node, "messages")

    for k, v in control.props.items():
        node[0].append(xml_property(Property((k, v))))

    for value in control.values.values():
        node[1].append(xml_value(value))

    for message in control.messages:
        node[2].append(xml_message(message))

    if len(control.children) > 0:
        SubElement(node, "children")
        for child in control.children:
            node[3].append(xml_control(child))

    return node
