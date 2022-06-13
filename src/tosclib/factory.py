"""
Tuple factories for the types hinted in elements.py
"""

from typing import TypeGuard, Literal
from .elements import *
from logging import debug


__all__ = [
    "prop_prop",
    "val_value",
    "msg_config",
    "msg_trigger",
    "msg_partial",
    "msg_midimsg",
    "msg_midival",
    "msg_localsrc",
    "msg_localdst",
    "osc",
    "midi",
    "local",
]


def prop_prop(
    key: str, value: str | int | float | bool | tuple[int, ...] | tuple[float, ...]
) -> Property:
    """Property factory"""
    return (key, value)


def val_value(
    key: Literal["x", "y", "touch", "text"] = "touch",
    locked: bool = False,
    lockedCD: bool = False,
    default: str | bool | float = True,
    pull: int = 0,
) -> Value:
    """Value factory"""
    return (key, locked, lockedCD, default, pull)


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


def msg_partial(
    typ: Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"] = "CONSTANT",
    conv: Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"] = "STRING",
    value: str = "/",
    scaleMin: int = 0,
    scaleMax: int = 1,
) -> Partial:
    """Partial factory"""
    return Partial((typ, conv, value, scaleMin, scaleMax))


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
    if config is None:
        config = msg_config()
    if triggers is None:
        triggers = (msg_trigger(),)
    if address is None:
        address = (
            msg_partial(),
            msg_partial("PROPERTY", "STRING", "name"),
            msg_partial(),
        )
    if arguments is None:
        arguments = (msg_partial(),)
    return MessageOSC((config, triggers, address, arguments))


def midi(
    config: MsgConfig = None,
    triggers: Triggers = None,
    message: MidiMsg = None,
    values: MidiValues = None,
) -> MessageMIDI:
    """MIDI Message Factory"""
    if config is None:
        config = msg_config()
    if triggers is None:
        triggers = (msg_trigger(),)
    if message is None:
        message = msg_midimsg()
    if values is None:
        values = (msg_midival(),)
    return MessageMIDI((config, triggers, message, values))


def local(
    enabled: bool = True,
    triggers: Triggers = None,
    source: LocalSrc = None,
    destination: LocalDst = None,
) -> MessageLOCAL:
    """LOCAL Message factory"""
    if triggers is None:
        triggers = (msg_trigger(),)
    if source is None:
        source = msg_localsrc()
    if destination is None:
        destination = msg_localdst()
    return MessageLOCAL((enabled, triggers, source, destination))