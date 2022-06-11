"""Python Typed-hinted Tuples to XML Converters"""

from .elements import *
import xml.etree.ElementTree as ET
from typing import overload


def _xml_property(prop: Property) -> tuple[ET.Element, ET.Element]:
    name = f"{prop=}".partition("=")[0]
    property = ET.Element("property")
    ET.SubElement(property, "key").text = name
    value = ET.SubElement(property, "value")
    return property, value


@overload
def xml_property(prop: str) -> ET.Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "s"
    value.text = prop
    return property


@overload
def xml_property(prop: bool) -> ET.Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "b"
    value.text = str(int(prop))
    return property


@overload
def xml_property(prop: int) -> ET.Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "i"
    value.text = str(prop)
    return property


@overload
def xml_property(prop: float) -> ET.Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "f"
    value.text = str(prop)
    return property


@overload
def xml_property(prop: tuple[int, ...]) -> ET.Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "r"
    for k, p in zip(("x", "y", "w", "h"), prop):
        ET.SubElement(value, k).text = str(p)
    return property


@overload
def xml_property(prop: tuple[float, ...]) -> ET.Element:
    property, value = _xml_property(prop)
    property.attrib["type"] = "c"
    for k, p in zip(("r", "g", "b", "a"), prop):
        ET.SubElement(value, k).text = str(p)
    return property


def xml_property(prop: Property) -> ET.Element:
    """Overloaded Property Converter"""
    ...


def xml_value(val: Value) -> ET.Element:
    value = ET.Element("value")
    ET.SubElement(value, "key").text = val[0]
    ET.SubElement(value, "locked").text = str(int(val[1]))
    ET.SubElement(value, "lockedDefaultCurrent").text = str(int(val[2]))
    ET.SubElement(value, "valueDefault").text = str(int(val[3]))
    ET.SubElement(value, "defaultPull").text = str(int(val[4]))

    return value
