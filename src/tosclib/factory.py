"""
Tuple factories for the types in .elements
"""

from typing import Literal
from .elements import *
from logging import debug


__all__ = [
    "prop",
    "value",
    "msgconfig",
    "msgtrigger",
    "msgpartial",
    "msgmidimsg",
    "msgmidival",
    "msglocalsrc",
    "msglocaldst",
    "osc",
    "midi",
    "local",
]


def prop(
    key: str, value: str | int | float | bool | tuple[int, ...] | tuple[float, ...]
) -> Property:
    """Property factory"""
    return (key, value)


def value(
    key: Literal["x", "y", "touch", "text"] = "touch",
    locked: bool = False,
    lockedCD: bool = False,
    default: str | bool | float = True,
    pull: int = 0,
) -> Value:
    """Value factory"""
    return (key, locked, lockedCD, default, pull)


def msgconfig(
    enabled: bool = True,
    send: bool = True,
    receive: bool = True,
    feedback: bool = False,
    connection: str = "11111",
) -> MsgConfig:
    """MessageConfig factory"""
    return MsgConfig((enabled, send, receive, feedback, connection))


def msgtrigger(
    key: Literal["x", "y", "touch", "text"] = "touch",
    condition: Literal["ANY", "RISE", "FALL"] = "ANY",
):
    """Trigger factory"""
    return Trigger((key, condition))


def msgpartial(
    typ: Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"] = "CONSTANT",
    conv: Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"] = "STRING",
    value: str = "/",
    scaleMin: int = 0,
    scaleMax: int = 1,
) -> Partial:
    """Partial factory"""
    return Partial((typ, conv, value, scaleMin, scaleMax))


def msgmidimsg(
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


def msgmidival(
    key: str = "x",
    typ: Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"] = "VALUE",
    scaleMin: int = 0,
    scaleMax: int = 127,
) -> MidiValue:
    """Midi Value factory"""
    return MidiValue((typ, key, scaleMin, scaleMax))


def msglocalsrc(
    key: str = "x",
    typ: Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"] = "VALUE",
    conversion: Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"] = "FLOAT",
    minRange: int = 0,
    maxRange: int = 1,
) -> LocalSrc:
    """Local Source factory"""
    return LocalSrc((typ, conversion, key, minRange, maxRange))


def msglocaldst(
    key: str = "x",
    id: str = " ",
    typ: Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"] = "VALUE",
) -> LocalDst:
    """Local Destination factory"""
    return LocalDst((typ, key, id))


def osc(
    config: MsgConfig = None,
    triggers: Triggers = None,
    address: Address = None,
    arguments: Arguments = None,
) -> MessageOSC:
    """OSC message factory"""
    if config is None:
        config = msgconfig()
    if triggers is None:
        triggers = (msgtrigger(),)
    if address is None:
        address = (
            msgpartial(),
            msgpartial("PROPERTY", "STRING", "name"),
            msgpartial(),
        )
    if arguments is None:
        arguments = (msgpartial(),)
    return MessageOSC(("osc", config, triggers, address, arguments))


def midi(
    config: MsgConfig = None,
    triggers: Triggers = None,
    message: MidiMsg = None,
    values: MidiValues = None,
) -> MessageMIDI:
    """MIDI Message Factory"""
    if config is None:
        config = msgconfig()
    if triggers is None:
        triggers = (msgtrigger(),)
    if message is None:
        message = msgmidimsg()
    if values is None:
        values = (msgmidival(),)
    return MessageMIDI(("midi", config, triggers, message, values))


def local(
    enabled: bool = True,
    triggers: Triggers = None,
    source: LocalSrc = None,
    destination: LocalDst = None,
) -> MessageLOCAL:
    """LOCAL Message factory"""
    if triggers is None:
        triggers = (msgtrigger(),)
    if source is None:
        source = msglocalsrc()
    if destination is None:
        destination = msglocaldst()
    return MessageLOCAL(("local", enabled, triggers, source, destination))
