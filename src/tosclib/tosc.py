"""
Simplify navigating, editing and generating .tosc files.
"""
import sys
import xml.etree.ElementTree as ET
import re
import zlib
import uuid


class Partial:
    """Valid Partial Elements"""

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
    """Valid Trigger Elements"""

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
    def fromFile(cls, file: str):
        """Returns ElementTOSC, for debugging purposes"""
        return cls(load(file)[0])

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

    def hasProperty(self, key: str):
        for property in self.properties:
            if re.fullmatch(property.find("key").text, key):
                return True
        return False

    def createProperty(self, type: str, key: str, text: str, params: dict = {}) -> bool:
        """Add a new property with key, value and/or value's {<element> : element.text}"""

        if self.hasProperty(key):
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

    def hasValue(self, key: str):
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
        if self.hasValue(key):
            raise ValueError(f"Value '{key}' already exists")
        items = locals().items()
        value = ET.SubElement(self.values, "value")
        for k, v in items:
            if k != "self":
                e = ET.SubElement(value, k)
                e.text = v
        return ET.iselement(value)

    def setValue(
        self,
        key: str,
        locked: str,
        lockedDefaultCurrent: str,
        default: str,
        defaultPull: str,
    ) -> bool:
        items = locals().items()
        for value in self.values:
            if re.fullmatch(value.find("key").text, key):
                for k, v in items:
                    if k != "self":
                        value.find(k).text = v
                return True
        return False

    def setFrame(self, x: float, y: float, w: float, h: float) -> bool:
        """Create a Frame Property, if already exists, then modify it."""
        params = {"x": str(x), "y": str(y), "w": str(w), "h": str(h)}
        if self.hasProperty("frame"):
            return self.setPropertyValue("frame", "", params)
        return self.createProperty("r", "frame", "", params)

    def setColor(self, r: float, g: float, b: float, a: float) -> bool:
        """Create a Color Property, if already exists, then modify it."""
        params = {"r": str(r), "g": str(g), "b": str(b), "a": str(a)}
        if self.hasProperty("color"):
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


def findKey(elements: ET.Element, key: str):
    """Iterate through element with children and return child whose key matches"""
    for e in elements:
        if re.fullmatch(e.find("key").text, key):
            return e


def showElement(e: ET.Element):
    """Generic show function, UTF-8, indented 2 spaces"""
    if sys.version_info[0] == 3 and sys.version_info[1] >= 9:
        ET.indent(e, "  ")
    print(ET.tostring(e).decode("utf-8"))


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
