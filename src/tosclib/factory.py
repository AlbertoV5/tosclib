"""
Tuple factories for the types hinted in elements.py
"""

from typing import TypeGuard
from .elements import *
from logging import debug


def val_value(
    key: Literal["x", "y", "touch", "text"] = "touch",
    locked: bool = False,
    lockedCD: bool = False,
    default: str | bool | float = True,
    pull: int = 0,
) -> Value:
    """Value factory"""
    return Value((key, locked, lockedCD, default, pull))


def val_values(*args: Value) -> Values:
    """Values factory"""
    return Values(tuple(arg for arg in args))


def msg_config(
    enabled: bool = True,
    send: bool = True,
    receive: bool = True,
    feedback: bool = False,
    connection: str = "11111",
) -> MsgConfig:
    """MessageConfig factory"""
    return MsgConfig((enabled, send, receive, feedback, connection))


def msg_trigger(
    key: Literal["x", "y", "touch", "text"] = "touch",
    condition: Literal["ANY", "RISE", "FALL"] = "ANY",
):
    """Trigger factory"""
    return Trigger((key, condition))


def msg_triggers(*args: Trigger):
    """Triggers factory"""
    return Triggers(tuple(arg for arg in args))


def msg_partial(
    typ: Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"] = "CONSTANT",
    conv: Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"] = "STRING",
    value: str = "/",
    scaleMin: int = 0,
    scaleMax: int = 1,
) -> Partial:
    """Partial factory"""
    return Partial((typ, conv, value, scaleMin, scaleMax))


def msg_address(*args: Partial) -> Address:
    """Message Address factory"""
    return Address(tuple(arg for arg in args))


def msg_args(*args: Partial) -> Arguments:
    """Message Arguments factory"""
    return Arguments(tuple(arg for arg in args))


def msg_midimsg(
    typ: Literal[
        "NOTE_OFF",
        "NOTE_ON",
        "POLYPRESSURE",
        "CONTROLCHANGE",
        "PROGRAMCHANGE",
        "CHANNELPRESSURE",
        "PITCHBEND",
        "SYSTEMEXCLUSIVE",
    ] = "CONTROLCHANGE",
    channel: int = 1,
    data1: str = "",
    data2: str = "",
) -> MidiMsg:
    """Midi Message factory"""
    return MidiMsg((typ, channel, data1, data2))


def msg_midival(
    key: str = "x",
    typ: Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"] = "VALUE",
    scaleMin: int = 0,
    scaleMax: int = 127,
) -> MidiValue:
    """Midi Value factory"""
    return MidiValue((key, typ, scaleMin, scaleMax))


def msg_midivals(*args: MidiValue) -> MidiValues:
    """Midi Values factory"""
    return MidiValues(tuple(arg for arg in args))


def msg_localsrc(
    key: str = "x",
    typ: Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"] = "VALUE",
    conversion: Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"] = "FLOAT",
    minRange: int = 0,
    maxRange: int = 1,
) -> LocalSrc:
    """Local Source factory"""
    return LocalSrc((key, typ, conversion, minRange, maxRange))


def msg_localdst(
    key: str = "x",
    id: str = " ",
    typ: Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"] = "VALUE",
) -> LocalDst:
    """Local Destination factory"""
    return LocalDst((key, id, typ))


def osc(
    config: MsgConfig = None,
    triggers: Triggers = None,
    address: Address = None,
    arguments: Arguments = None,
) -> MessageOSC:
    """OSC message factory"""
    config = msg_config() if config is None else config
    triggers = msg_triggers() if triggers is None else triggers
    address = msg_address() if address is None else address
    arguments = msg_args() if arguments is None else arguments
    return MessageOSC((config, triggers, address, arguments))


def midi(
    config: MsgConfig = None,
    triggers: Triggers = None,
    message: MidiMsg = None,
    values: MidiValues = None,
) -> MessageMIDI:
    """MIDI Message Factory"""
    config = msg_config() if config is None else config
    triggers = msg_triggers() if triggers is None else triggers
    message = msg_midimsg() if message is None else message
    values = msg_midivals() if values is None else values
    return MessageMIDI((config, triggers, message, values))


def local(
    enabled: bool = None,
    triggers: Triggers = None,
    source: LocalSrc = None,
    destination: LocalDst = None,
) -> MessageLOCAL:
    """LOCAL Message factory"""
    enabled = True if enabled is None else enabled
    triggers = msg_triggers() if triggers is None else triggers
    source = msg_localsrc() if source is None else source
    destination = msg_localdst() if destination is None else destination
    return MessageLOCAL((enabled, triggers, source, destination))


"""

UTIL

"""


def is_property(property: Property) -> TypeGuard[Property]:
    """Verify if property is Property"""
    if isinstance(property, int):
        debug("int")
        return True
    elif isinstance(property, float):
        debug("float")
        return True
    elif isinstance(property, bool):
        debug("bool")
        return True
    elif isinstance(property, str):
        debug("str")
        return True
    elif isinstance(property, tuple) and isinstance(property[0], int):
        debug("frame")
        return True
    elif isinstance(property, tuple) and isinstance(property[0], float):
        debug("color")
        return True
    else:
        return False
