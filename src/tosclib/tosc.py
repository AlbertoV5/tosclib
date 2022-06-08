"""
Higher level wrapper for a TOSC Control Element.
"""
import logging
from copy import deepcopy
import sys
import re
from typing import TypeGuard
import zlib
import uuid
from .elements import (
    Partial,
    Trigger,
    Property,
    Value,
    OSC,
    MIDI,
    LOCAL,
    MidiMessage,
    PropertyType,
    ControlElements,
    ControlType,
    PropertyFactory,
)
from .controls import (
    XmlFactory,
    Properties,
    controlType
)

# import xml.etree.ElementTree as ET
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

    def __getitem__(self,item):
        return self.__class__(self.children[item])

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

    def setProperty(self, key: str, value: str = "",
                    params: dict = {}) -> bool:
        e = findKey(self.properties, key)
        if e is None:
            raise ValueError(f"{key} doesn't exist.")
        return XmlFactory.modifyProperty(value, params, e)

    def createProperty(self, property: Property) -> bool:
        if findKey(self.properties, property.key) is not None:
            raise ValueError(f"{property.key} already exists.")
        return XmlFactory.buildProperties([property],self.properties)

    def createPropertyUnsafe(self, property: Property) -> bool:
        return XmlFactory.buildProperties([property],self.properties)

    def getValue(self, key: str) -> ET.Element:
        return findKey(self.values, key)

    def getValueParam(self, key: str, param: str) -> ET.Element:
        return findKey(self.values, key).find(param)

    def hasValue(self, key: str) -> bool:
        return findKey(self.values, key)

    def createValue(self, value: Value) -> bool:
        if findKey(self.values, value.key) is not None:
            raise ValueError(f"{value.key} already exists.")
        return XmlFactory.buildValues((value,),self.values)

    def setValue(self, value: Value) -> bool:
        e = findKey(self.values, value.key)
        if e is None:
            raise ValueError(f"{value.key} doesn't exist.")
        return XmlFactory.modifyValue(value, e)

    def createOSC(self, message: OSC = OSC()) -> ET.Element:
        """Builds and appends an OSC message"""
        # return ControlElements.OSC, message
        return XmlFactory.buildMessages((message,),self.messages)

    def createMIDI(self, message: MIDI = MIDI()) -> ET.Element:
        """Builds and appends a M1D1 message"""
        return XmlFactory.buildMessages((message,),self.messages)

    def createLOCAL(self, message: LOCAL = LOCAL()) -> ET.Element:
        """Builds and appends a LOCAL message"""
        return XmlFactory.buildMessages((message,),self.messages)

    def removeOSC(self) -> bool:
        """Find and remove all OSC messages"""
        [msg.remove for msg in self.messages.findall(ControlElements.OSC.value)]
        return True

    def removeMIDI(self) -> bool:
        """Find and remove all MIDI messages"""
        [msg.remove for msg in self.messages.findall(ControlElements.MIDI.value)]
        return True

    def removeLOCAL(self) -> bool:
        """Find and remove all LOCAL messages"""
        [msg.remove for msg in self.messages.findall(ControlElements.LOCAL.value)]
        return True

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

    def createChild(self, type: controlType) -> ET.Element:
        return XmlFactory.buildNode(type, self.children)

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

    def getColor(self) -> tuple:
        return (self.getR(), self.getG(), self.getB(), self.getA())

    def getR(self):
        return float(self.getPropertyParam("color", "r").text)

    def getG(self):
        return float(self.getPropertyParam("color", "g").text)

    def getB(self):
        return float(self.getPropertyParam("color", "b").text)

    def getA(self):
        return float(self.getPropertyParam("color", "a").text)

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
            return self.createPropertyUnsafe(
                Property(type.value, key, str(value)))

        return wrapper

    def booleanProperty(fun):
        """Pass value as bool, so outline is True"""

        def wrapper(self: "ElementTOSC", value):
            type, key = fun(self)
            element = self.getProperty(key)
            if element is not None:
                self.properties.remove(element)
            return self.createPropertyUnsafe(
                Property(type.value, key, repr(int(value)))
            )

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
                    params={k: repr(params[i])
                            for i, k in enumerate(paramKeys)},
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


def findKey(elements: ET.Element, key: str) -> TypeGuard[ET.Element]:
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


