import logging
import re
from typing import get_args
from tosclib.controls import ControlBuilder
from .elements import *
from xml.etree.ElementTree import Element, SubElement, fromstring
import zlib


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


def load(inputPath: str) -> Element:
    """Reads a .tosc file and returns the XML root Element"""
    with open(inputPath, "rb") as file:
        return fromstring(zlib.decompress(file.read()))
