"""
Higher level wrapper for a TOSC Control Element.
"""
import sys
import xml.etree.ElementTree as ET
import re
import zlib
import uuid
from .controls import *


class ElementTOSC:
    """
    Contains a Node Element and its SubElements. Creates them if not found.
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
        self.properties = self.getSet("properties")
        self.values = self.getSet("values")
        self.messages = self.getSet("messages")
        self.children = self.getSet("children")

    def __iter__(self):
        return iter(self.children)

    def append(self, e: "ElementTOSC") -> "ElementTOSC":
        self.children.append(e.node)
        return self

    def getSet(self, target):
        s = self.node.find(target)
        if s is not None:
            return s
        return ET.SubElement(self.node, target)

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
        return True if findKey(self.properties, key) else False

    def setProperty(self, key: str, value: str = "", params: dict = {}) -> bool:
        if not findKey(self.properties, key):
            raise ValueError(f"{key} doesn't exist.")
        val = self.getPropertyValue(key)
        if value is not None:
            val.text = value
            return True
        for paramKey in params:
            val.find(paramKey).text = params[paramKey]
        return True

    def createProperty(self, property: Property) -> bool:
        if findKey(self.properties, property.key) is not None:
            raise ValueError(f"{property.key} already exists.")
        property.applyTo(self.properties)
        return True

    def getValue(self, key: str) -> ET.Element:
        return findKey(self.values, key)

    def getValueParam(self, key: str, param: str) -> ET.Element:
        return findKey(self.values, key).find(param)

    def hasValue(self, key: str) -> bool:
        return ET.iselement(findKey(self.values, key))

    def createValue(self, value: Value) -> bool:
        if self.hasValue(value.key):
            raise ValueError(f"{value.key} already exists.")
        element = ET.SubElement(self.values, "value")
        for v in vars(value):
            ET.SubElement(element, v).text = getattr(value, v)
        return True

    def setValue(self, value: Value) -> bool:
        if not self.hasValue(value.key):
            raise ValueError(f"{value.key} doesn't exist.")
        element = findKey(self.values, value.key)
        for v in vars(value):
            element.find(v).text = getattr(value, v)
        return True

    def _createMessage(self, name, message) -> ET.Element:
        msg = ET.SubElement(self.messages, name)
        for key in vars(message):
            element = ET.SubElement(
                msg, key
            )  # enabled, send, receive, message, values, etc.
            attribute = getattr(message, key)
            if isinstance(attribute, list):  # For Partials and Triggers
                for partialOrTrigger in attribute:
                    subElement = ET.SubElement(
                        element, type(partialOrTrigger).__name__.lower()
                    )  # Create <partial> or <trigger>
                    for v in vars(partialOrTrigger):  # Attributes of Partials/Triggers
                        ET.SubElement(subElement, v).text = getattr(partialOrTrigger, v)
            elif isinstance(attribute, MidiMessage):  # not a list of Partials, not str
                for v in vars(attribute):
                    ET.SubElement(element, v).text = getattr(attribute, v)
            else:
                element.text = getattr(message, key)
        return msg

    def createOSC(self, message: OSC = OSC()) -> ET.Element:
        return self._createMessage(ControlElements.OSC, message)

    def createMIDI(self, message: MIDI = MIDI()) -> ET.Element:
        return self._createMessage(ControlElements.MIDI, message)

    def createLOCAL(self, message: LOCAL = LOCAL()) -> ET.Element:
        return self._createMessage(ControlElements.LOCAL, message)

    def removeOSC(self) -> bool:
        return [e.remove for e in self.messages.findall(ControlElements.OSC)]

    def removeMIDI(self) -> bool:
        return [e.remove for e in self.messages.findall(ControlElements.MIDI)]

    def removeLOCAL(self) -> bool:
        return [e.remove for e in self.messages.findall(ControlElements.LOCAL)]

    def findChildByName(self, name: str) -> ET.Element:
        for child in self.children:
            if child.find(ControlElements.PROPERTIES) is None:
                continue
            if re.fullmatch(
                getTextValueFromKey(child.find(ControlElements.PROPERTIES), "name"),
                name,
            ):
                return child
        return None

    def createChild(self, type: ControlType) -> ET.Element:
        return ET.SubElement(
            self.children,
            ControlElements.NODE,
            attrib={"ID": str(uuid.uuid4()), "type": type},
        )

    def getID(self) -> str:
        return str(self.node.attrib["ID"])

    def isControlType(self, control: str):
        return str(self.node.attrib["type"]) == control

    def setControlType(self, value: str):
        """See ControlType Element"""
        self.node.attrib["type"] = value
        return True

    def getX(self):
        return int(self.getPropertyParam("frame", "x").text)

    def getY(self):
        return int(self.getPropertyParam("frame", "y").text)

    def getW(self):
        return int(self.getPropertyParam("frame", "w").text)

    def getH(self):
        return int(self.getPropertyParam("frame", "h").text)

    def simpleProperty(fun):
        """Pass value as text arg, so name is Craig"""

        def wrapper(self, value):
            type, key = fun(self)
            element = self.getProperty(key)
            if element is not None:
                self.properties.remove(element)
            return self.createProperty(Property(type, key, str(value)))

        return wrapper

    def booleanProperty(fun):
        """Pass value as text arg, so name is Craig"""

        def wrapper(self, value):
            type, key = fun(self)
            element = self.getProperty(key)
            if element is not None:
                self.properties.remove(element)
            return self.createProperty(Property(type, key, str(int(value))))

        return wrapper

    def multiProperty(fun):
        """Pass args as tuple of keys, so color is ("r","g","b","a")"""

        def wrapper(self, params):
            type, key, paramKeys = fun(self)
            element = self.getProperty(key)
            if element is not None:
                self.properties.remove(element)
            return self.createProperty(
                Property(type, key, params={k : str(params[i]) for i, k in enumerate(paramKeys)})
            )

        return wrapper

    @simpleProperty
    def setName(self):
        """String"""
        return PropertyType.STRING, "name"

    def getName(self):
        return self.getPropertyValue("name").text

    @simpleProperty
    def setTag(self):
        """String"""
        return PropertyType.STRING, "tag"

    @simpleProperty
    def setScript(self):
        """String"""
        return PropertyType.STRING, "script"

    @multiProperty
    def setFrame(self) -> bool:
        """Tuple of x,y,w,h"""
        return PropertyType.FRAME, "frame", ("x", "y", "w", "h")

    @multiProperty
    def setColor(self):
        """r, g, b, a"""
        return PropertyType.COLOR, "color", ("r", "g", "b", "a")

    @booleanProperty
    def setLocked(self):
        """Boolean"""
        return PropertyType.BOOLEAN, "locked"

    @booleanProperty
    def setBackground(self):
        """Boolean"""
        return PropertyType.BOOLEAN, "background"

    @booleanProperty
    def setVisible(self):
        """Boolean"""
        return PropertyType.BOOLEAN, "visible"

    @booleanProperty
    def setInteractive(self):
        """Boolean"""
        return PropertyType.BOOLEAN, "interactive"

    @booleanProperty
    def setOutline(self):
        """Boolean"""
        return PropertyType.BOOLEAN, "outline"

    def show(self):
        showElement(self.node)

    def showProperty(self, name: str):
        try:
            showElement(findKey(self.properties, name))
        except TypeError:
            raise ValueError(f"{name} doesn't exist")

    def showValue(self, name: str):
        try:
            showElement(findKey(self.values, name))
        except TypeError:
            raise ValueError(f"{name} doesn't exist")


""" 

