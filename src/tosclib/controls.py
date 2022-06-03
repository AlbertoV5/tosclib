"""
Hexler Enumerations as Controls
"""

from dataclasses import dataclass, field
from typing import Final
from .elements import *


@dataclass
class Properties:
    """Common properties across all Control Types
    https://hexler.net/touchosc/manual/script-properties-and-values"""

    name: Final[str] = " "
    """Any string"""
    tag: Final[str] = "tag"
    """Any string"""
    script: Final[str] = " "
    """Any string"""
    frame: Final[list] = field(default_factory=lambda: [0, 0, 100, 100])
    """x,y,w,h float list"""
    color: Final[list] = field(default_factory=lambda: [0.25, 0.25, 0.25, 1.0])
    """r,g,b,a float list"""
    locked: Final[bool] = False
    visible: Final[bool] = True
    interactive: Final[bool] = True
    background: Final[bool] = True
    outline: Final[bool] = True
    outlineStyle: int = 1
    """0,1,2, = Full, Corner, Edges"""
    grabFocus: bool = True
    """Depends on the control, groups are false"""
    pointerPriority: Final[int] = 0
    """0,1 = Oldest, Newest"""
    cornerRadius: Final[float] = 0.0
    """An integer number value ranging from 0 to 10"""
    orientation: int = 0
    """0,1,2,3 = North, East, South, West"""
    props: list = field(default_factory=lambda: [])
    """Use build to populate this dict"""

    def build(self, *args) -> bool:
        """Use attributes to create Property Elements.
        Pass args to chose which Properties to build.
        Any Properties built will be stored in the props attribute.

        Returns:
            Stores tuple in self.props"""
        if args is None:
            raise ValueError(f"No args found. Pass 'all' for building all.")
        elif "all" in args:
            args = [key for key in vars(self) if key != "props"]

        for key in args:
            value = getattr(self, key)
            if type(value) is list and key == "frame":
                prop = Property(
                    PropertyType.FRAME,
                    key,
                    "",
                    {
                        "x": str(value[0]),
                        "y": str(value[1]),
                        "w": str(value[2]),
                        "h": str(value[3]),
                    },
                )
            elif type(value) is list and key != "frame":
                prop = Property(
                    PropertyType.COLOR,
                    key,
                    "",
                    {
                        "r": str(value[0]),
                        "g": str(value[1]),
                        "b": str(value[2]),
                        "a": str(value[3]),
                    },
                )
            elif type(value) is int:
                prop = Property(PropertyType.INTEGER, key, str(value))
            elif type(value) is bool:
                prop = Property(PropertyType.BOOLEAN, key, (str(int(value))))
            elif type(value) is float:
                prop = Property(PropertyType.FLOAT, key, str(value))
            elif type(value) is str:
                prop = Property(PropertyType.STRING, key, str(value))
            else:
                raise TypeError(f"{key}, {type(key)}, is not compatible.")
            # self.props[key] = prop

            self.props.append(prop)

        self.props = tuple(self.props)
        return True


@dataclass
class PropertiesBox:
    shape: int = 0
    """0,1,2,3,4,5 Rectangle, Circle, Triangle, Diamond, Pentagon, Hexagon"""


@dataclass
class PropertiesGroup:
    outlineStyle: int = 0
    """0,1,2, = Full, Corner, Edges"""
    grabFocus: bool = False
    """Depends on the control, groups are false"""


@dataclass
class PropertiesGrid:
    grid: Final[bool] = True
    gridSteps: Final[int] = 10
    """Size of grid"""


@dataclass
class PropertiesResponse:
    response: Final[int] = 0
    """0,1 = Absolute, Relative"""
    responseFactor: Final[int] = 100
    """An integer value ranging from 1 to 100."""


@dataclass
class PropertiesCursor:
    cursor: Final[bool] = True
    cursorDisplay: Final[int] = 0
    """Cursor display 0, 1, 2 = always, active, inactive"""


@dataclass
class PropertiesLine:
    lines: Final[bool] = 1
    linesDisplay: Final[int] = 0
    """Cursor display 0, 1, 2 = always, active, inactive"""


@dataclass
class PropertiesXY:
    lockX: Final[bool] = False
    lockY: Final[bool] = False
    gridX: Final[bool] = True
    gridY: Final[bool] = True
    gridStepsX: Final[int] = 10
    gridStepsY: Final[int] = 10


@dataclass
class PropertiesText:
    font: int = 0
    """0, 1 = default, monospaced"""
    textSize: Final[int] = 14
    """Any int"""
    textColor: Final[list] = field(default_factory=lambda: [1, 1, 1, 1])
    """rgba dict from 0 to 1 as str"""
    textAlignH: Final[int] = 2
    """1,2,3 = left, center, right"""


