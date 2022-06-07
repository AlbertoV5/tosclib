"""
Hexler's Enumerations
"""

from dataclasses import dataclass, field
from typing import ClassVar, Final
from .elements import *


@dataclass
class _ControlProperties:
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
    props: List[Property] = field(default_factory=lambda: [])
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
class _BoxProperties:
    shape: int = 0
    """0,1,2,3,4,5 Rectangle, Circle, Triangle, Diamond, Pentagon, Hexagon"""


@dataclass
class _GroupProperties:
    outlineStyle: int = 0
    """0,1,2, = Full, Corner, Edges"""
    grabFocus: bool = False
    """Depends on the control, groups are false"""


@dataclass
class _GridProperties:
    grid: Final[bool] = True
    gridSteps: Final[int] = 10
    """Size of grid"""


@dataclass
class _ResponseProperties:
    response: Final[int] = 0
    """0,1 = Absolute, Relative"""
    responseFactor: Final[int] = 100
    """An integer value ranging from 1 to 100."""


@dataclass
class _CursorProperties:
    cursor: Final[bool] = True
    cursorDisplay: Final[int] = 0
    """Cursor display 0, 1, 2 = always, active, inactive"""


@dataclass
class _LineProperties:
    lines: Final[bool] = 1
    linesDisplay: Final[int] = 0
    """Cursor display 0, 1, 2 = always, active, inactive"""


@dataclass
class _XyProperties:
    lockX: Final[bool] = False
    lockY: Final[bool] = False
    gridX: Final[bool] = True
    gridY: Final[bool] = True
    gridStepsX: Final[int] = 10
    gridStepsY: Final[int] = 10


@dataclass
class _TextProperties:
    font: int = 0
    """0, 1 = default, monospaced"""
    textSize: Final[int] = 14
    """Any int"""
    textColor: Final[list] = field(default_factory=lambda: [1, 1, 1, 1])
    """rgba dict from 0 to 1 as str"""
    textAlignH: Final[int] = 2
    """1,2,3 = left, center, right"""


@dataclass
class BoxProperties(_ControlProperties, _BoxProperties):
    orientation: int = 0
    """0,1,2,3 = North, East, South, West"""


@dataclass
class ButtonProperties(_ControlProperties, _BoxProperties):
    buttonType: Final[int] = 0
    """0,1,2 Momentary, Toggle_Release, Toggle_Press"""
    press: Final[bool] = True
    release: Final[bool] = True
    valuePosition: Final[bool] = False


@dataclass
class LabelProperties(_ControlProperties, _TextProperties):
    textLength: Final[int] = 0
    """0 is infinite length"""
    textClip: Final[bool] = True


@dataclass
class TextProperties(_ControlProperties, _TextProperties):
    pass


@dataclass
class FaderProperties(
    _ControlProperties, _ResponseProperties, _GridProperties, _CursorProperties
):
    bar: Final[bool] = True
    barDisplay: Final[int] = 0


@dataclass
class XyProperties(
    _ControlProperties,
    _ResponseProperties,
    _CursorProperties,
    _XyProperties,
):
    pass


@dataclass
class RadialProperties(
    _ControlProperties,
    _ResponseProperties,
    _GridProperties,
    _CursorProperties,
):
    outlineStyle: int = 0
    """0,1,2, = Full, Corner, Edges"""
    inverted: Final[bool] = False
    centered: Final[bool] = False


@dataclass
class EncoderProperties(_ControlProperties, _ResponseProperties, _GridProperties):
    outlineStyle: int = 0
    """0,1,2, = Full, Corner, Edges"""


@dataclass
class RadarProperties(
    _ControlProperties,
    _CursorProperties,
    _LineProperties,
    _XyProperties,
):
    pass


@dataclass
class RadioProperties(_ControlProperties):
    steps: Final[int] = 5
    """Amount of radio steps"""
    radioType: Final[int] = 0
    """0,1 = select, meter"""
    orientation: int = 0
    """0,1,2,3 = North, East, South, West"""


