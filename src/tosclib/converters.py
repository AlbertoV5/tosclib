"""
Python Typed-hinted-tuples to XML Converters
"""

from .elements import *
from xml.etree.ElementTree import Element, SubElement
from typing import overload


def _xml_property(prop: Property) -> tuple[Element, Element]:
    """Internal Property util"""
    name = f"{prop=}".partition("=")[0]
    property = Element("property")
    SubElement(property, "key").text = name
    value = SubElement(property, "value")
    return property, value


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
        SubElement(value, "type").text = v[1]
        SubElement(value, "key").text = v[0]
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
def xml_property(prop: str) -> Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "s"
    value.text = prop
    return property


@overload
def xml_property(prop: bool) -> Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "b"
    value.text = str(int(prop))
    return property


@overload
def xml_property(prop: int) -> Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "i"
    value.text = str(prop)
    return property


@overload
def xml_property(prop: float) -> Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "f"
    value.text = str(prop)
    return property


@overload
def xml_property(prop: tuple[int, ...]) -> Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "r"
    for k, p in zip(("x", "y", "w", "h"), prop):
        SubElement(value, k).text = str(p)
    return property


@overload
def xml_property(prop: tuple[float, ...]) -> Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "c"
    for k, p in zip(("r", "g", "b", "a"), prop):
        SubElement(value, k).text = str(p)
    return property


def xml_property(prop: Property) -> Element:
    """Overloaded Property Converter"""
    ...


def xml_value(val: Value) -> Element:
    """Value Converter, not overloaded."""
    value = Element("value")
    SubElement(value, "key").text = val[0]
    SubElement(value, "locked").text = str(int(val[1]))
    SubElement(value, "lockedDefaultCurrent").text = str(int(val[2]))
    SubElement(value, "valueDefault").text = str(int(val[3]))
    SubElement(value, "defaultPull").text = str(val[4])
    return value


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


def xml_message(msg: MessageOSC | MessageMIDI | MessageLOCAL) -> Element:
    """Overloaded XML Message Converter"""
    ...
