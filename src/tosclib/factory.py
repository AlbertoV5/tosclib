"""
Factories for elements defined in core.
"""

from typing import Literal, overload
from uuid import UUID, uuid4
from .core.elements import *

__all__ = [
    "property",
    "value",
    "msgconfig",
    "trigger",
    "triggers",
    "partial",
    "address",
    "arguments",
    "midimsg",
    "midival",
    "localsrc",
    "localdst",
    "osc",
    "midi",
    "local",
]


def property(key: str, value: PropertyValue) -> Property:
    """Property factory: Creates type-safe tuple.

    Args:
        key (str): Key of the property. Like "tag", "outline", "frame", etc.
        value (PropertyValue):
            Any str, int, float, bool, tuple[float,...] or tuple[int,...]
            that fits the key.

    Important:

        - The Python type will dictate the "type" attribute for the XML Element.

        - A str will become type = "s", bool will be "b", etc.

        - The value arg becomes the Element's text or sub elements depending on the value's type.

        - tuple[int,...] converts to: {"x":v[0], "y":v[1], "w":v[2], "h":v[3]}

        - tuple[float,..] converts to the r,g,b,a equivalent.

    Hint:

        - This functions sirves mostly as a type-checker as you can create the tuple manually.

        - You can use the tosclib.properties module to find common properties and their types.


    Examples:

        .. code-block:: python

            name = property("name", "GeoffPeterson")

        .. code-block:: XML

            <property type="s">
                <key>name</key>
                <value>GeoffPeterson</value>
            </property>

        .. code-block:: python

            frame = property("frame", (0,0,100,100))

        .. code-block:: XML

            <property type="r">
                <key>
                    frame
                </key>
                <value>
                    <x>0</x>
                    <y>0</y>
                    <w>100</w>
                    <h>100</h>
                </value>
            </property>

    Returns:
        Property: :class:`~tosclib.core.Property`
    """
    return Property((key, value))


@overload
def value(
    key: Literal["touch"], locked: bool, locked_dc: bool, default: bool, pull: int
) -> Value:
    ...


@overload
def value(
    key: Literal["x", "y"], locked: bool, locked_dc: bool, default: float, pull: int
) -> Value:
    ...


@overload
def value(
    key: Literal["page"], locked: bool, locked_dc: bool, default: int, pull: int
) -> Value:
    ...


@overload
def value(
    key: Literal["text"], locked: bool, locked_dc: bool, default: str, pull: int
) -> Value:
    ...


def value(
    key: ValueKey = "touch",
    locked: bool = False,
    locked_dc: bool = False,
    default: ValueDefault = True,
    pull: int = 0,
) -> Value:
    """Value Factory: Creates type-safe tuple.

    Args:
        key (ValueKey, optional): The key of the value. Default is "touch".
        locked (bool, optional): Default is False.
        locked_dc (bool, optional): Lock default current. Default is False.
        default (ValueDefault, optional): This is the "value's value".
        pull (int, optional): Int from 0 to 100. Defaults to 0.

    Important:

        - Just as Property, this will convert the Python types into XML strings.

        - The default argument type must match the key:
            - For "touch" use a boolean.
            - For "page" use an int.
            - For "x", "y" use a float.
            - For "text" use a str.

    Examples:

        .. code-block:: python

            x = value(key = "x", default = 0.42)

        .. code-block:: XML

            <value>
                <key>x</key>
                <locked>0</locked>
                <lockedDefaultCurrent>0</lockedDefaultCurrent>
                <default>0.42</default>
                <defaultPull>0</defaultPull>
            </value>

        .. code-block:: python

            text = value(key = "text", default = "Synth")

        .. code-block:: XML

            <value>
                <key>text</key>
                <locked>0</locked>
                <lockedDefaultCurrent>0</lockedDefaultCurrent>
                <default>Synth</default>
                <defaultPull>0</defaultPull>
            </value>


    Returns:
        Value: :class:`~tosclib.core.Value`
    """
    return Value((key, locked, locked_dc, default, pull))


def msgconfig(
    enabled: bool = True,
    send: bool = True,
    receive: bool = True,
    feedback: bool = False,
    connection: str = "11111",
) -> MsgConfig:
    """Message config factory.

    Args:
        enabled (bool, optional): _description_. Defaults to True.
        send (bool, optional): _description_. Defaults to True.
        receive (bool, optional): _description_. Defaults to True.
        feedback (bool, optional): _description_. Defaults to False.
        connection (str, optional): _description_. Defaults to "11111".

    Returns:
        MsgConfig: _description_
    """
    return MsgConfig((enabled, send, receive, feedback, connection))


