"""
Simplify navigating, editing and generating .tosc files.
"""
import sys
import xml.etree.ElementTree as ET
import re
import zlib
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto, unique
from typing import List, Final


@unique
class ControlElements(Enum):
    """Valid Sub Elements for a Node"""

    PROPERTIES = "properties"
    VALUES = "values"
    MESSAGES = "messages"
    CHILDREN = "children"
    # Sub Elements
    PROPERTY = "property"
    VALUE = "value"
    # Messages
    OSC = "osc"
    MIDI = "midi"
    LOCAL = "local"
    GAMEPAD = "gamepad"
    # Children
    CHILD = "node"


@dataclass
class Property:
    """Element structure for a <property>

    Args:
        type (str): See PropertyType.
        key (str): See parameters of inner classes of Controls.
        value (str, optional): Exclusive with params.
        params (dict[str,str], optional): Exclusive with value.
    """

    type: str
    key: str
    value: str = ""
    params: dict = field(default_factory=lambda: {})

    def __post_init__(self):
        if self.value and self.params:
            raise ValueError(f"{self} can't have both value and params.")
        if not self.value and not self.params:
            raise ValueError(f"{self} needs either a value or params.")


@dataclass
class Value:
    """Default Elements for <value>.

    Args:
        key (str, optional): "x" or "touch". Defaults to "touch".
        locked (str, optional): boolean. Defaults to "0".
        lockedDefaultCurrent (str, optional): boolean. Defaults to "0".
        default (str, optional): float or boolean. Defaults to "false".
        defaultPull (str, optional): 0 to 100. Defaults to "0".
    """

    key: str = "touch"
    locked: str = "0"
    lockedDefaultCurrent: str = "0"
    default: str = "false"
    defaultPull: str = "0"


@dataclass
class Partial:
    """Default Elements for <partial>

    Args:
        type (str, optional): "CONSTANT", "INDEX", "VALUE", "PROPERTY". Defaults to "CONSTANT".
        conversion (str, optional): "BOOLEAN", "INTEGER", "FLOAT", "STRING". Defaults to "STRING".
        value (str, optional): Depends on the context. Defaults to "/".
        scaleMin (str, optional): If "VALUE", set range. Defaults to "0".
        scaleMax (str, optional): If "VALUE", set range. Defaults to "1".
    """

    type: str = "CONSTANT"
    conversion: str = "STRING"
    value: str = "/"
    scaleMin: str = "0"
    scaleMax: str = "1"


@dataclass
class Trigger:
    """Default Elements for <trigger>

    Args:
        var (str, optional): "x" or "touch". Defaults to "x".
        con (str, optional): "ANY", "RISE" or "FALL". Defaults to "ANY".
    """

    var: str = "x"
    condition: str = "ANY"


