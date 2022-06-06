""" Enumerations for constructing XML Elements"""

from typing import NamedTuple
from dataclasses import dataclass, field
from typing import List
import xml.etree.ElementTree as ET
from lxml import etree as ET


class ControlElements(NamedTuple):
    """Valid Elements of a Node"""

    PROPERTIES = "properties"  #: <properties>
    VALUES = "values"  #: <values>
    MESSAGES = "messages"  #: <messages>
    CHILDREN = "children"  #: <children>
    PROPERTY = (
        "property"  #: <property type = `PropertyType <#tosclib.tosc.PropertyType>`_>
    )
    VALUE = "value"  #: <value>
    OSC = "osc"  #: <osc>
    MIDI = "midi"  #: <midi>
    LOCAL = "local"  #: <local>
    GAMEPAD = "gamepad"  #: <gamepad>
    NODE = "node"  #: <node type = `ControlType <#tosclib.tosc.ControlType>`_>


class ControlType(NamedTuple):
    """Enum of valid <node type=>"""

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


class PropertyType(NamedTuple):
    """Enum of valid <property type=>"""

    STRING = "s"  #: <property type="s">
    BOOLEAN = "b"  #: <property type="b">
    INTEGER = "i"  #: <property type="i">
    FLOAT = "f"  #: <property type="f">
    FRAME = "r"  #: <property type="r">
    COLOR = "c"  #: <property type="c">


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
            raise ValueError(f"{self} is missing both value and params.")

    def applyTo(self, e: ET.Element) -> bool:
        """Create SubElement Property in passed Element"""
        property = ET.SubElement(e, "property", attrib={"type": self.type})
        ET.SubElement(property, "key").text = self.key
        value = ET.SubElement(property, "value")
        if self.value:
            value.text = self.value
            return True
        for paramKey in self.params:
            ET.SubElement(value, paramKey).text = self.params[paramKey]
        return True

    def build(self) -> ET.Element:
        """Returns an xml Element <property>"""
        property = ET.Element("property", attrib={"type": self.type})
        ET.SubElement(property, "key").text = self.key
        value = ET.SubElement(property, "value")
        if self.value:
            value.text = self.value
            return property
        for paramKey in self.params:
            ET.SubElement(value, paramKey).text = self.params[paramKey]
        return property

    @classmethod
    def createProperty(cls, type, key, value=None, params=None) -> ET.Element:
        property = ET.Element("property", attrib={"type": type})
        ET.SubElement(property, "key").text = key
        value = ET.SubElement(property, "value")
        if value:
            value.text = value
            return property
        for paramKey in params:
            ET.SubElement(value, paramKey).text = params[paramKey]
        return property

    class Elements(NamedTuple):
        KEY = "key"
        VALUE = "value"
        R, G, B, A = "r", "g", "b", "a"
        X, Y, W, H = "x", "y", "w", "h"


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

    class Elements(NamedTuple):
        KEY = "key"
        LOCKED = "locked"
        LOCKED_DEFAULT_CURRENT = "lockedDefaultCurrent"
        DEFAULT = "default"
        DEFAULT_PULL = "defaultPull"


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


@dataclass
class MidiMessage:
    type: str = "CONTROLCHANGE"
    channel: str = "0"
    data1: str = "0"
    data2: str = "0"


@dataclass
class MidiValue:
    type: str = "CONSTANT"
    key: str = ""
    scaleMin: str = "0"
    scaleMax: str = "15"


@dataclass
class MIDI:
    """Default elements for <midi>
    Args:
        enabled: bool
        send : bool
        receive : bool
        feedback : bool
        connections : bool
        triggers : List of Trigger
        messages : MidiMessage
        values : List of MidiValue
    """

    enabled: str = "1"
    send: str = "1"
    receive: str = "1"
    feedback: str = "0"
    connections: str = "00001"
    triggers: List[Trigger] = field(default_factory=lambda: [Trigger()])
    message: MidiMessage = MidiMessage()
    values: List[MidiValue] = field(
        default_factory=lambda: [
            MidiValue(),
            MidiValue("INDEX", "", "0", "1"),
            MidiValue("VALUE", "x", "0", "127"),
        ]
    )


@dataclass
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

    enabled: str = "1"
    triggers: List[Trigger] = field(default_factory=lambda: [Trigger()])
    type: str = "VALUE"
    conversion: str = "FLOAT"
    value: str = "x"
    scaleMin: str = "0"
    scaleMax: str = "1"
    dstType: str = ""
    dstVar: str = ""
    dstID: str = ""
