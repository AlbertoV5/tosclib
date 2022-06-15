"""
Hexler's Controls
"""

from dataclasses import dataclass, field
from typing import Final, Literal
import uuid
from .elements import *


class ControlBuilder:
    def __init__(
        self,
        type: ControlType,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        children: Children = None,
        **kwargs: Property,
    ):
        """Default factory for Control. Not an XML Element.

        Args:
            type (ControlType): Required field. ControlType Literal.
            id (str, optional): Random uuid4. Defaults to None.
            values (Values, optional): Tuple of Value objects. Defaults to None.
            messages (Messages, optional): Tuple of Message objects. Defaults to None.
            children (tuple[&quot;Node&quot;], optional): Tuple of Node objects. Defaults to None.
            kwargs (Property): Pass any extra Property types as keyword arguments.

        Example (using a subclass of ControlBuilder):

            class Box(ControlBuilder):
                type: ControlType = "BOX"
                ...

            box = Box(name = ("name", "boxy")) # with kwargs only

            assert box.name == ("name", "boxy")
            assert box.type == "BOX"
        """
        self.id: str = str(uuid.uuid4()) if id is None else id
        self.type: ControlType = type
        self.values: Values = [] if values is None else values
        self.messages: Messages = [] if messages is None else messages
        self.children: Children = [] if children is None else children

        for k in kwargs:
            setattr(self, k, kwargs[k])

    def __repr__(self):
        return str(tuple((getattr(self, p) for p in vars(self))))

    def print(self):
        print("Control:")
        print(f"\t{self.type}, {self.id}")
        print("Values:")
        for v in self.values:
            print(f"\t{v}")
        print("Properties:")
        for p in vars(self):
            if p not in ("id", "type", "values", "messages", "children"):
                print(f"\t{getattr(self, p)}")
        print("Messages:")
        for m in self.messages:
            print(f"\t{m}")
        print("Children:")
        print(self.children)


class Box(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        **kwargs: Property,
    ):
        super().__init__("BOX", id, values, messages, None, **kwargs)


class Button(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        **kwargs: Property,
    ):
        super().__init__("BUTTON", id, values, messages, None, **kwargs)


class Encoder(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        **kwargs: Property,
    ):
        super().__init__("ENCODER", id, values, messages, None, **kwargs)


class Fader(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        **kwargs: Property,
    ):
        super().__init__("FADER", id, values, messages, None, **kwargs)


class Grid(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        children: Children = None,
        **kwargs: Property,
    ):
        super().__init__("GRID", id, values, messages, children, **kwargs)


class Group(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        children: Children = None,
        **kwargs: Property,
    ):
        super().__init__("GROUP", id, values, messages, children, **kwargs)


class Label(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        **kwargs: Property,
    ):
        super().__init__("LABEL", id, values, messages, None, **kwargs)


class Page(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        children: Children = None,
        **kwargs: Property,
    ):
        super().__init__("GROUP", id, values, messages, children, **kwargs)


class Pager(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        children: Children = None,
        **kwargs: Property,
    ):
        children = Children([Page(), Page(), Page()]) if children is None else children
        super().__init__("PAGER", id, values, messages, children, **kwargs)


class Radial(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        **kwargs: Property,
    ):
        super().__init__("RADIAL", id, values, messages, None, **kwargs)


class Radar(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        **kwargs: Property,
    ):
        super().__init__("RADAR", id, values, messages, None, **kwargs)


class Radio(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        **kwargs: Property,
    ):
        super().__init__("RADIO", id, values, messages, None, **kwargs)


class Text(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        **kwargs: Property,
    ):
        super().__init__("TEXT", id, values, messages, None, **kwargs)


class Xy(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        **kwargs: Property,
    ):
        super().__init__("XY", id, values, messages, None, **kwargs)


def get_prop(control: Control, key: str) -> Property:
    """Get the Property of a Control"""
    if (p:=getattr(control, key)) is not None:
        return (key, p[1])
    raise KeyError(f"{p} is not a valid Property.")


def set_prop(control: Control, property: Property) -> Control:
    """Set the Property of a Control"""
    setattr(control, property[0], property)
    return control


def get_value(control: Control, key: str) -> Value | None:
    """Get the Value of a Control"""
    for v in control.values:
        if v[0] == key:
            return v
    return None


def set_value(control: Control, value: Value) -> Control:
    """Set the Value of a Control"""
    for i, v in enumerate(control.values):
        if v[0] == value[0]:
            control.values[i] = value
    return control


def get_msglist(control: Control, key: Literal["osc", "midi", "local"]) -> Messages:
    """Get all messages of the same type, osc, midi, etc."""
    msgs: Messages = []
    for v in control.messages:
        if v[0] == key:
            msgs.append(v)
    return msgs


def set_msglist(
    control: Control, key: Literal["osc", "midi", "local"], msgs: Messages
) -> Control:
    """Set all messages of the same type, osc, midi, etc."""
    for i, v in enumerate(control.messages.copy()):
        if v[0] == key:
            control.messages.pop(i)
    for m in msgs:
        control.messages.append(m)
    return control


""" DEPRECATED?? """


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
    frame: Final[tuple] = field(default_factory=lambda: (0, 0, 100, 100))
    """x,y,w,h float list"""
    color: Final[tuple] = field(default_factory=lambda: (0.25, 0.25, 0.25, 1.0))
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

    # def build(self, *args) -> Properties:
    #     """Build all Property objects of this class.
    #     Returns:
    #         list[Property] from this class' attributes.
    #     """
    #     if len(args) == 0:
    #         args = tuple(key for key in vars(self))

    #     return [PropertyFactory.buildAny(arg, getattr(self, arg)) for arg in args]


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
    lines: Final[bool] = True
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
    textColor: Final[tuple] = field(default_factory=lambda: (1, 1, 1, 1))
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

    tabLabels: Final[bool] = True
    tabbar: Final[bool] = True
    tabbarDoubleTap: Final[bool] = False
    tabbarSize: Final[int] = 40
    """int from 10 to 300"""
    textSizeOff: Final[int] = 14
    """font size any int"""
    textSizeOn: Final[int] = 14
    """font size any int"""


@dataclass
class PageProperties(_ControlProperties, _GroupProperties):
    tabColorOff: Final[tuple] = field(default_factory=lambda: (0.25, 0.25, 0.25, 1.0))
    tabColorOn: Final[tuple] = field(default_factory=lambda: (0, 0, 0, 0))
    tabLabel: Final[str] = "1"
    textColorOff: Final[tuple] = field(default_factory=lambda: (1, 1, 1, 1))
    textColorOn: Final[tuple] = field(default_factory=lambda: (1, 1, 1, 1))
