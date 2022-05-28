"""
Simplify navigating, editing and generating .tosc files.
"""
import xml.etree.ElementTree as ET
import re
import zlib
import uuid
from enum import Enum, unique


@unique
class SubElements(Enum):
    """Enum for the default SubElements in <node>"""

    PROPERTIES = "properties"  #: Find <properties> of Element.
    VALUES = "values"  #: Find <values> of Element.
    MESSAGES = "messages"  #: Find <messages> of Element.
    CHILDREN = "children"  #: Find <children> of Element.


class Partial:
    """Valid Partial Values"""

    def __init__(
        self,
        typ="CONSTANT",
        con="STRING",
        val="/",
        smin="0",
        smax="1",
    ):

        self.type = typ
        self.conversion = con
        self.value = val
        self.scaleMin = smin
        self.scaleMax = smax


class Trigger:
    """Valid Trigger Values"""

    def __init__(self, var="x", con="ANY"):
        self.var = var
        self.condition = con


class OSC:
    """Valid OSC Message Elements"""

    def __init__(
        self,
        enabled="1",
        send="1",
        receive="1",
        feedback="0",
        connections="00001",
        triggers=[Trigger()],
        path=[Partial(), Partial(typ="PROPERTY", val="name")],
        arguments=[Partial(typ="VALUE", con="FLOAT", val="x")],
    ):
        self.enabled = enabled
        self.send = send
        self.receive = receive
        self.feedback = feedback
        self.connections = connections
        self.triggers = triggers
        self.path = path
        self.arguments = arguments


class ElementTOSC:
    """
    Contains a Node Element and its SubElements.
    Creates Enum SubElements if they are not found in the Node.
    """

    def __init__(self, e: ET.Element, subs: SubElements = SubElements):
        self.node = e
        [
            setattr(self, sub.value, e.find(sub.value))
            if e.find(sub.value)
            else setattr(self, sub.value, ET.SubElement(e, sub.value))
            for sub in subs
        ]

    @classmethod
    def fromFile(cls, file: str, enum: Enum = SubElements):
        """Returns ElementTOSC, for debugging purposes"""
        return cls(load(file)[0], enum)

    def getPropertyValue(self, key: str) -> ET.Element:
        """Find <value> from a known <key>"""
        for p in self.properties:
            if re.fullmatch(p.find("key").text, key):
                return p.find("value")

    def getPropertyParam(self, key: str, param: str) -> ET.Element:
        """Find <value><param> from a known <key>"""
        for p in self.properties:
            if re.fullmatch(p.find("key").text, key):
                return p.find("value").find(param)

    def setPropertyValue(self, key: str, text: str = "", params: dict = {}) -> bool:
        """Set the key's value.text and/or value's {<element> : element.text}"""
        for property in self.properties:
            if re.fullmatch(property.find("key").text, key):
                if text:
                    property.find("value").text = text
                    return True
                else:
                    for paramKey in params:
                        property.find("value").find(paramKey).text = params[paramKey]
                    return True
        return False

    def isProperty(self, key: str):
        for property in self.properties:
            if re.fullmatch(property.find("key").text, key):
                return True
        return False

    def createProperty(self, type: str, key: str, text: str, params: dict = {}) -> bool:
        """Add a new property with key, value and/or value's {<element> : element.text}"""

        if self.isProperty(key):
            raise ValueError(f"Property '{key}' already exists")

        property = ET.SubElement(self.properties, "property", attrib={"type": type})
        keyElement = ET.SubElement(property, "key")
        valueElement = ET.SubElement(property, "value")
        keyElement.text = key
        valueElement.text = text

        for paramKey in params:
            subElement = ET.SubElement(valueElement, paramKey)
            subElement.text = params[paramKey]

        return ET.iselement(property)

    def findChild(self, name: str) -> ET.Element:
        """Look for a Child Node by name"""
        for child in self.children:
            if not child.find("properties"):
                continue
            if re.fullmatch(
                getTextValueFromKey(child.find("properties"), "name"), name
            ):
                return child
        return None

    def createNode(self, type: str) -> ET.Element:
        """
        Create and return a children Element with attrib = {'ID' : str(uuid4()), 'type' : type}
        """
        return ET.SubElement(
            self.children, "node", attrib={"ID": str(uuid.uuid4()), "type": type}
        )

    def isValue(self, key: str):
        for value in self.values:
            if re.fullmatch(value.find("key").text, key):
                return True
        return False

    def createValue(
        self,
        key: str,
        locked: str,
        lockedDefaultCurrent: str,
        default: str,
        defaultPull: str,
    ) -> bool:
        """Create a Value element in <values>"""
        if self.isValue(key):
            raise ValueError(f"Value '{key}' already exists")

        value = ET.SubElement(self.values, "value")
        for i, a in locals().items():
            if i != "self" and i != "value":
                e = ET.SubElement(value, i)
                e.text = a
        return ET.iselement(value)

    def setFrame(self, x, y, w, h) -> bool:
        """Create a Frame Property, if already exists, then modify it."""
        params = {"x": str(x), "y": str(y), "w": str(w), "h": str(h)}
        if self.isProperty("frame"):
            return self.setPropertyValue("frame", "", params)
        return self.createProperty("r", "frame", "", params)

    def setColor(self, r, g, b, a) -> bool:
        """Create a Color Property, if already exists, then modify it."""
        params = {"r": str(r), "g": str(g), "b": str(b), "a": str(a)}
        if self.isProperty("color"):
            return self.setPropertyValue("color", "", params)
        return self.createProperty("c", "color", "", params)

    def createOSC(self, oscMessage: OSC = OSC()) -> ET.Element:
        """Create new OSC message from dict"""
        osc = ET.SubElement(self.messages, "osc")
        for key in vars(oscMessage):
            element = ET.SubElement(osc, key)
            obj = getattr(oscMessage, key)
            if isinstance(obj, list):  # For Partials and Triggers
                for val in obj:
                    partial = ET.SubElement(element, type(val).__name__.lower())
                    for v in vars(val):  # Attributes of Partials/Triggers
                        s = ET.SubElement(partial, v)
                        s.text = getattr(val, v)
            else:
                element.text = getattr(oscMessage, key)
        return osc

    def show(self):
        """Print indented XML as UTF-8"""
        ET.indent(self.node, "  ")
        print(ET.tostring(self.node).decode("utf-8"))

    def showValues(self):
        """Print indented XML as UTF-8"""
        ET.indent(self.values, "  ")
        print(ET.tostring(self.values).decode("utf-8"))

    def showMessages(self):
        for message in self.messages:
            ET.indent(message, "  ")
            print(ET.tostring(message).decode("utf-8"))

    def showProperty(self, name: str):
        """Print indented XML of a single property by name as utf-8"""
        for property in self.properties:
            if re.fullmatch(property.find("key").text, name):
                ET.indent(property, "  ")
                print(ET.tostring(property).decode("utf-8"))

    def showValue(self, name: str):
        """Print indented XML of a single property by name as utf-8"""
        for value in self.values:
            if re.fullmatch(value.find("key").text, name):
                ET.indent(value, "  ")
                print(ET.tostring(value).decode("utf-8"))


