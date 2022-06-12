import logging
import re
from typing import get_args
from tosclib.controls import ControlBuilder
from .elements import *
from xml.etree.ElementTree import Element, SubElement


class ElementTOSC:
    """
    Control as XML ElementTree, references Node and top layer children.
    Creates them if not found.
    """

    __slots__ = ("node", "properties", "values", "messages", "children")

    def __init__(self, e: Element):
        """Find SubElements on init

        Args:
            e (ET.Element): <node> Element

        Attributes:
            properties (ET.Element): Find <properties>
            values (ET.Element): Find <values>
            messages (ET.Element): Find <messages>
            children (ET.Element): Find <children>
        """
        self.node: Element = e
        self.properties: Element = self._getCreate("properties")
        self.values: Element = self._getCreate("values")
        self.messages: Element = self._getCreate("messages")
        self.children: Element = self._getCreate("children")

    def __iter__(self):
        """Return iter over children"""
        return iter(self.children)

    def __getitem__(self, item):
        """Index children as Elements"""
        return self.__class__(self.children[item])

    def append(self, e: "ElementTOSC") -> "ElementTOSC":
        """Append an ElementTOSC's Node to this element's Children"""
        self.children.append(e.node)
        return self

    def _getCreate(self, target):
        s = self.node.find(target)
        if s is not None:
            return s
        return SubElement(self.node, target)


def is_ctrl(s: str) -> ControlType:
    match s:
        case [
            "BOX" | "BUTTON" | "ENCODER" | "FADER"
            "GROUP" | "GRID" | "RADIO" | "RADAR" | "RADIAL"
            "LABEL" | "TEXT" | "PAGER" | "XY"
        ]:
            return s
        case _:
            raise TypeError(f"{s} is not a valid ControlType.")


def is_val(tup: tuple) -> Value:
    tup = Value(("x", True, True, 0, 0))
    match tup[0]:
        case ["x" | "y" | "touch" | "text"]:
            return tup
        case _:
            raise TypeError(f"{tup} is not a valid Value.")


def as_ctrl(e: ElementTOSC) -> Control:

    control = ControlBuilder(
        is_ctrl(e.node.attrib["type"]),
        e.node.attrib["ID"],
    )

    e.values[0].find("key")

    return control
