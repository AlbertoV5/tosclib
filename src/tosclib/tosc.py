"""
Simplify navigating, editing and generating .tosc files.
"""
import sys
import xml.etree.ElementTree as ET
import re
import zlib
import uuid
from typing import List


class Value:
    """Valid <value> Elements"""

    def __init__(
        self,
        key: str = "touch",
        locked: str = "0",
        lockedDefaultCurrent: str = "0",
        default: str = "false",
        defaultPull: str = "0",
    ):
        """Default Value Elements for "touch".

        Args:
            key (str, optional): "x" or "touch". Defaults to "touch".
            locked (str, optional): boolean. Defaults to "0".
            lockedDefaultCurrent (str, optional): boolean. Defaults to "0".
            default (str, optional): float or boolean. Defaults to "false".
            defaultPull (str, optional): 0 to 100. Defaults to "0".
        """
        self.key = key
        self.locked = locked
        self.lockedDefaultCurrent = lockedDefaultCurrent
        self.default = default
        self.defaultPull = defaultPull


class Partial:
    """Valid <partial> Elements"""

    def __init__(
        self,
        type: str = "CONSTANT",
        conversion: str = "STRING",
        value: str = "/",
        scaleMin: str = "0",
        scaleMax: str = "1",
    ):
        """Default Partial Elements for "CONSTANT"

        Args:
            type (str, optional): "CONSTANT", "INDEX", "VALUE", "PROPERTY". Defaults to "CONSTANT".
            conversion (str, optional): "BOOLEAN", "INTEGER", "FLOAT", "STRING". Defaults to "STRING".
            value (str, optional): Depends on the context. Defaults to "/".
            scaleMin (str, optional): If "VALUE", set range. Defaults to "0".
            scaleMax (str, optional): If "VALUE", set range. Defaults to "1".
        """

        self.type = type
        self.conversion = conversion
        self.value = value
        self.scaleMin = scaleMin
        self.scaleMax = scaleMax


class Trigger:
    """Valid <trigger> Elements"""

    def __init__(self, var: str = "x", con: str = "ANY"):
        """Default Trigger Elements for "x"

        Args:
            var (str, optional): "x" or "touch". Defaults to "x".
            con (str, optional): "ANY", "RISE" or "FALL". Defaults to "ANY".
        """
        self.var = var
        self.condition = con


