"""
Hexler's Enumerations
"""

from copy import deepcopy
from dataclasses import dataclass, field
from types import UnionType
from typing import ClassVar, Final, Protocol, TypeAlias, TypeGuard
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

import xml.etree.ElementTree as ET
# from lxml import etree as ET

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

    def build(self, *args) -> Properties:
        """Build all Property objects of this class.
        Returns:
            list[Property] from this class' attributes.
        """
        if len(args) == 0:
            args = tuple(key for key in vars(self))

        return [PropertyFactory.build(arg, getattr(self, arg)) for arg in args]


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


@dataclass
class Page:
    """Not a main control"""

    controlT: ClassVar[controlType] = ControlType.GROUP
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(default_factory=lambda:PageProperties().build())
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Box:
    controlT: ClassVar[controlType] = ControlType.BOX
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(default_factory=lambda: BoxProperties().build())
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Button:
    controlT: ClassVar[controlType] = ControlType.BUTTON
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: ButtonProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Label:
    controlT: ClassVar[controlType] = ControlType.LABEL
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: LabelProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Text:
    controlT: ClassVar[controlType] = ControlType.TEXT
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: TextProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Fader:
    controlT: ClassVar[controlType] = ControlType.FADER
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: FaderProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Xy:
    controlT: ClassVar[controlType] = ControlType.XY
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(default_factory=lambda: XyProperties().build())
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Radial:
    controlT: ClassVar[controlType] = ControlType.RADIAL
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: RadialProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Encoder:
    controlT: ClassVar[controlType] = ControlType.ENCODER
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: EncoderProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Radar:
    controlT: ClassVar[controlType] = ControlType.RADAR
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: RadarProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Radio:
    controlT: ClassVar[controlType] = ControlType.RADIO
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: RadioProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Group:
    controlT: ClassVar[controlType] = ControlType.GROUP
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: GroupProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Grid:
    controlT: ClassVar[controlType] = ControlType.GRID
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: GridProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = None


@dataclass
class Pager:
    controlT: ClassVar[controlType] = ControlType.PAGER
    id: str = field(default_factory=lambda:str(uuid.uuid4()))
    properties: Properties = field(
        default_factory=lambda: PagerProperties().build()
    )
    values: Values = field(default_factory=lambda: [])
    messages: Messages = field(default_factory=lambda: [])
    children: list["Control"] | None | list = field(
        default_factory=lambda: [Group(), Group(), Group()]
    )


class Control(Protocol):
    """Protocol type of Control

    Attributes:
        controlT: Control Type
        properties: List of Property
        values: List of Value
        messages: List of Message
    """
    controlT: ClassVar[controlType]
    id: str
    properties: Properties
    values: Values
    messages: Messages
    children: list["Control"] | None | list

# Control:TypeAlias = (
#     Label | Text | Box | Button | Group | Encoder | Page |
#     Grid | Fader | Pager | Radial | Radio | Radar | Xy)


class ControlProperties(Protocol):
    """Data structure to store control properties and defaults
    for reference."""
    name: str
    tag: str
    script: str
    frame: tuple
    color: tuple

    def build(self) -> Properties:
        ...



class ControlFactory:
    @classmethod
    def build(cls, 
    controlT: controlType, 
    id: str = None,
    properties: Properties = None,
    values: Values = None,
    messages: Messages = None) -> Control:
        id = str(uuid.uuid4()) if id is None else id
        properties = [] if properties is None else properties
        values = [] if values is None else values
        messages = [] if messages is None else messages
        match controlT:
            case ControlType.BOX:
                return Box(id, properties, values, messages)
            case ControlType.BUTTON:
                return Button(id, properties, values, messages)
            case ControlType.ENCODER:
                return Encoder(id, properties, values, messages)
            case ControlType.FADER:
                return Fader(id, properties, values, messages)
            case ControlType.GRID:
                return Grid(id, properties, values, messages)
            case ControlType.GROUP:
                return Group(id, properties, values, messages)
            case ControlType.LABEL:
                return Label(id, properties, values, messages)
            case ControlType.PAGER:
                return Pager(id, properties, values, messages)
            case ControlType.RADAR:
                return Radar(id, properties, values, messages)
            case ControlType.RADIAL:
                return Radial(id, properties, values, messages)
            case ControlType.RADIO:
                return Radio(id, properties, values, messages)
            case ControlType.TEXT:
                return Text(id, properties, values, messages)
            case ControlType.XY:
                return Xy(id, properties, values, messages)
            case _:
                raise ValueError(f"{controlT} not found.")


class ControlConverter:
    """Convert from Control to XML"""
    @classmethod
    def build(cls, control: Control) -> ET.Element:
        """Generate the XML Element and its SubElements

        Args:
            control (Control): Control

        Returns:
            ET.Element: XML
        """
        node = ET.Element(
            ControlElements.NODE.value,
            attrib={"ID": control.id, "type": control.controlT.value},
        )
        properties = ET.SubElement(node, ControlElements.PROPERTIES.value)
        values = ET.SubElement(node, ControlElements.VALUES.value)
        messages = ET.SubElement(node, ControlElements.MESSAGES.value)
        
        XmlFactory.buildProperties(properties, control.properties)
        XmlFactory.buildValues(values, control.values)
        XmlFactory.buildMessages(messages, control.messages)

        if control.children is not None:
            children = ET.SubElement(node, ControlElements.CHILDREN.value)
            for child in control.children:
                children.append(cls.build(child))
        
        return node


class XmlFactory:
    """Generate specific XML structures"""
    @classmethod
    def buildProperties(cls, e: ET.Element, props: Properties) -> bool:
        """Create many <property> XML

        Args:
            props (Properties): List of Properties
            e (ET.Element): Element to append the properties to

        Returns:
            bool: bool
        """
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
    def modifyProperty(cls, e: ET.Element, value:str, params:dict[str,str]) -> bool:
        """Modify an existing property XML

        Args:
            value (str): New value
            params (dict): New params
            p (ET.Element): <property>

        Returns:
            bool: bool
        """
        if (v:= e.find("value")) is not None:
            v.text = value
            for k in params:
                if (p := v.find(k)) is not None:
                    p.text = params[k]
            return True
        return False

    @classmethod
    def buildValues(cls, e: ET.Element, vals: Values) -> bool:
        for val in vals:
            value = ET.SubElement(e, ControlElements.VALUE.value)
            for k in val.__slots__:
                ET.SubElement(value, k).text = getattr(val, k)
        return True

    @classmethod
    def modifyValue(cls, e: ET.Element, val: Value) -> bool:
        for k in val.__slots__:
            if (v:=e.find(k)) is not None:
                v.text = getattr(val, k)
        return True

    @classmethod
    def buildMessages(cls, e: ET.Element, msgs: Messages) -> bool:
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
    def buildNode(cls, e: ET.Element, controlT: controlType, ) -> ET.Element:
        return ET.SubElement(
            e,
            ControlElements.NODE.value,
            attrib={"ID": str(uuid.uuid4()), "type": controlT.value},
        )