GENERAL FUNCTIONS 

"""


def findKey(elements: ET.Element, key: str) -> ET.Element:
    """Iterate through element with children and return child whose key matches"""
    return elements.find(f"*[key='{key}']")
    # for e in elements:
    #     if re.fullmatch(e.find("key").text, key):
    #         return e
    # return None


def showElement(e: ET.Element):
    """Generic print string function, UTF-8, indented 2 spaces"""
    if sys.version_info[0] == 3 and sys.version_info[1] >= 9:
        ET.indent(e, "  ")
    print(ET.tostring(e).decode("utf-8"))


def createTemplate(*, frame=(0, 0, 2560, 1600)) -> ET.Element:
    """Generates a root Element for your .tosc file"""
    root = ET.Element("lexml", attrib={"version": "3"})
    group = ET.SubElement(
        root,
        ControlElements.NODE,
        attrib={"ID": str(uuid.uuid4()), "type": ControlType.GROUP},
    )
    ElementTOSC(group).setFrame(frame)
    return root


def createGroup() -> ET.Element:
    """Simple create Node type GROUP"""
    return ET.Element(
        ControlElements.NODE,
        attrib={"ID": str(uuid.uuid4()), "type": ControlType.GROUP},
    )


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


def getTextValueFromKey(properties: ET.Element, key: str) -> str:
    """Find the value.text from a known key"""
    for property in properties:
        if re.fullmatch(property.find("key").text, key):
            return property.find("value").text


"""