@dataclass
class OSC:
    """Default Elements and Sub Elements for <osc>

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

    enabled: str = "1"
    send: str = "1"
    receive: str = "1"
    feedback: str = "0"
    connections: str = "00001"
    triggers: List[Trigger] = field(default_factory=lambda: [Trigger()])
    path: List[Partial] = field(
        default_factory=lambda: [Partial(), Partial(type="PROPERTY", value="name")]
    )
    arguments: List[Partial] = field(
        default_factory=lambda: [Partial(type="VALUE", conversion="FLOAT", value="x")]
    )


@unique
class PropertyType(Enum):
    """Enum of valid <property type=?>"""

    STRING = "s"
    BOOLEAN = "b"
    INTEGER = "i"
    FLOAT = "f"
    FRAME = "r"
    COLOR = "c"


@unique
class textAlignH(Enum):
    LEFT = "0"
    CENTER = "1"
    RIGHT = "2"


@unique
class textAlignV(Enum):
    TOP = "0"
    MIDDLE = "1"
    BOTTOM = "2"


@unique
class buttonType(Enum):
    MOMENTARY = "0"
    TOGGLE_RELEASE = "1"
    TOGGLE_PRESS = "2"


@unique
class ControlType(Enum):
    """Enum of valid <node type=?>"""

    BOX = "BOX"
    BUTTON = "BUTTON"
    LABEL = "LABEL"
    TEXT = "TEXT"
    FADER = "FADER"
    XY = "XY"
    RADIAL = "RADIAL"
    ENCODER = "ENCODER"
    RADAR = "RADAR"
    RADIO = "RADIO"
    GROUP = "GROUP"
    PAGER = "PAGER"
    GRID = "GRID"


@unique
class cursorDisplay(Enum):
    ALWAYS = "0"
    ACTIVE = "1"
    INACTIVE = "2"


@unique
class font(Enum):
    DEFAULT = "0"
    MONOSPACED = "1"


@unique
class orientation(Enum):
    NORTH = "0"
    EAST = "1"
    SOUTH = "2"
    WEST = "3"


@unique
class outlineStyle(Enum):
    FULL = "0"
    CORNERS = "1"
    EDGES = "2"


@unique
class pointerPriority(Enum):
    OLDEST = "0"
    NEWEST = "1"


@unique
class response(Enum):
    ABSOLUTE = "0"
    RELATIVE = "1"


@unique
class shape(Enum):
    RECTANGLE = "0"
    CIRCLE = "1"
    TRIANGLE = "2"
    DIAMOND = "3"
    PENTAGON = "4"
    HEXAGON = "5"


class _PropertyKeys:
    """All controls have these properties
    https://hexler.net/touchosc/manual/script-properties-and-values"""

    NAME: Final[str] = "name"
    TAG: Final[str] = "tag"
    FRAME: Final[str] = "frame"
    COLOR: Final[str] = "color"
    LOCKED: Final[str] = "locked"
    VISIBLE: Final[str] = "visible"
    INTERACTIVE: Final[str] = "interactive"
    BACKGROUND: Final[str] = "background"
    OUTLINE: Final[str] = "outline"
    OUTLINE_STYLE: Final[str] = outlineStyle.__name__
    GRAB_FOCUS: Final[str] = "grabFocus"
    POINTER: Final[str] = pointerPriority.__name__
    CORNER: Final[str] = "cornerRadius"
    ORIENTATION: Final[str] = orientation.__name__
    SCRIPT: Final[str] = "script"


class _PropertiesBox:
    SHAPE: Final[str] = shape.__name__


class _PropertiesGrid:
    GRID: Final[str] = "grid"
    GRID_STEPS: Final[str] = "gridSteps"


class _PropertiesResponse:
    RESPONSE: Final[str] = response.__name__
    RESPONSE_FACTOR: Final[str] = "responseFactor"


class _PropertiesCursor:
    CURSOR: Final[str] = "cursor"
    CURSOR_DISPLAY: Final[str] = cursorDisplay.__name__


class _PropertiesLine:
    LINES: Final[str] = "lines"
    LINES_DISPLAY: Final[str] = "linesDisplay"


class _PropertiesXY:
    LOCK_X: Final[str] = "lockX"
    LOCK_Y: Final[str] = "lockY"
    GRID_X: Final[str] = "gridX"
    GRID_Y: Final[str] = "gridY"
    GRID_STEPSX: Final[str] = "gridStepsX"
    GRID_STEPSY: Final[str] = "gridStepsY"


class _PropertiesText:
    FONT: Final[str] = "font"
    SIZE: Final[str] = "textSize"
    ALIGNMENT_H: Final[str] = "textAlignH"
    TEXT_COLOR: Final[str] = "textColor"