def createTemplate() -> ET.Element:
    """Generates a root Element for your .tosc file"""
    root = ET.Element("lexml", attrib={"version": "3"})
    ET.SubElement(root, "node", attrib={"ID": str(uuid.uuid4()), "type": "GROUP"})
    return root


def load(inputPath: str) -> ET.Element:
    """Reads .tosc and returns the xml root element"""
    with open(inputPath, "rb") as file:
        return ET.fromstring(zlib.decompress(file.read()))


def write(root: ET.Element, outputPath: str = None) -> bool:
    """Encodes a root element directly to UTF-8 and compresses to .tosc"""
    with open(outputPath, "wb") as file:
        treeFile = ET.tostring(root, encoding="UTF-8", method="xml")
        file.write(zlib.compress(treeFile))
        return True


def findChildByName(element: ET.Element, name: str) -> ET.Element:
    """Returns the first child element by name"""
    for child in element.find("children"):
        if not child.find("properties"):
            continue
        if re.fullmatch(getTextValueFromKey(child.find("properties"), "name"), name):
            return child


def getTextValueFromKey(properties: ET.Element, key: str) -> str:
    """Find the value.text from a known key"""
    for property in properties:
        if re.fullmatch(property.find("key").text, key):
            return property.find("value").text


def pullValueFromKey(inputFile: str, key: str, value: str, targetKey: str) -> str:
    """Find a value from a known key, value and target key"""
    parser = ET.XMLPullParser()
    with open(inputFile, "rb") as file:
        parser.feed(zlib.decompress(file.read()))
        for _, e in parser.read_events():  # event, element
            if not e.find("properties"):
                continue
            if re.fullmatch(getTextValueFromKey(e.find("properties"), key), value):
                parser.close()
                return getTextValueFromKey(e.find("properties"), targetKey)

    parser.close()
    return ""