class OSC:
    """Valid <osc> Elements"""

    def __init__(
        self,
        enabled: str = "1",
        send: str = "1",
        receive: str = "1",
        feedback: str = "0",
        connections: str = "00001",
        triggers: List[Trigger] = [Trigger()],
        path: List[Partial] = [Partial(), Partial(type="PROPERTY", value="name")],
        arguments: List[Partial] = [
            Partial(type="VALUE", conversion="FLOAT", value="x")
        ],
    ):
        """Default OSC Elements for address "/name", arguments "x"

        Args:
            enabled (str, optional): Boolean. Defaults to "1".
            send (str, optional): Boolean. Defaults to "1".
            receive (str, optional): Boolean. Defaults to "1".
            feedback (str, optional): Boolean. Defaults to "0".
            connections (str, optional): Binary. Defaults to "00001" (channel 1, "00011" means 1 and 2).
            triggers (List[Trigger], optional): [Trigger]. Defaults to [Trigger()].
            path (List[Partial], optional): [Partial]. Defaults to [Partial(), Partial(typ="PROPERTY", val="name")].
            arguments (List[Partial], optional): [Partial]. Defaults to [Partial(typ="VALUE", con="FLOAT", val="x")].
        """

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

    def __init__(self, e: ET.Element):
        """Find SubElements on init

        Args:
            e (ET.Element): <node> Element

        Attributes:
            properties (ET.Element): Find <properties>
            values (ET.Element): Find <values>
            messages (ET.Element): Find <messages>
            children (ET.Element): Find <children>
        """
        self.node = e
        f = lambda v: e.find(v) if e.find(v) else ET.SubElement(e, v)
        self.properties = f("properties")
        self.values = f("values")
        self.messages = f("messages")
        self.children = f("children")

    @classmethod
    def fromFile(cls, file: str) -> "ElementTOSC":
        return cls(load(file)[0])

    def getProperty(self, key: str) -> ET.Element:
        return findKey(self.properties, key)

    def getPropertyValue(self, key: str) -> ET.Element:
        return findKey(self.properties, key).find("value")

    def getPropertyParam(self, key: str, param: str) -> ET.Element:
        return findKey(self.properties, key).find("value").find(param)

    def hasProperty(self, key: str) -> bool:
        return True if ET.iselement(findKey(self.properties, key)) else False

    def setProperty(self, key: str, text: str = "", params: dict = {}) -> bool:
        if not text and not params:
            raise ValueError(f"Missing either text or params")
        if not self.hasProperty(key):
            raise ValueError(f"Property '{key}' doesn't exist.")
        value = self.getPropertyValue(key)
        if text:
            value.text = text
            return True
        for paramKey in params:
            e = value.find(paramKey)
            e.text = params[paramKey]
        return True

    def createProperty(
        self, type: str, key: str, text: str = "", params: dict = {}
    ) -> bool:
        if self.hasProperty(key):
            raise ValueError(f"Property '{key}' already exists.")
        property = ET.SubElement(self.properties, "property", attrib={"type": type})
        (keyElement, valueElement) = (
            ET.SubElement(property, "key"),
            ET.SubElement(property, "value"),
        )
        keyElement.text = key
        if text:
            valueElement.text = text
            return True
        for paramKey in params:
            subElement = ET.SubElement(valueElement, paramKey)
            subElement.text = params[paramKey]
        return True

    def getValue(self, key: str) -> ET.Element:
        return findKey(self.values, key)

    def getValueParam(self, key: str, param: str) -> ET.Element:
        return findKey(self.values, key).find(param)

    def hasValue(self, key: str) -> bool:
        return True if findKey(self.values, key) else False

    def createValue(self, value: Value) -> bool:
        if self.hasValue(value.key):
            raise ValueError(f"Value '{value.key}' already exists.")
        element = ET.SubElement(self.values, "value")
        for v in vars(value):
            e = ET.SubElement(element, v)
            e.text = getattr(value, v)
        return ET.iselement(element)

    def setValue(self, value: Value) -> bool:
        if not self.hasValue(value.key):
            raise ValueError(f"Value '{value.key}' doesn't exist.")
        element = findKey(self.values, value.key)
        for v in vars(value):
            element.find(v).text = getattr(value, v)
        return True

    def createOSC(self, message: OSC = OSC()) -> ET.Element:
        """Create new OSC message from dict"""
        osc = ET.SubElement(self.messages, "osc")
        for key in vars(message):
            element = ET.SubElement(osc, key)
            obj = getattr(message, key)
            if isinstance(obj, list):  # For Partials and Triggers
                for val in obj:
                    partial = ET.SubElement(element, type(val).__name__.lower())
                    for v in vars(val):  # Attributes of Partials/Triggers
                        s = ET.SubElement(partial, v)
                        s.text = getattr(val, v)
            else:
                element.text = getattr(message, key)
        return osc

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

    def createChild(self, type: str) -> ET.Element:
        """
        Create and return a children Element with attrib = {'ID' : str(uuid4()), 'type' : type}
        """
        return ET.SubElement(
            self.children, "node", attrib={"ID": str(uuid.uuid4()), "type": type}
        )

    def setFrame(self, x: float, y: float, w: float, h: float) -> bool:
        """Create a Frame Property, if already exists, then modify it."""
        params = {"x": str(x), "y": str(y), "w": str(w), "h": str(h)}
        if not self.hasProperty("frame"):
            return self.createProperty("r", "frame", "", params)
        return self.setProperty("frame", "", params)

    def setColor(self, r: float, g: float, b: float, a: float) -> bool:
        """Create a Color Property, if already exists, then modify it."""
        params = {"r": str(r), "g": str(g), "b": str(b), "a": str(a)}
        if not self.hasProperty("color"):
            return self.createProperty("c", "color", "", params)
        return self.setProperty("color", "", params)

    def show(self):
        showElement(self.node)

    def showProperties(self):
        showElement(self.properties)

    def showValues(self):
        showElement(self.values)

    def showMessages(self):
        showElement(self.messages)

    def showChildren(self):
        showElement(self.children)

    def showProperty(self, name: str):
        showElement(findKey(self.properties, name))

    def showValue(self, name: str):
        showElement(findKey(self.values, name))


def findKey(elements: ET.Element, key: str) -> ET.Element:
    """Iterate through element with children and return child whose key matches"""
    for e in elements:
        if re.fullmatch(e.find("key").text, key):
            return e


def showElement(e: ET.Element) -> str:
    """Generic show function, UTF-8, indented 2 spaces"""
    if sys.version_info[0] == 3 and sys.version_info[1] >= 9:
        ET.indent(e, "  ")
    show = ET.tostring(e).decode("utf-8")
    print(show)
    return show


def createTemplate() -> ET.Element:
    """Generates a root Element for your .tosc file"""
    root = ET.Element("lexml", attrib={"version": "3"})
    ET.SubElement(root, "node", attrib={"ID": str(uuid.uuid4()), "type": "GROUP"})
    return root


def load(inputPath: str) -> ET.Element:
    """Reads a .tosc file and returns the XML root Element"""
    with open(inputPath, "rb") as file:
        return ET.fromstring(zlib.decompress(file.read()))


def write(root: ET.Element, outputPath: str = None) -> bool:
    """Encodes a root Element to .tosc"""
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