class Controls:
    """All the Node Types and their available properties

    https://hexler.net/touchosc/manual/script-enumerations#controltype"""

    class BOX(_PropertyKeys, _PropertiesBox):
        pass

    class BUTTON(_PropertyKeys, _PropertiesBox):
        BUTTON_TYPE = buttonType.__name__
        PRESS = "press"
        RELEASE = "release"
        VALUE_POSITION = "valuePosition"

    class LABEL(_PropertyKeys, _PropertiesText):
        LENGTH = "textLength"
        CLIP = "textClip"

    class TEXT(_PropertyKeys, _PropertiesText):
        pass

    class FADER(_PropertyKeys, _PropertiesResponse, _PropertiesGrid, _PropertiesCursor):
        BAR = "bar"
        BAR_DISPLAY = "barDisplay"

    class XY(
        _PropertyKeys,
        _PropertiesResponse,
        _PropertiesCursor,
        _PropertiesXY,
    ):
        pass

    class RADIAL(
        _PropertyKeys,
        _PropertiesResponse,
        _PropertiesGrid,
        _PropertiesCursor,
    ):
        INVERTED = "inverted"
        CENTERED = "centered"

    class ENCODER(_PropertyKeys, _PropertiesResponse, _PropertiesGrid):
        pass

    class RADAR(
        _PropertyKeys,
        _PropertiesCursor,
        _PropertiesLine,
        _PropertiesXY,
    ):
        pass

    class RADIO(_PropertyKeys):
        STEPS = "steps"
        RADIO_TYPE = "radioType"
        pass

    class GROUP(_PropertyKeys):
        pass

    class PAGER(_PropertyKeys):
        TAB_LABELS = "tabLabels"
        TAB_BAR = "tabbar"
        DOUBLE_TAP = "tabbarDoubleTap"
        TAB_BAR_SIZE = "tabbarSize"
        TEXT_SIZE_OFF = "textSizeOff"
        TEXT_SIZE_ON = "textSizeOn"
        pass

        class PAGE(_PropertyKeys):
            TAB_COLOR_OFF = "tabColorOff"
            TAB_COLOR_ON = "tabColorOn"
            TAB_LABEL = "tabLabel"
            TEXT_COLOR_OFF = "textColorOff"
            TEXT_COLOR_ON = "textColorOn"

    class GRID(_PropertyKeys):
        EXCLUSIVE = "exclusive"
        GRID_NAMING = "gridNaming"
        GRID_ORDER = "gridOrder"
        GRID_START = "gridStart"
        GRID_TYPE = "gridType"
        GRID_X = "gridX"
        GRID_Y = "gridY"

    @classmethod
    def hasChildren(cls):
        return (cls.GRID, cls.GROUP, cls.PAGER)


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
        self.properties = f(ControlElements.PROPERTIES.value)
        self.values = f(ControlElements.VALUES.value)
        self.messages = f(ControlElements.MESSAGES.value)
        self.children = f(ControlElements.CHILDREN.value)

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
        if not self.hasProperty(key):
            raise ValueError(f"{key} doesn't exist.")
        val = self.getPropertyValue(key)
        if value:
            val.text = value
            return True
        for paramKey in params:
            val.find(paramKey).text = params[paramKey]
        return True

    def createProperty(self, property: Property) -> bool:
        if self.hasProperty(property.key):
            raise ValueError(f"{property.key} already exists.")
        prop = ET.SubElement(
            self.properties,
            ControlElements.PROPERTY.value,
            attrib={"type": property.type},
        )
        (key, value) = (ET.SubElement(prop, "key"), ET.SubElement(prop, "value"))
        key.text = property.key
        if property.value:
            value.text = property.value
            return True
        for paramKey in property.params:
            ET.SubElement(value, paramKey).text = property.params[paramKey]
        return True

    def getValue(self, key: str) -> ET.Element:
        return findKey(self.values, key)

    def getValueParam(self, key: str, param: str) -> ET.Element:
        return findKey(self.values, key).find(param)

    def hasValue(self, key: str) -> bool:
        return True if findKey(self.values, key) else False

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

    def createOSC(self, message: OSC = OSC()) -> ET.Element:
        osc = ET.SubElement(self.messages, ControlElements.OSC.value)
        for key in vars(message):
            element = ET.SubElement(osc, key)
            attribute = getattr(message, key)
            if isinstance(attribute, list):  # For Partials and Triggers
                for partialOrTrigger in attribute:
                    subElement = ET.SubElement(
                        element, type(partialOrTrigger).__name__.lower()
                    )  # Create <partial> or <trigger>
                    for v in vars(partialOrTrigger):  # Attributes of Partials/Triggers
                        ET.SubElement(subElement, v).text = getattr(partialOrTrigger, v)
            else:
                element.text = getattr(message, key)
        return osc

    def findChildByName(self, name: str) -> ET.Element:
        for child in self.children:
            if not child.find(ControlElements.PROPERTIES.value):
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
            ControlElements.CHILD.value,
            attrib={"ID": str(uuid.uuid4()), "type": type},
        )

    #
    #
    #   SHORTCUTS:
    #
    #
    def overrideProperty(
        self, type: str, key: str, value: str = "", params: dict = {}
    ) -> bool:
        """Create a Property, if already exists, then modify its values."""
        if not self.hasProperty(key):
            return self.createProperty(Property(type, key, value=value, params=params))
        return self.setProperty(key, value=value, params=params)

    def setType(self, value: str):
        """See ControlType Element"""
        self.node.attrib = {"type": value}
        return True

    def setName(self, value: str):
        return self.overrideProperty(
            PropertyType.STRING.value, _PropertyKeys.NAME, value=value
        )

    def setTag(self, value: str):
        return self.overrideProperty(
            PropertyType.STRING.value, _PropertyKeys.TAG, value=value
        )

    def setFrame(self, x: float, y: float, w: float, h: float):
        return self.overrideProperty(
            PropertyType.FRAME.value,
            _PropertyKeys.FRAME,
            params={"x": str(x), "y": str(y), "w": str(w), "h": str(h)},
        )

    def setColor(self, r: float, g: float, b: float, a: float):
        return self.overrideProperty(
            PropertyType.COLOR.value,
            _PropertyKeys.COLOR,
            params={"r": str(r), "g": str(g), "b": str(b), "a": str(a)},
        )

    def setLocked(self, value: bool):
        return self.overrideProperty(
            PropertyType.BOOLEAN, _PropertyKeys.LOCKED, str(int(value))
        )

    def setBackground(self, value: bool):
        return self.overrideProperty(
            PropertyType.BOOLEAN.value, _PropertyKeys.BACKGROUND, value=str(int(value))
        )

    def setVisible(self, value: bool):
        return self.overrideProperty(
            PropertyType.BOOLEAN.value, _PropertyKeys.VISIBLE, value=str(int(value))
        )

    def setInteractive(self, value: bool):
        return self.overrideProperty(
            PropertyType.BOOLEAN, _PropertyKeys.INTERACTIVE, value=str(int(value))
        )

    def setOutline(self, value: bool):
        return self.overrideProperty(
            PropertyType.BOOLEAN, _PropertyKeys.OUTLINE, value=value
        )

    def setScript(self, value: str):
        return self.overrideProperty(
            PropertyType.STRING.value, _PropertyKeys.SCRIPT, value=value
        )

    def show(self):
        showElement(self.node)

    def showProperty(self, name: str):
        showElement(findKey(self.properties, name))

    def showValue(self, name: str):
        showElement(findKey(self.values, name))