def trigger(
    key: ValueKey = "touch",
    condition: TriggerType = "ANY",
) -> Trigger:
    """Trigger factory"""
    return Trigger((key, condition))


def triggers(*args: Trigger) -> tuple[Trigger, ...]:
    """tuple[Trigger,...] factory"""
    if len(args) == 0:
        args = (trigger(),)
    return args


def partial(
    typ: PartialType = "CONSTANT",
    conv: ConversionType = "STRING",
    value: str = "/",
    scaleMin: int = 0,
    scaleMax: int = 1,
) -> Partial:
    """Partial factory"""
    return Partial((typ, conv, value, scaleMin, scaleMax))


def address(*args: Partial) -> tuple[Partial, ...]:
    """tuple[Partial, ...] factory"""
    if len(args) == 0:
        args = (partial(), partial("PROPERTY", "STRING", "name"), partial())
    return args


def arguments(*args: Partial) -> tuple[Partial, ...]:
    """tuple[Partial, ...] factory"""
    if len(args) == 0:
        args = (partial(), partial("VALUE", "FLOAT", "x"), partial())
    return args


def midimsg(
    typ: MidiMsgType = "CONTROLCHANGE",
    channel: int = 1,
    data1: str = "",
    data2: str = "",
) -> MidiMsg:
    """Midi Message factory"""
    return MidiMsg((typ, channel, data1, data2))


def midival(
    key: str = "x",
    typ: PartialType = "VALUE",
    scaleMin: int = 0,
    scaleMax: int = 127,
) -> MidiValue:
    """Midi Value factory"""
    return MidiValue((typ, key, scaleMin, scaleMax))


def localsrc(
    type: PartialType = "VALUE",
    conversion: ConversionType = "FLOAT",
    value: str = "x",
    scaleMin: int = 0,
    scaleMax: int = 1,
) -> LocalSrc:
    """Local Source factory"""
    return LocalSrc((type, conversion, value, scaleMin, scaleMax))


def localdst(
    dstType: PartialType = "VALUE",
    dstVar: str = "x",
    dstID: str = " ",
) -> LocalDst:
    """Local Destination factory"""
    return LocalDst((dstType, dstVar, dstID))


def osc(
    config: MsgConfig = None,
    triggers: tuple[Trigger, ...] = None,
    addrs: tuple[Partial, ...] = None,
    args: tuple[Partial, ...] = None,
) -> MessageOSC:
    """OSC Message Factory: Creates type-safe new-type tuple.

    Args:
        config (MsgConfig, optional): Type-safe tuple. Defaults to None.
        triggers (tuple[Trigger, ...], optional): Tuple of type-safe tuples. Defaults to None.
        addrs (tuple[Partial, ...], optional): Tuple of type-safe tuples. Defaults to None.
        args (tuple[Partial, ...], optional): Tuple of type-safe tuples. Defaults to None.

    Returns:
        MessageOSC: _description_
    """
    if config is None:
        config = msgconfig()
    if triggers is None:
        triggers = (trigger(),)
    if addrs is None:
        addrs = address()
    if args is None:
        args = arguments()
    return MessageOSC(("osc", config, triggers, addrs, args))


def midi(
    config: MsgConfig = None,
    triggers: tuple[Trigger, ...] = None,
    message: MidiMsg = None,
    values: tuple[MidiValue, ...] = None,
) -> MessageMIDI:
    """MIDI Message Factory"""
    if config is None:
        config = msgconfig()
    if triggers is None:
        triggers = (trigger(),)
    if message is None:
        message = midimsg()
    if values is None:
        values = (midival(),)
    return MessageMIDI(("midi", config, triggers, message, values))


def local(
    enabled: bool = True,
    triggers: tuple[Trigger, ...] = None,
    source: LocalSrc = None,
    destination: LocalDst = None,
) -> MessageLOCAL:
    """LOCAL Message factory"""
    if triggers is None:
        triggers = (trigger(),)
    if source is None:
        source = localsrc()
    if destination is None:
        destination = localdst()
    return MessageLOCAL(("local", enabled, triggers, source, destination))
