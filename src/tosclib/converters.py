"""
Python Typed-hinted-tuples to XML Converters
"""

import logging
from .elements import *
from typing import Literal
from xml.etree.ElementTree import Element, SubElement
from typing import overload

__all__ = [
    # Property
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
]


def _xml_property_generic(name: str) -> tuple[Element, Element]:
    """Create an XML <property> Element of unspecified <value>.

    Args:
        name (str): Name/key of the property.

    Returns:
        tuple[Element, Element]: <property> and <value> Elements.
    """
    property = Element("property")
    SubElement(property, "key").text = name
    value = SubElement(property, "value")
    return property, value


def _xml_value_generic(val: tuple[str, bool, bool, str, int]) -> Element:
    """Create an XML <value> with all its children.

    Args:
        val (tuple[str,bool,bool,str,int]):
        Pass a generic Value with Literal and optionals converted to str.

    Returns:
        Element: <value> Element.
    """
    value = Element("value")
    SubElement(value, "key").text = val[0]
    SubElement(value, "locked").text = str(int(val[1]))
    SubElement(value, "lockedDefaultCurrent").text = str(int(val[2]))
    SubElement(value, "valueDefault").text = val[3]
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


def xml_midimsg(msg: MidiMsg) -> Element:
    """XML midi messages converter. Returns <message>"""
    message = Element("message")
    SubElement(message, "type").text = msg[0]
    SubElement(message, "channel").text = str(msg[1])
    SubElement(message, "data1").text = msg[2]
    SubElement(message, "data2").text = msg[3]
    return message


def xml_midivals(parent: Element, vals: MidiValues) -> Element:
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
    SubElement(parent, "type").text = msg[1]
    SubElement(parent, "conversion").text = msg[2]
    SubElement(parent, "value").text = msg[0]
    SubElement(parent, "scaleMin").text = str(msg[3])
    SubElement(parent, "scaleMax").text = str(msg[4])
    return parent


def xml_localDst(parent: Element, msg: LocalDst) -> Element:
    """XML local destination converter. Returns parent, expects <local>, etc"""
    SubElement(parent, "dstType").text = msg[2]
    SubElement(parent, "dstVar").text = msg[0]
    SubElement(parent, "dstID").text = msg[1]
    return parent


"""
OVERLOADS
"""


@overload
def xml_property(prop: tuple[str, str]) -> Element:
    """Overload for <property type="s">"""
    property, value = _xml_property_generic(prop[0])
    property.attrib["type"] = "s"
    value.text = prop[1]
    return property


@overload
def xml_property(prop: tuple[str, bool]) -> Element:
    """Overload for <property type="b">"""
    property, value = _xml_property_generic(prop[0])
    property.attrib["type"] = "b"
    value.text = str(int(prop[1]))
    return property


@overload
def xml_property(prop: tuple[str, int]) -> Element:
    """Overload for <property type="i">"""
    property, value = _xml_property_generic(prop[0])
    property.attrib["type"] = "i"
    value.text = str(prop[1])
    return property


@overload
def xml_property(prop: tuple[str, float]) -> Element:
    """Overload for <property type="f">"""
    property, value = _xml_property_generic(prop[0])
    property.attrib["type"] = "f"
    value.text = str(prop[1])
    return property


@overload
def xml_property(prop: tuple[str, tuple[int, ...]]) -> Element:
    """Overload for <property type="r">"""
    property, value = _xml_property_generic(prop[0])
    property.attrib["type"] = "r"
    for k, p in zip(("x", "y", "w", "h"), prop[1]):
        SubElement(value, k).text = str(p)
    return property


@overload
def xml_property(prop: tuple[str, tuple[float, ...]]) -> Element:
    """Overload for <property type="c">"""
    property, value = _xml_property_generic(prop[0])
    property.attrib["type"] = "c"
    for k, p in zip(("r", "g", "b", "a"), prop[1]):
        SubElement(value, k).text = str(p)
    return property


def xml_property(prop: Property) -> Element | None:
    """Overloaded Property Converter"""
    logging.warning(f"{prop} is not specific.")
    return None


@overload
def xml_value(val: tuple[Literal["x", "y"], bool, bool, float, int]) -> Element:
    """Literal "x" or "y" Value overload"""
    return _xml_value_generic((str(val[0]), val[1], val[2], str(val[3]), val[4]))


@overload
def xml_value(val: tuple[Literal["text"], bool, bool, str, int]) -> Element:
    """Literal "text" Value overload"""
    return _xml_value_generic((str(val[0]), val[1], val[2], val[3], val[4]))


@overload
def xml_value(val: tuple[Literal["touch"], bool, bool, bool, int]) -> Element:
    """Touch Value overload"""
    return _xml_value_generic((str(val[0]), val[1], val[2], str(int(val[3])), val[4]))


def xml_value(val: Value) -> Element | None:
    """Overloaded Value to XML Converter"""
    logging.warning(f"{val} is not specific.")
    return None


@overload
def xml_message(msg: MessageOSC) -> Element:
    message = Element("osc")
    xml_msgconfig(message, msg[0])
    xml_triggers(SubElement(message, "triggers"), msg[1])
    xml_partials(SubElement(message, "path"), msg[2])
    xml_partials(SubElement(message, "arguments"), msg[3])
    return message


@overload
def xml_message(msg: MessageMIDI) -> Element:
    message = Element("midi")
    xml_msgconfig(message, msg[0])
    xml_triggers(SubElement(message, "triggers"), msg[1])
    message.append(xml_midimsg(msg[2]))
    xml_midivals(Element("values"), msg[3])
    return message


@overload
def xml_message(msg: MessageLOCAL) -> Element:
    message = Element("local")
    SubElement(message, "enabled").text = str(msg[0])
    xml_triggers(SubElement(message, "triggers"), msg[1])
    return message


def xml_message(msg: MessageOSC | MessageMIDI | MessageLOCAL) -> Element | None:
    """Overloaded Message to XML Converter"""
    logging.warning(f"{msg} is not specific.")
    return None
