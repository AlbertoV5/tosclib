""" Enumerations for constructing XML Elements"""

from enum import Enum, unique
from typing import List, Literal, Protocol, TypeAlias, TypeVar, TypedDict
from xmlrpc.client import boolean

"""

FIRST SECTION: 

Define Enumerations and Literal types from Hexler's Touch OSC design.

SECOND SECTION:

Define struct like classes that carry the data to create xml Elements.
Plus Factory classes to create them.

"""


@unique
class ControlElements(Enum):
    """Valid xml tags for a Control"""

    PROPERTIES = "properties"  #: <properties>
    VALUES = "values"  #: <values>
    MESSAGES = "messages"  #: <messages>
    CHILDREN = "children"  #: <children>
    PROPERTY = "property"  #: <property type=>
    VALUE = "value"  #: <value>
    OSC = "osc"  #: <osc>
    MIDI = "midi"  #: <midi>
    LOCAL = "local"  #: <local>
    GAMEPAD = "gamepad"  #: <gamepad>
    NODE = "node"  #: <node type =>


@unique
class ControlType(Enum):
    """Valid xml attrib = {"type":ControlType} for <node>"""

    BOX = "BOX"  #: <node type = "BOX">
    BUTTON = "BUTTON"  #: <node type = "BUTTON">
    LABEL = "LABEL"  #: <node type = "LABEL">
    TEXT = "TEXT"  #: <node type = "TEXT">
    FADER = "FADER"  #: <node type = "FADER">
    XY = "XY"  #: <node type = "XY">
    RADIAL = "RADIAL"  #: <node type = "RADIAL">
    ENCODER = "ENCODER"  #: <node type = "ENCODER">
    RADAR = "RADAR"  #: <node type = "RADAR">
    RADIO = "RADIO"  #: <node type = "RADIO">
    GROUP = "GROUP"  #: <node type = "GROUP">
    PAGER = "PAGER"  #: <node type = "PAGER">
    GRID = "GRID"  #: <node type = "GRID">


@unique
class PropertyType(Enum):
    """Valid xml attrib = {"type":PropertyType} for <property>"""

    STRING = "s"  #: <property type="s">
    BOOLEAN = "b"  #: <property type="b">
    INTEGER = "i"  #: <property type="i">
    FLOAT = "f"  #: <property type="f">
    FRAME = "r"  #: <property type="r">
    COLOR = "c"  #: <property type="c">


elementType = Literal[
    ControlElements.CHILDREN,
    ControlElements.GAMEPAD,
    ControlElements.LOCAL,
    ControlElements.MESSAGES,
    ControlElements.MIDI,
    ControlElements.NODE,
    ControlElements.OSC,
    ControlElements.PROPERTIES,
    ControlElements.PROPERTY,
    ControlElements.VALUES,
    ControlElements.VALUE,
]


controlType = Literal[
    ControlType.BOX,
    ControlType.BUTTON,
    ControlType.ENCODER,
    ControlType.FADER,
    ControlType.GRID,
    ControlType.GROUP,
    ControlType.LABEL,
    ControlType.PAGER,
    ControlType.RADAR,
    ControlType.RADIAL,
    ControlType.RADIO,
    ControlType.TEXT,
    ControlType.XY,
]

propertyType = Literal[
    PropertyType.BOOLEAN,
    PropertyType.COLOR,
    PropertyType.FLOAT,
    PropertyType.FRAME,
    PropertyType.INTEGER,
    PropertyType.STRING,
]


class Frame(TypedDict):
    """Typed dictionary of 4 floats"""

    x: int
    y: int
    w: int
    h: int


class Color(TypedDict):
    """Typed dictionary of 4 floats"""

    r: float
    g: float
    b: float
    a: float


"""

SECOND SECTION:

"""


class Property:
    """Struct like object to carry the property values"""

    __slots__ = ("type", "key", "value", "params")

    def __init__(
        self, type: str, key: str, value: str = None, params: Frame | Color = None
    ) -> "Property":
        self.type: propertyType = type
        self.key: str = key
        self.value: str = value
        self.params: Frame | Color = params if params is not None else {}