@dataclass
class GroupProperties(_ControlProperties, _GroupProperties):
    pass


@dataclass
class GridProperties(_ControlProperties):
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


@dataclass
class PagerProperties(_ControlProperties, _GroupProperties):
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
class PageProperties(_ControlProperties, _GroupProperties):
    tabColorOff: Final[list] = field(default_factory=lambda: [0.25, 0.25, 0.25, 1])
    tabColorOn: Final[list] = field(default_factory=lambda: [0, 0, 0, 0])
    tabLabel: Final[str] = "1"
    textColorOff: Final[list] = field(default_factory=lambda: [1, 1, 1, 1])
    textColorOn: Final[list] = field(default_factory=lambda: [1, 1, 1, 1])


@dataclass
class Page:
    controlType: ClassVar[ControlType] = ControlType.GROUP
    properties: PageProperties = field(default_factory=PageProperties())
    values: list = field(default_factory=[])
    messages: list = field(default_factory=[])
    children: list = field(default_factory=[])

    
class Control:
    """All the Control Types and their available properties

    https://hexler.net/touchosc/manual/controls"""

    @classmethod
    def name(cls, value: str):
        return Property(PropertyType.STRING.value, "name", value=value)

    @classmethod
    def tag(cls, value: str):
        return Property(PropertyType.STRING.value, "tag", value=value)

    @classmethod
    def outline(cls, value: bool):
        return Property(PropertyType.BOOLEAN.value, "outline", value=str(int(value)))

    @dataclass
    class Box:
        controlType: ClassVar[ControlType] = ControlType.BOX
        properties: BoxProperties = field(default_factory=BoxProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])

    @dataclass
    class Button:
        controlType: ClassVar[ControlType] = ControlType.BUTTON
        properties: ButtonProperties = field(default_factory=ButtonProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])

    @dataclass
    class Label:
        controlType: ClassVar[ControlType] = ControlType.LABEL
        properties: LabelProperties = field(default_factory=LabelProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])

    @dataclass
    class Text:
        controlType: ClassVar[ControlType] = ControlType.TEXT
        properties: TextProperties = field(default_factory=TextProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])

    @dataclass
    class Fader:
        controlType: ClassVar[ControlType] = ControlType.FADER
        properties: FaderProperties = field(default_factory=FaderProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])

    @dataclass
    class Xy:
        controlType: ClassVar[ControlType] = ControlType.XY
        properties: XyProperties = field(default_factory=XyProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])

    @dataclass
    class Radial:
        controlType: ClassVar[ControlType] = ControlType.RADIAL
        properties: RadialProperties = field(default_factory=RadialProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])

    @dataclass
    class Encoder:
        controlType: ClassVar[ControlType] = ControlType.ENCODER
        properties: EncoderProperties = field(default_factory=EncoderProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])

    @dataclass
    class Radar:
        controlType: ClassVar[ControlType] = ControlType.RADAR
        properties: RadarProperties = field(default_factory=RadarProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])

    @dataclass
    class Radio:
        controlType: ClassVar[ControlType] = ControlType.RADIO
        properties: RadioProperties = field(default_factory=RadioProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])

    @dataclass
    class Group:
        controlType: ClassVar[ControlType] = ControlType.GROUP
        properties: GroupProperties = field(default_factory=GroupProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])
        children: list = field(default_factory=[])

    @dataclass
    class Grid:
        controlType: ClassVar[ControlType] = ControlType.GRID
        properties: GridProperties = field(default_factory=GridProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])
        children: list = field(default_factory=[])

    @dataclass
    class Pager:
        controlType: ClassVar[ControlType] = ControlType.PAGER
        properties: PagerProperties = field(default_factory=PagerProperties())
        values: list = field(default_factory=[])
        messages: list = field(default_factory=[])
        children: list = field(default_factory=[])


    @classmethod
    def hasChildren(cls):
        return (cls.Grid, cls.Group, cls.Pager)
