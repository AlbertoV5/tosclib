"""
Hexler's Enumerations
"""

from copy import deepcopy
from dataclasses import dataclass, field
from typing import ClassVar, Final, Protocol, TypeAlias
import uuid
from .elements import (
    MidiMessage,
    Property,
    Value,
    OSC,
    MIDI,
    LOCAL,
    PropertyFactory,
    controlType,
    ControlType,
    ControlElements,
)

# import xml.etree.ElementTree as ET
from lxml import etree as ET

Properties: TypeAlias = list[Property]
Values: TypeAlias = list[Value]
Message: TypeAlias = OSC | MIDI | LOCAL
Messages: TypeAlias = list[OSC | MIDI | LOCAL]


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

    def build(self, *args) -> list[Property]:
        """Build all Property objects of this class.
        Returns:
            list[Property] from this class' attributes.
        """
        if len(args) == 0:
            args = [key for key in vars(self)]

        return tuple(PropertyFactory.build(arg, getattr(self, arg)) for arg in args)


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
    tabColorOff: Final[tuple] = field(default_factory=lambda: (0.25, 0.25, 0.25, 1))
    tabColorOn: Final[list] = field(default_factory=lambda: (0, 0, 0, 0))
    tabLabel: Final[str] = "1"
    textColorOff: Final[list] = field(default_factory=lambda: (1, 1, 1, 1))
    textColorOn: Final[list] = field(default_factory=lambda: (1, 1, 1, 1))


@dataclass
class Page:
    """Not a main control"""

    controlT: ClassVar[controlType] = ControlType.GROUP
    properties: Properties = field(default_factory=PageProperties())
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list[controlType] = field(default_factory=lambda: [])


@dataclass
class Box:
    controlT: ClassVar[controlType] = ControlType.BOX
    properties: Properties = field(default_factory=lambda: BoxProperties().build())
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])


@dataclass
class Button:
    controlT: ClassVar[controlType] = ControlType.BUTTON
    properties: Properties = field(
        default_factory=lambda: ButtonProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])


@dataclass
class Label:
    controlT: ClassVar[controlType] = ControlType.LABEL
    properties: Properties = field(
        default_factory=lambda: LabelProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])


@dataclass
class Text:
    controlT: ClassVar[controlType] = ControlType.TEXT
    properties: Properties = field(
        default_factory=lambda: TextProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])


@dataclass
class Fader:
    controlT: ClassVar[controlType] = ControlType.FADER
    properties: Properties = field(
        default_factory=lambda: FaderProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])


@dataclass
class Xy:
    controlT: ClassVar[controlType] = ControlType.XY
    properties: Properties = field(default_factory=lambda: XyProperties().build())
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])


@dataclass
class Radial:
    controlT: ClassVar[controlType] = ControlType.RADIAL
    properties: Properties = field(
        default_factory=lambda: RadialProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])


@dataclass
class Encoder:
    controlT: ClassVar[controlType] = ControlType.ENCODER
    properties: Properties = field(
        default_factory=lambda: EncoderProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])


@dataclass
class Radar:
    controlT: ClassVar[controlType] = ControlType.RADAR
    properties: Properties = field(
        default_factory=lambda: RadarProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])


@dataclass
class Radio:
    controlT: ClassVar[controlType] = ControlType.RADIO
    properties: Properties = field(
        default_factory=lambda: RadioProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])


@dataclass
class Group:
    controlT: ClassVar[controlType] = ControlType.GROUP
    properties: Properties = field(
        default_factory=lambda: GroupProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list[controlType] = field(default_factory=lambda: [])


@dataclass
class Grid:
    controlT: ClassVar[controlType] = ControlType.GRID
    properties: Properties = field(
        default_factory=lambda: GridProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list[controlType] = field(default_factory=lambda: [])


@dataclass
class Pager:
    controlT: ClassVar[controlType] = ControlType.PAGER
    properties: Properties = field(
        default_factory=lambda: PagerProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list[controlType] = field(
        default_factory=lambda: [Page(), Page(), Page()]
    )


class Control(Protocol):
    controlT: ClassVar[controlType]
    properties: Properties
    values: Values
    messages: Messages


class ControlProperties(Protocol):
    name: str
    tag: str
    script: str
    frame: tuple
    color: tuple

    def build(self) -> Properties:
        ...


class ControlFactory:
    @classmethod
    def build(cls, control: Control) -> ET.Element:
        node = ET.Element(
            ControlElements.NODE.value,
            attrib={"ID": str(uuid.uuid4()), "type": control.controlT.value},
        )
        properties = ET.SubElement(node, ControlElements.PROPERTIES.value)
        values = ET.SubElement(node, ControlElements.VALUES.value)
        messages = ET.SubElement(node, ControlElements.MESSAGES.value)
        children = ET.SubElement(node, ControlElements.CHILDREN.value)

        XmlFactory.buildProperties(control.properties, properties)
        XmlFactory.buildValues(control.values, values)
        XmlFactory.buildMessages(control.messages, messages)
        return node



class XmlFactory:
    @classmethod
    def buildProperties(cls, props: Properties, e: ET.Element) -> bool:
        for prop in props:
            property = ET.SubElement(
                e, ControlElements.PROPERTY.value, attrib={"type": prop.type}
            )
            ET.SubElement(property, "key").text = prop.key
            value = ET.SubElement(property, "value")
            value.text = prop.value
            for k in prop.params:
                ET.SubElement(value, k).text = prop.params[k]
        return True

    @classmethod
    def modifyProperty(cls, value, params, p: ET.Element) -> bool:
        v = p.find("value")
        v.text = value
        for k in params:
            value.find(k).text = params[k]
        return True

    @classmethod
    def buildValues(cls, vals: Values, e: ET.Element) -> bool:
        for val in vals:
            value = ET.SubElement(e, ControlElements.VALUE.value)
            for k in val.__slots__:
                ET.SubElement(value, k).text = getattr(val, k)
        return True

    @classmethod
    def modifyValue(cls, val: Value, e: ET.Element) -> bool:
        for k in val.__slots__:
            e.find(k).text = getattr(val, k)
        return True

    @classmethod
    def buildMessages(cls, msgs: Messages, e: ET.Element) -> bool:
        for message in msgs:
            msg = ET.SubElement(e, message.__class__.__name__.lower())
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
        return True

    @classmethod
    def buildNode(cls, controlT: controlType, e) -> ET.Element:
        return ET.SubElement(
            e,
            ControlElements.NODE.value,
            attrib={"ID": str(uuid.uuid4()), "type": controlT.value},
        )
