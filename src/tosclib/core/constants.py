"""
Constants implements all the types in Elements as tuples.
"""
from typing import Literal
from .elements import (
    ControlType,
    PropertyType,
    ValueType,
    PartialType,
    ConversionType,
    TriggerType,
    MidiMsgType,
)

__all__ = [
    # PROPERTY
    "PROPERTY_TYPES",
    "BOOLEAN",
    "COLOR",
    "FLOAT",
    "INTEGER",
    "FRAME",
    "STRING",
    # VALUE
    "VALUE_TYPES",
    # MESSAGE
    "OSC",
    "MIDI",
    "LOCAL",
    "MESSAGE_TYPES",
    "PARTIAL_TYPES",
    "CONVERSION_TYPES",
    "TRIGGER_TYPES",
    "MIDI_MESSAGE_TYPES",
    # CONTROL
    "BOX",
    "BUTTON",
    "ENCODER",
    "FADER",
    "GRID",
    "GROUP",
    "LABEL",
    "PAGER",
    "RADAR",
    "RADIAL",
    "RADIO",
    "TEXT",
    "XY",
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
OSC: Literal["osc"] = "osc"
MIDI: Literal["midi"] = "midi"
LOCAL: Literal["local"] = "local"

MESSAGE_TYPES: tuple[Literal["osc"], Literal["midi"], Literal["local"]] = (
    OSC,
    MIDI,
    LOCAL,
)

BOOLEAN: Literal["b"] = "b"
COLOR: Literal["c"] = "c"
FLOAT: Literal["f"] = "f"
INTEGER: Literal["i"] = "i"
FRAME: Literal["r"] = "r"
STRING: Literal["s"] = "s"

PROPERTY_TYPES: tuple[PropertyType, ...] = (
    BOOLEAN,
    COLOR,
    FLOAT,
    INTEGER,
    FRAME,
    STRING,
)
"""(b)oolean, (c)olor, (f)loat, (i)nteger, f(r)ame, (s)tring"""

NOT_PROPERTIES: tuple[
    Literal["type"],
    Literal["id"],
    Literal["values"],
    Literal["messages"],
    Literal["children"],
    Literal["node"],
] = ("type", "id", "values", "messages", "children", "node")
"""Attributes that are not properties of a Control"""

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

CONTROL_TYPES: tuple[ControlType, ...] = (
    BOX,
    BUTTON,
    ENCODER,
    FADER,
    GRID,
    GROUP,
    LABEL,
    PAGE,
    PAGER,
    RADAR,
    RADIAL,
    RADIO,
    TEXT,
    XY,
)
"""Valid Control Type attributes in type="""

VALUE_TYPES: tuple[ValueType, ...] = ("x", "y", "touch", "text", "page")

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