###
#
#   GLOBAL FUNCTIONS
#
###

def findKey(elements: ET.Element, key: str) -> ET.Element:
    """Iterate through element with children and return child whose key matches"""
    for e in elements:
        if re.fullmatch(e.find("key").text, key):
            return e
    return None


def showElement(e: ET.Element):
    """Generic show function, UTF-8, indented 2 spaces"""
    if sys.version_info[0] == 3 and sys.version_info[1] >= 9:
        ET.indent(e, "  ")
    print(ET.tostring(e).decode("utf-8"))


def createTemplate() -> ET.Element:
    """Generates a root Element for your .tosc file"""
    root = ET.Element("lexml", attrib={"version": "3"})
    ET.SubElement(
        root,
        ControlElements.CHILD.value,
        attrib={"ID": str(uuid.uuid4()), "type": ControlType.GROUP.value},
    )
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


def getTextValueFromKey(properties: ET.Element, key: str) -> str:
    """Find the value.text from a known key"""
    for property in properties:
        if re.fullmatch(property.find("key").text, key):
            return property.find("value").text


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
            if not e.find("properties"):
                continue
            if re.fullmatch(getTextValueFromKey(e.find("properties"), key), value):
                parser.close()
                return getTextValueFromKey(e.find("properties"), targetKey)

    parser.close()
    return ""

def pullValueFromKey2(root: ET.Element, key : str, value : str, targetKey : str) -> str:
    """If you know the name of an element but don't know its other properties.

    Args:
        root (ET.Element): Parses the whole element, so you can feed the root.
        key (str): Known key.
        value (str): Known value.
        targetKey (str): Known key of unknown value.

    Returns:
        str: Value
    """
    parser = ET.XMLPullParser()
    parser.feed(ET.tostring(root, encoding = "UTF-8"))
    for _, e in parser.read_events():  # event, element
        if not e.find("properties"):
            continue
        if re.fullmatch(getTextValueFromKey(e.find("properties"), key), value):
            parser.close()
            return getTextValueFromKey(e.find("properties"), targetKey)