GENERAL PARSERS

"""


def pullValueFromKey(inputFile: str, key: str, value: str, targetKey: str) -> str:
    """If you know the name of an element but don't know its other properties.
    This function uses a .tosc file and gets its root.
    For passing an element see pullValueFromKey2

    Args:
        inputFile (str): File to parse.
        key (str): Known key.
        value (str): Known value.
        targetKey (str): Known key of unknown value.

    Returns:
        str: Value
    """
    parser = ET.XMLPullParser()
    with open(inputFile, "rb") as file:
        parser.feed(zlib.decompress(file.read()))
        for _, e in parser.read_events():  # event, element
            if e.find("properties") is None:
                continue
            if re.fullmatch(getTextValueFromKey(e.find("properties"), key), value):
                parser.close()
                return getTextValueFromKey(e.find("properties"), targetKey)

    parser.close()
    return ""


def pullValueFromKey2(root: ET.Element, key: str, value: str, targetKey: str) -> str:
    """If you know the name of an element but don't know its other properties.
    This parses an Element and has to convert it to string so its slower.

    Args:
        root (ET.Element): Parses the whole element, so you can feed the root.
        key (str): Known key.
        value (str): Known value.
        targetKey (str): Known key of unknown value.

    Returns:
        str: Value
    """
    parser = ET.XMLPullParser()
    parser.feed(ET.tostring(root, encoding="UTF-8"))
    for _, e in parser.read_events():  # event, element
        if e.find("properties") is None:
            continue
        if re.fullmatch(getTextValueFromKey(e.find("properties"), key), value):
            parser.close()
            return getTextValueFromKey(e.find("properties"), targetKey)


"""

FUNCTIONS TO ADD CONTROL ELEMENTS TO A ELEMENTTOSC

Creating ElementTOSC directly to a parent.

"""


def addBox(e: ElementTOSC):
    return ElementTOSC(
        ET.SubElement(
            e.children,
            ControlElements.NODE,
            attrib={"ID": str(uuid.uuid4()), "type": ControlType.BOX},
        )
    )


def addGroup(e: ElementTOSC, *args: str):
    """Pass Control Types as arguments to append children to the group.
    Then the result will be a tuple (group, child, child, ...)"""
    group = ElementTOSC(
        ET.SubElement(
            e.children,
            ControlElements.NODE,
            attrib={"ID": str(uuid.uuid4()), "type": ControlType.GROUP},
        )
    )
    if not args:
        return group
    return [group] + [
        ElementTOSC(
            ET.SubElement(
                group.children,
                ControlElements.NODE,
                attrib={"ID": str(uuid.uuid4()), "type": arg},
            )
        )
        for arg in args
    ]


def addButton(e: ElementTOSC):
    return ElementTOSC(e.createChild(ControlType.BUTTON))


def addLabel(e: ElementTOSC):
    return ElementTOSC(e.createChild(ControlType.LABEL))


def testFromString(data):
    return ET.fromstring(data)