class Control:
    """All the Control Types and their available properties

    https://hexler.net/touchosc/manual/controls"""

    @dataclass
    class Box(Properties, PropertiesBox):
        orientation: int = 0
        """0,1,2,3 = North, East, South, West"""

    @dataclass
    class Button(Properties, PropertiesBox):
        buttonType: Final[int] = 0
        """0,1,2 Momentary, Toggle_Release, Toggle_Press"""
        press: Final[bool] = True
        release: Final[bool] = True
        valuePosition: Final[bool] = False

    @dataclass
    class Label(Properties, PropertiesText):
        textLength: Final[int] = 0
        """0 is infinite length"""
        textClip: Final[bool] = True

    @dataclass
    class Text(Properties, PropertiesText):
        pass

    @dataclass
    class Fader(Properties, PropertiesResponse, PropertiesGrid, PropertiesCursor):
        bar: Final[bool] = True
        barDisplay: Final[int] = 0
        """Cursor display 0, 1, 2 = always, active, inactive"""

    @dataclass
    class Xy(
        Properties,
        PropertiesResponse,
        PropertiesCursor,
        PropertiesXY,
    ):
        pass

    @dataclass
    class Radial(
        Properties,
        PropertiesResponse,
        PropertiesGrid,
        PropertiesCursor,
    ):
        outlineStyle: int = 0
        """0,1,2, = Full, Corner, Edges"""
        inverted: Final[bool] = False
        centered: Final[bool] = False

    @dataclass
    class Encoder(Properties, PropertiesResponse, PropertiesGrid):
        outlineStyle: int = 0
        """0,1,2, = Full, Corner, Edges"""

    @dataclass
    class Radar(
        Properties,
        PropertiesCursor,
        PropertiesLine,
        PropertiesXY,
    ):
        pass

    @dataclass
    class Radio(Properties):
        steps: Final[int] = 5
        """Amount of radio steps"""
        radioType: Final[int] = 0
        """0,1 = select, meter"""
        orientation: int = 0
        """0,1,2,3 = North, East, South, West"""

    @dataclass
    class Group(Properties, PropertiesGroup):
        pass

    @dataclass
    class Pager(Properties):
        grabFocus: bool = False
        """Depends on the control, groups are false"""
        outlineStyle: int = 0
        """0,1,2, = Full, Corner, Edges"""
        tabLabels: Final[bool] = 1
        tabbar: Final[bool] = 1
        tabbarDoubleTap: Final[bool] = 0
        tabbarSize: Final[int] = 40
        """int from 10 to 300"""
        textSizeOff: Final[int] = 14
        """font size any int"""
        textSizeOn: Final[int] = 14
        """font size any int"""

    @dataclass
    class Page(Properties):
        tabColorOff: Final[list] = field(default_factory=lambda: [0.25, 0.25, 0.25, 1])
        tabColorOn: Final[list] = field(default_factory=lambda: [0, 0, 0, 0])
        tabLabel: Final[str] = "1"
        textColorOff: Final[list] = field(default_factory=lambda: [1, 1, 1, 1])
        textColorOn: Final[list] = field(default_factory=lambda: [1, 1, 1, 1])

    @dataclass
    class Grid(Properties):
        grabFocus: bool = False
        """Depends on the control, groups are false"""
        exclusive: bool = False
        gridNaming: Final[int] = 0
        """0,1,2 = Index, Column, Row"""
        gridOrder: Final[int] = 0
        """0,1 = Row, Column"""
        gridStart: Final[int] = 0
        """0,1,2,3 = Top left, Top right, Bottom Left, Bottom Right"""
        gridType: Final[int] = 4
        """0,1,2,3,4,5,6,7,8 See ControlType, can't hold groups"""
        gridX: Final[int] = 2
        """amount of elements on X"""
        gridY: Final[int] = 2
        """amount of elements on Y"""

    @classmethod
    def hasChildren(cls):
        return (cls.Grid, cls.Group, cls.Pager)

    class _PropertyParser:
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
            if tag == ControlElements.NODE:
                self.index += 1
                self.node = True
                self.targetList.append({arg: "" for arg in [*self.args]})
            elif self.node and tag == ControlElements.PROPERTY:
                self.property = True
            elif self.property and tag == Property.Elements.KEY:
                self.key = True
            elif self.property and tag == Property.Elements.VALUE:
                self.value = True

        def end(self, tag):
            if tag == ControlElements.NODE:
                self.node = False
            elif self.node and tag == ControlElements.PROPERTY:
                self.property = False
            elif self.property and tag == Property.Elements.KEY:
                self.key = False
            elif self.property and tag == Property.Elements.VALUE:
                self.value = False

            if self.targetFound and tag == Property.Elements.VALUE:
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

    @classmethod
    def parseProperties(cls, node: ET.Element, *args) -> list:
        """
        Specify all properties you want to find and this will parse
        the entire Node and its children and return a list of key value pairs.

        For example:

        >>>Control.parseProperties(node, "name", "script")

        [{"name":"control1", "script":"scriptContent1"},
        {"name":"control2", "script":""},
        {"name":"control3", "script":"scriptContent3"}]

        Args:
            node (ET.Element): Node element to parse.

        Returns:
            List[dict]: [{arg: "" for arg in [args]}]
        """
        target = cls._PropertyParser(*args)
        line = ET.tostring(node, encoding="UTF-8")
        parser = ET.XMLParser(target=target)
        parser.feed(line)
        return parser.close()
