"""
Constants implements all the types in Elements as tuples.
"""
from typing import Literal, NamedTuple
from .elements import (
    PartialType,
    ConversionType,
    TriggerType,
    MidiMsgType,
)

__all__ = [
    "PROPERTY_TYPES",
    "VALUE_KEYS",
    # MESSAGE
    "MESSAGE_TYPES",
    "PARTIAL_TYPES",
    "CONVERSION_TYPES",
    "TRIGGER_TYPES",
    "MIDI_MESSAGE_TYPES",
    "CONTROL_TYPES",
    # UTIL
    "NOT_PROPERTIES",
    "PROPERTIES",
    "VALUES",
    "MESSAGES",
    "CHILDREN",
]

PROPERTIES: Literal["properties"] = "properties"
VALUES: Literal["values"] = "values"
MESSAGES: Literal["messages"] = "messages"
CHILDREN: Literal["children"] = "children"


class PropertyTypes(NamedTuple):
    BOOLEAN: Literal["b"] = "b"
    COLOR: Literal["c"] = "c"
    FLOAT: Literal["f"] = "f"
    INTEGER: Literal["i"] = "i"
    FRAME: Literal["r"] = "r"
    STRING: Literal["s"] = "s"


PROPERTY_TYPES: PropertyTypes = PropertyTypes()
"""(b)oolean, (c)olor, (f)loat, (i)nteger, f(r)ame, (s)tring"""


class ValueKeys(NamedTuple):
    X: Literal["x"] = "x"
    Y: Literal["y"] = "y"
    TOUCH: Literal["touch"] = "touch"
    TEXT: Literal["text"] = "text"
    PAGE: Literal["page"] = "page"


VALUE_KEYS: ValueKeys = ValueKeys()


class MessageTypes(NamedTuple):
    OSC: Literal["osc"] = "osc"
    MIDI: Literal["midi"] = "midi"
    LOCAL: Literal["local"] = "local"


MESSAGE_TYPES: MessageTypes = MessageTypes()


NOT_PROPERTIES: tuple[
    Literal["type"],
    Literal["id"],
    Literal["values"],
    Literal["messages"],
    Literal["children"],
    Literal["node"],
] = ("type", "id", "values", "messages", "children", "node")
"""Attributes that are not properties of a Control"""


class ControlTypes(NamedTuple):
    BOX: Literal["BOX"] = "BOX"
    BUTTON: Literal["BUTTON"] = "BUTTON"
    ENCODER: Literal["ENCODER"] = "ENCODER"
    FADER: Literal["FADER"] = "FADER"
    GRID: Literal["GRID"] = "GRID"
    GROUP: Literal["GROUP"] = "GROUP"
    LABEL: Literal["LABEL"] = "LABEL"
    PAGE: Literal["PAGE"] = "PAGE"
    PAGER: Literal["PAGER"] = "PAGER"
    RADAR: Literal["RADAR"] = "RADAR"
    RADIAL: Literal["RADIAL"] = "RADIAL"
    RADIO: Literal["RADIO"] = "RADIO"
    TEXT: Literal["TEXT"] = "TEXT"
    XY: Literal["XY"] = "XY"


CONTROL_TYPES: ControlTypes = ControlTypes()
"""Valid Control Type attributes in type"""

PARTIAL_TYPES: tuple[PartialType, ...] = ("CONSTANT", "INDEX", "VALUE", "PROPERTY")

CONVERSION_TYPES: tuple[ConversionType, ...] = ("BOOLEAN", "INTEGER", "FLOAT", "STRING")

TRIGGER_TYPES: tuple[TriggerType, ...] = ("ANY", "RISE", "FALL")

MIDI_MESSAGE_TYPES: tuple[MidiMsgType, ...] = (
    "NOTE_OFF",
    "NOTE_ON",
    "POLYPRESSURE",
    "CONTROLCHANGE",
    "PROGRAMCHANGE",
    "CHANNELPRESSURE",
    "PITCHBEND",
    "SYSTEMEXCLUSIVE",
)
