"""
Higher level wrapper for a TOSC Control Element.
"""
import sys
import xml.etree.ElementTree as ET
import re
import zlib
import uuid
from .controls import *
from lxml import etree as ET


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
        """Return iter over children"""
        return iter(self.children)

    def append(self, e: "ElementTOSC") -> "ElementTOSC":
        """Append an ElementTOSC's Node to this element's Children"""
        self.children.append(e.node)
        return self

    def getSet(self, target):
        s = self.node.find(target)
        if s is not None:
            return s
        return ET.SubElement(self.node, target)

    @classmethod
    def fromFile(cls, file: str) -> "ElementTOSC":
        """Load a .tosc file into an XML Element and then as ElementTOSC"""
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
        self.createPropertyUnsafe(property)
        return True

    def createPropertyUnsafe(self, prop: Property) -> bool:
        property = ET.Element("property", attrib={"type": prop.type})
        ET.SubElement(property, "key").text = prop.key
        value = ET.SubElement(property, "value")
        value.text = prop.value
        for paramKey in prop.params:
            ET.SubElement(value, paramKey).text = prop.params[paramKey]
        self.properties.append(property)
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
        for k in value.__slots__:
            ET.SubElement(element, k).text = getattr(value, k)
        return True

    def setValue(self, value: Value) -> bool:
        if not self.hasValue(value.key):
            raise ValueError(f"{value.key} doesn't exist.")
        element = findKey(self.values, value.key)
        for k in value.__slots__:
            element.find(k).text = getattr(value, k)
        return True

    def _createMessage(func) -> ET.Element:
        def wrapper(self, message=None):
            name, message = func(message)
            msg = ET.SubElement(self.messages, name.value)
            for k in message.__slots__:
                element = ET.SubElement(msg, k)
                v = getattr(message, k)
                if isinstance(v, list):
                    for pt in v:
                        e = ET.SubElement(element, type(pt).__name__.lower())
                        for x in pt.__slots__:
                            ET.SubElement(e, x).text = getattr(pt, x)
                elif isinstance(v, MidiMessage):
                    for x in pt.__slots__:
                        ET.SubElement(element, x).text = getattr(pt, x)
                else:
                    element.text = v
            return msg

        return wrapper

    def _removeMessage(func) -> bool:
        def wrapper(self):
            [msg.remove for msg in self.messages.findall(func(self).value)]
            return True

        return wrapper

    @_createMessage
    def createOSC(self, message: OSC = OSC()) -> ET.Element:
        """Builds and appends an OSC message"""
        return ControlElements.OSC, message

    @_createMessage
    def createMIDI(self, message: MIDI = MIDI()) -> ET.Element:
        """Builds and appends a M1D1 message"""
        return ControlElements.MIDI, message

    @_createMessage
    def createLOCAL(self, message: LOCAL = LOCAL()) -> ET.Element:
        """Builds and appends a LOCAL message"""
        return ControlElements.LOCAL, message

    @_removeMessage
    def removeOSC(self) -> bool:
        """Find and remove all OSC messages"""
        return ControlElements.OSC

    @_removeMessage
    def removeMIDI(self) -> bool:
        """Find and remove all MIDI messages"""
        return ControlElements.MIDI

    @_removeMessage
    def removeLOCAL(self) -> bool:
        """Find and remove all LOCAL messages"""
        return ControlElements.LOCAL

    def findChildByName(self, name: str) -> ET.Element:
        for child in self.children:
            if child.find(ControlElements.PROPERTIES.value) is None:
                continue
            if re.fullmatch(
                getTextValueFromKey(
                    child.find(ControlElements.PROPERTIES.value), "name"
                ),
                name,
            ):
                return child
        return None

    def createChild(self, type: ControlType) -> ET.Element:
        return ET.SubElement(
            self.children,
            ControlElements.NODE.value,
            attrib={"ID": str(uuid.uuid4()), "type": type.value},
        )

    def getID(self) -> str:
        return str(self.node.attrib["ID"])

    def isControlType(self, control: ControlType):
        return str(self.node.attrib["type"]) == control.value

    def setControlType(self, value: ControlType):
        """See ControlType Element"""
        self.node.attrib["type"] = value.value
        return True

    def getFrame(self) -> tuple:
        """Wrapper for getX, getY, etc."""
        return (self.getX(), self.getY(), self.getW(), self.getH())

    def getX(self):
        return float(self.getPropertyParam("frame", "x").text)

    def getY(self):
        return float(self.getPropertyParam("frame", "y").text)

    def getW(self):
        return float(self.getPropertyParam("frame", "w").text)

    def getH(self):
        return float(self.getPropertyParam("frame", "h").text)

    def simpleProperty(fun):
        """Pass value as text arg, so name is Craig"""

        def wrapper(self: "ElementTOSC", value):
            type, key = fun(self)
            element = self.getProperty(key)
            if element is not None:
                self.properties.remove(element)
            return self.createPropertyUnsafe(Property(type.value, key, str(value)))

        return wrapper

    def booleanProperty(fun):
        """Pass value as text arg, so name is Craig"""

        def wrapper(self: "ElementTOSC", value):
            type, key = fun(self)
            element = self.getProperty(key)
            if element is not None:
                self.properties.remove(element)
            return self.createPropertyUnsafe(Property(type.value, key, str(int(value))))

        return wrapper

    def multiProperty(fun):
        """Pass args as tuple of keys, so color is ("r","g","b","a")"""

        def wrapper(self: "ElementTOSC", params):
            type, key, paramKeys = fun(self)
            element = self.getProperty(key)
            if element is not None:
                self.properties.remove(element)
            return self.createPropertyUnsafe(
                Property(
                    type.value,
                    key,
                    params={k: str(params[i]) for i, k in enumerate(paramKeys)},
                )
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


def createTemplate(*, frame: tuple = None) -> ET.Element:
    """Generates a root xml Element and adds the base GROUP node to it."""
    root = ET.Element("lexml", attrib={"version": "3"})
    node = ET.SubElement(
        root,
        ControlElements.NODE.value,
        attrib={"ID": str(uuid.uuid4()), "type": ControlType.GROUP.value},
    )
    if frame is not None:
        ElementTOSC(node).setFrame(frame)
    return root


def createGroup() -> ET.Element:
    """Simple create Node type GROUP"""
    return ET.Element(
        ControlElements.NODE.value,
        attrib={"ID": str(uuid.uuid4()), "type": ControlType.GROUP.value},
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


class PropertyParser:
    """Find all defined properties in the Node"""

    def __init__(self, *args):
        self.targetList = []
        self.args = [*args]
        self.targetFound = None
        self.multiLine = ""
        self.node = False
        self.property = False
        self.key = False
        self.value = False
        self.index = -1

    def start(self, tag, attrib):
        if tag == ControlElements.NODE.value:
            self.index += 1
            self.node = True
            self.targetList.append({arg: "" for arg in [*self.args]})
        elif self.node and tag == ControlElements.PROPERTY.value:
            self.property = True
        elif self.property and tag == "key":
            self.key = True
        elif self.property and tag == "value":
            self.value = True

    def end(self, tag):
        if tag == ControlElements.NODE.value:
            self.node = False
        elif self.node and tag == ControlElements.PROPERTY.value:
            self.property = False
        elif self.property and tag == "key":
            self.key = False
        elif self.property and tag == "value":
            self.value = False

        if self.targetFound and tag == "value":
            self.targetList[self.index][self.targetFound] = self.multiLine
            self.multiLine = ""
            self.targetFound = None

    def data(self, data):
        if (
            self.node
            and self.property
            and self.key
            # and data in self.targetList.keys()
            and data in self.args
        ):
            self.targetFound = data
        if self.node and self.property and self.value and self.targetFound:
            self.multiLine = f"{self.multiLine}{data}"

    def close(self):
        return self.targetList


def parseProperties(node: ET.Element, *args) -> list:
    """
    Specify all properties you want to find and this will parse
    the entire Node and its children and return a list of key value pairs.

    For example:

    [{"name":"control1", "script":"scriptContent1"},
    {"name":"control2", "script":""},
    {"name":"control3", "script":"scriptContent3"}]

    Args:
        node (ET.Element): Node element to parse.

    Returns:
        List[dict]: [{arg: "" for arg in [args]}]
    """
    target = PropertyParser(*args)
    line = ET.tostring(node, encoding="UTF-8")
    parser = ET.XMLParser(target=target)
    parser.feed(line)
    return parser.close()


"""

FUNCTIONS TO ADD CONTROL ELEMENTS TO A ELEMENTTOSC

Creating ElementTOSC directly to a parent.

"""


def addBoxTo(e: ElementTOSC):
    return ElementTOSC(
        ET.SubElement(
            e.children,
            ControlElements.NODE.value,
            attrib={"ID": str(uuid.uuid4()), "type": ControlType.BOX.value},
        )
    )


def addGroupTo(e: ElementTOSC, *args: str):
    """Pass Control Types as arguments to append children to the group.
    Then the result will be a tuple (group, child, child, ...)"""
    group = ElementTOSC(
        ET.SubElement(
            e.children,
            ControlElements.NODE.value,
            attrib={"ID": str(uuid.uuid4()), "type": ControlType.GROUP.value},
        )
    )
    if not args:
        return group
    return [group] + [
        ElementTOSC(
            ET.SubElement(
                group.children,
                ControlElements.NODE.value,
                attrib={"ID": str(uuid.uuid4()), "type": arg},
            )
        )
        for arg in args
    ]


def addButtonTo(e: ElementTOSC):
    return ElementTOSC(e.createChild(ControlType.BUTTON))


def addLabelTo(e: ElementTOSC):
    return ElementTOSC(e.createChild(ControlType.LABEL))


def testFromString(data):
    return ET.fromstring(data)