class PropertyFactory:
    @classmethod
    def build(
        cls, key, value: int | bool | float | str | tuple[int] | tuple[float]
    ) -> Property:
        """_summary_

        Args:
            key (_type_): _description_
            value (int | bool | float | str | tuple[int] | tuple[float]):
            Whatever value with one of those python types.
            Tuples of ints are considered Frames.
            Tuples of floats are considered Colors.

        Raises:
            ValueError: If value type is not compatible with TouchOSC's equivalent.

        Returns:
            Property: _description_
        """
        if type(value) is str:
            return cls.buildString(key, value)
        elif type(value) is bool:
            return cls.buildBoolean(key, value)
        elif type(value) is int:
            return cls.buildInteger(key, value)
        elif type(value) is float:
            return cls.buildFloat(key, value)
        elif type(value) is tuple and type(value[0]) is int:
            return cls.buildFrame(key, value)
        elif type(value) is tuple and type(value[0]) is float:
            return cls.buildColor(key, value)
        else:
            raise ValueError(f"{key}-{value} type is not a valid PropertyType.")

    @classmethod
    def buildBoolean(cls, key: str, value: bool) -> Property:
        return Property(PropertyType.BOOLEAN.value, key, str(int(value)))

    @classmethod
    def buildString(cls, key: str, value: str) -> Property:
        return Property(PropertyType.STRING.value, key, value)

    @classmethod
    def buildInteger(cls, key: str, value: int) -> Property:
        return Property(PropertyType.INTEGER.value, key, str(value))

    @classmethod
    def buildFloat(cls, key: str, value: float) -> Property:
        return Property(PropertyType.FLOAT.value, key, str(value))

    @classmethod
    def buildColor(cls, key: str, value: tuple) -> Property:
        return Property(
            PropertyType.COLOR.value,
            key,
            "",
            {
                "r": str(value[0]),
                "g": str(value[1]),
                "b": str(value[2]),
                "a": str(value[3]),
            },
        )

    @classmethod
    def buildFrame(cls, key: str, value: tuple) -> Property:
        return Property(
            PropertyType.FRAME.value,
            key,
            "",
            {
                "x": str(value[0]),
                "y": str(value[1]),
                "w": str(value[2]),
                "h": str(value[3]),
            },
        )

    @classmethod
    def name(cls, value: str) -> Property:
        return Property(PropertyType.STRING.value, "name", value)

    @classmethod
    def tag(cls, value: str) -> Property:
        return Property(PropertyType.STRING.value, "tag", value)

    @classmethod
    def script(cls, value: str) -> Property:
        return Property(PropertyType.STRING.value, "script", value)

    @classmethod
    def frame(cls, params: Frame) -> Property:
        return Property(PropertyType.FRAME.value, "frame", params=params)

    @classmethod
    def color(cls, params: Color) -> Property:
        return Property(PropertyType.COLOR.value, "color", params=params)

    # locked

    # visible

    # interactive

    @classmethod
    def background(cls, value: bool):
        return Property(PropertyType.BOOLEAN.value, "background", value=str(int(value)))

    @classmethod
    def outline(cls, value: bool):
        return Property(PropertyType.BOOLEAN.value, "outline", value=str(int(value)))


class Value:
    """Default Elements for <value>.

    Args:
        key (str, optional): "x" or "touch". Defaults to "touch".
        locked (str, optional): boolean. Defaults to "0".
        lockedDefaultCurrent (str, optional): boolean. Defaults to "0".
        default (str, optional): float or boolean. Defaults to "false".
        defaultPull (str, optional): 0 to 100. Defaults to "0".
    """

    __slots__ = ("key", "locked", "lockedDefaultCurrent", "default", "defaultPull")

    def __init__(
        self,
        key: str = "touch",
        locked: str = "0",
        lockedDefaultCurrent: str = "0",
        default: str = "false",
        defaultPull: str = "0",
    ):
        self.key: str = key
        self.locked: str = locked
        self.lockedDefaultCurrent: str = lockedDefaultCurrent
        self.default: str = default
        self.defaultPull: str = defaultPull


class Partial:
    """Default Elements for <partial>

    Args:
        type (str, optional): "CONSTANT", "INDEX", "VALUE", "PROPERTY". Defaults to "CONSTANT".
        conversion (str, optional): "BOOLEAN", "INTEGER", "FLOAT", "STRING". Defaults to "STRING".
        value (str, optional): Depends on the context. Defaults to "/".
        scaleMin (str, optional): If "VALUE", set range. Defaults to "0".
        scaleMax (str, optional): If "VALUE", set range. Defaults to "1".
    """

    __slots__ = ("type", "conversion", "value", "scaleMin", "scaleMax")

    def __init__(
        self,
        type: str = "CONSTANT",
        conversion: str = "STRING",
        value: str = "/",
        scaleMin: str = "0",
        scaleMax: str = "1",
    ):
        self.type = type
        self.conversion = conversion
        self.value = value
        self.scaleMin = scaleMin
        self.scaleMax = scaleMax


class Trigger:
    """Default Elements for <trigger>

    Args:
        var (str, optional): "x" or "touch". Defaults to "x".
        con (str, optional): "ANY", "RISE" or "FALL". Defaults to "ANY".
    """

    __slots__ = ("var", "condition")

    def __init__(self, var: str = "x", condition: str = "ANY"):
        self.var = var
        self.condition = condition