def createTemplate(frame: tuple = None) -> ET.Element:
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
COPY AND MOVE
"""


def copyProperties(source: ElementTOSC, target: ElementTOSC, *args: str):
    """Args can be any number of property keys"""
    if args is None:
        [target.properties.append(deepcopy(e)) for e in source.properties]
        return True
    for arg in args:
        if elements := source.properties.findall(f"*[key='{arg}']"):
            [target.properties.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {args}")
    return True


def moveProperties(source: ElementTOSC, target: ElementTOSC, *args):
    elements = []
    if args is None:
        elements = source.properties
    for arg in args:
        if e := source.properties.findall(f"*[key='{arg}']"):
            elements += e
        else:
            raise ValueError(f"Failed to find all elements with {args}")

    [target.properties.append(deepcopy(e)) for e in elements]
    [source.properties.remove(e) for e in elements]
    return True


def copyValues(source: ElementTOSC, target: ElementTOSC, *args: str):
    """Args can be any number of value keys"""
    if args is None:
        [target.values.append(deepcopy(e)) for e in source.values]
        return True
    for arg in args:
        if elements := source.values.findall(f"*[key='{arg}']"):
            [target.values.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {args}")
    return True


def moveValues(source: ElementTOSC, target: ElementTOSC, *args: str):
    elements = []
    if args is None:
        elements = source.values
    for arg in args:
        if e := source.values.findall(f"*[key='{arg}']"):
            elements += e
        else:
            raise ValueError(f"Failed to find all elements with {args}")

    [target.values.append(deepcopy(e)) for e in elements]
    [source.values.remove(e) for e in elements]
    return True


def copyMessages(source: ElementTOSC, target: ElementTOSC, *args: str):
    """Args can be ControlElements.OSC, MIDI, LOCAL, GAMEPAD"""
    if args is None:
        [target.messages.append(deepcopy(e)) for e in source.messages]
        return True
    for arg in args:
        if elements := source.messages.findall(f"./{arg.value}"):
            [target.messages.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {arg.value}")
    return True


def moveMessages(source: ElementTOSC, target: ElementTOSC, *args: str):
    elements = []
    if args is None:
        elements = source.messages
    for arg in args:
        if e := source.messages.findall(f"./{arg.value}"):
            elements += e
        else:
            raise ValueError(f"Failed to find all elements with {arg.value}")

    [target.messages.append(deepcopy(e)) for e in elements]
    [source.messages.remove(e) for e in elements]
    return True


def copyChildren(source: ElementTOSC, target: ElementTOSC, *args: str):
    """Args can be ControlType.BOX, BUTTON, etc."""
    if args is None:
        [target.children.append(deepcopy(e)) for e in source.children]
        return True
    for arg in args:
        if elements := source.children.findall(
            f"./{ControlElements.NODE.value}[@type='{arg.value}']"
        ):
            [target.children.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {arg.value}")
    return True


def moveChildren(source: ElementTOSC, target: ElementTOSC, *args: str):
    elements = []
    if args is None:
        elements = source.children
    for arg in args:
        if e := source.children.findall(
            f"./{ControlElements.NODE}[@type='{arg.value}']"
        ):
            elements += e
        else:
            raise ValueError(f"Failed to find all elements with {arg.value}")

    [target.children.append(deepcopy(e)) for e in elements]
    [source.children.remove(e) for e in elements]
    return True





"""

GENERAL PARSERS

"""


def pullValueFromKey(inputFile: str, key: str, value: str,
                     targetKey: str) -> str:
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
            if re.fullmatch(getTextValueFromKey(
                    e.find("properties"), key), value):
                parser.close()
                return getTextValueFromKey(e.find("properties"), targetKey)

    parser.close()
    return ""


def pullValueFromKey2(root: ET.Element, key: str,
                      value: str, targetKey: str) -> str:
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

def pullIdfromName(root: ET.Element, name: str) -> str:
    """
    """
    parser = ET.XMLPullParser()
    parser.feed(ET.tostring(root, encoding="UTF-8"))
    for _, e in parser.read_events():  # event, element
        if e.find("properties") is None:
            continue
        # xpath ftw
        if e.find(f"./properties/property/[value='{name}']") is not None:            
            parser.close()
            return e.attrib["ID"]
    
    raise ValueError(f"{name}'s ID wasn't found.")



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
