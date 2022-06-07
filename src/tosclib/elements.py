""" Enumerations for constructing XML Elements"""

from enum import Enum, unique
from typing import List, Literal, Protocol
import xml.etree.ElementTree as ET
from lxml import etree as ET


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


"""

Objects

"""


# class Property2(Protocol):
#     __slots__ = ("type", "key", "value", "params")
#     type: Literal[
#         PropertyType.BOOLEAN,
#         PropertyType.COLOR,
#         PropertyType.FLOAT,
#         PropertyType.FRAME,
#         PropertyType.INTEGER,
#         PropertyType.STRING,
#     ] = type
#     key: str = key
#     value: str | int | float | bool = value
#     params: dict = params


class Property:
    """Struct like object to carry the property values"""

    __slots__ = ("type", "key", "value", "params")

    def __init__(
        self, type: str, key: str, value: str = "", params: dict = {}
    ) -> "Property":
        self.type: str = type
        self.key: str = key
        self.value: str = value
        self.params: dict = params


class PropertyFactory:
    @classmethod
    def name(cls, value: str) -> Property:
        return Property(PropertyType.STRING.value, "name", value)

    @classmethod
    def tag(cls, value: str) -> Property:
        return Property(PropertyType.STRING.value, "tag", value)

    @classmethod
    def script(cls, value: str) -> Property:
        return Property(PropertyType.STRING.value, "script", value)

    # def frame

    # color

    # locked

    # visible

    # interactive

    # background

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

    __slots__ = ("type", "channel", "data1", "data2")

    def __init__(
        self,
        type: str = "CONTROLCHANGE",
        channel: str = "0",
        data1: str = "0",
        data2: str = "0",
    ):
        self.type = type
        self.channel = channel
        self.data1 = data1
        self.data2 = data2


class MidiValue:

    __slots__ = ("type", "key", "scaleMin", "scaleMax")

    def __init__(
        self,
        type: str = "CONSTANT",
        key: str = "",
        scaleMin: str = "0",
        scaleMax: str = "15",
    ):
        self.type = type
        self.key = key
        self.scaleMin = scaleMin
        self.scaleMax = scaleMax


class Message:
    pass


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
        triggers: List[Trigger] = [Trigger()],
        path: List[Partial] = [Partial(), Partial(type="PROPERTY", value="name")],
        arguments: List[Partial] = [
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
        triggers: List[Trigger] = [Trigger()],
        message: MidiMessage = MidiMessage(),
        values: List[MidiValue] = [
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
        triggers: List[Trigger] = [Trigger()],
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