class MidiMessage:
    """_summary_

    Args:
        type (str, optional): CONTROLCHANGE, NOTE_ON/OFF, etc. Defaults to "CONTROLCHANGE".
        channel (str, optional): Midi Channel. Defaults to "1".
        data1 (str, optional): Depends on type. Defaults to "0".
        data2 (str, optional): Depends on type. Defaults to "0".
    """

    __slots__ = ("type", "channel", "data1", "data2")

    def __init__(
        self,
        type: str = "CONTROLCHANGE",
        channel: str = "1",
        data1: str = "0",
        data2: str = "0",
    ):
        self.type = type
        self.channel = channel
        self.data1 = data1
        self.data2 = data2


class MidiValue:
    """The Value of the control to send as Midi, generally 0-127 scale.

    Args:
        type (str, optional): CONSTANT, INDEX, VALUE, PROPERTY. Defaults to "VALUE".
        key (str, optional): Value or Property of the control. Defaults to "x".
        scaleMin (str, optional): Scale of the control. Defaults to "0".
        scaleMax (str, optional): Scale of the control. Defaults to "127".
    """

    __slots__ = ("type", "key", "scaleMin", "scaleMax")

    def __init__(
        self,
        type: str = "VALUE",
        key: str = "x",
        scaleMin: str = "0",
        scaleMax: str = "127",
    ):

        self.type = type
        self.key = key
        self.scaleMin = scaleMin
        self.scaleMax = scaleMax


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

    __slots__ = (
        "enabled",
        "send",
        "receive",
        "feedback",
        "connections",
        "triggers",
        "path",
        "arguments",
    )

    def __init__(
        self,
        enabled: str = "1",
        send: str = "1",
        receive: str = "1",
        feedback: str = "0",
        connections: str = "00001",
        triggers: list[Trigger] = [Trigger()],
        path: list[Partial] = [Partial(), Partial(type="PROPERTY", value="name")],
        arguments: list[Partial] = [
            Partial(type="VALUE", conversion="FLOAT", value="x")
        ],
    ):
        self.enabled = enabled
        self.send = send
        self.receive = receive
        self.feedback = feedback
        self.connections = connections
        self.triggers = triggers
        self.path = path
        self.arguments = arguments


class MIDI:
    __slots__ = (
        "enabled",
        "send",
        "receive",
        "feedback",
        "connections",
        "triggers",
        "message",
        "values",
    )

    def __init__(
        self,
        enabled: str = "1",
        send: str = "1",
        receive: str = "1",
        feedback: str = "0",
        connections: str = "00001",
        triggers: list[Trigger] = [Trigger()],
        message: MidiMessage = MidiMessage(),
        values: list[MidiValue] = [
            MidiValue(),
            MidiValue("INDEX", "", "0", "1"),
            MidiValue("VALUE", "x", "0", "127"),
        ],
    ):
        self.enabled = enabled
        self.send = send
        self.receive = receive
        self.feedback = feedback
        self.connections = connections
        self.triggers = triggers
        self.message = message
        self.values = values


class LOCAL:
    """Default elements for <midi>
    Args:
        enabled: bool
        triggers : Trigger x or touch.
        type : BOOL, INT, FLOAT, STRING. The Type of Trigger.x
        conversion : BOOL, INT, FLOAT, STRING.
        value : The value sent to the other local Control.
        scaleMin : 0
        scaleMax : 1
        dstType : BOOL, INT, FLOAT, STRING of the target.
        dstVar : The value you want to change in the target.
        dstID : The node {ID} of the target.
    """

    __slots__ = (
        "enabled",
        "triggers",
        "type",
        "conversion",
        "value",
        "scaleMin",
        "scaleMax",
        "dstType",
        "dstVar",
        "dstID",
    )

    def __init__(
        self,
        enabled: str = "1",
        triggers: list[Trigger] = [Trigger()],
        type: str = "VALUE",
        conversion: str = "FLOAT",
        value: str = "x",
        scaleMin: str = "0",
        scaleMax: str = "1",
        dstType: str = "",
        dstVar: str = "",
        dstID: str = "",
    ):
        self.enabled = enabled
        self.triggers = triggers
        self.type = type
        self.conversion = conversion
        self.value = value
        self.scaleMin = scaleMin
        self.scaleMax = scaleMax
        self.dstType = dstType
        self.dstVar = dstVar
        self.dstID = dstID


# class Message(Protocol):
#     enabled: str
#     triggers: list[Trigger]


Properties: TypeAlias = tuple[Property]
Values: TypeAlias = tuple[Value]
Message: TypeAlias = OSC | MIDI | LOCAL
Messages: TypeAlias = tuple[OSC | MIDI | LOCAL]
