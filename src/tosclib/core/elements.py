"""
Types based on Hexler's Touch OSC Enumerations.

Using typing to define specific tuple shapes and Literals.

The result is no regular classes for these data structures,
this means that most of the logical work relies on the factory
and converter methods in other modules. 

The alternatives were dataclasses, slots or named tuples but
I decided to bet on the newest python >=3.10 typing features 
as a way to future-enable this library and have fun.

A TouchOSC Control is divided into 4 parts:

Control:

    1. Properties: list[Property,...]
    2. Values: list[Value,...]
    3. Messages: list[Message,...]
    4. Children: list[Control,...]

From those parts the following are Type Aliases for tuples:

    Property, Value

Then the Message type is a Type Alias for any of these New Types:

    MessageOSC, MessageMIDI, MessageLOCAL

MessageOSC is made of these New Types:

    MsgConfig: Tuple of various base types, bool, str etc.
    Triggers: Tuple of Trigger.
        Trigger: Tuple of Literal, Literal.
    Address: Tuple of Partials.
        Partial: Tuple of Literal, Literal, str, int, int
    Arguments: Tuple of Partials.

MessageMIDI is made of these New Types:

    MsgConfig.
    Triggers.
    MidiMsg: New Type of tuple of Literal, Literal, etc.
    MidiValues: Tuple of MidiValue.
        MidiValue: Tuple of Literal, str, etc.
    
MessageLOCAL is made of:

    Enabled: bool.
    Triggers.
    LocalSrc: Tuple of Literals, str, etc.
    LocalDst: Tuple of Literals, str, etc.

"""
from typing import Literal, TypeAlias, NewType, Protocol
import xml.etree.ElementTree as ET

__all__ = [
    # Property
    "PropertyType",
    "PropertyValue",
    "Property",
    # Value
    "ValueType",
    "ValueDefault",
    "Value",
    # Messages
    "PartialType",
    "ConversionType",
    "TriggerType",
    "MidiMsgType",
    "Trigger",
    "Partial",
    "MsgConfig",
    "MidiValue",
    "MidiMsg",
    "LocalSrc",
    "LocalDst",
    "MessageOSC",
    "MessageMIDI",
    "MessageLOCAL",
    "Message",
    # Control
    "ControlType",
    "Control",
    # External
    "Element",
]

Element = ET.Element
"""Alias for XML Element regarless of library used."""

ControlType: TypeAlias = Literal[
    "BOX",
    "BUTTON",
    "ENCODER",
    "FADER",
    "GRID",
    "GROUP",
    "LABEL",
    "PAGE",
    "PAGER",
    "RADAR",
    "RADIAL",
    "RADIO",
    "TEXT",
    "XY",
]
"""Valid literals for <node type:ControlType>"""
PropertyType: TypeAlias = Literal["b", "c", "r", "f", "i", "s"]
"""Valid literals for <property type:PropertyType> b: boolean, c: color, r: frame, f: float, i: int, s: string"""
PropertyValue: TypeAlias = (
    str | int | float | bool | tuple[int, ...] | tuple[float, ...]
)
"""Possible python types for a Property's value."""
Property: TypeAlias = tuple[str, PropertyValue]
"""
Property:
    [0] - Property Key(str): Name/key of the property.
    [1] - PropertyValue: Any str, int, float, bool, PropertyFrame or PropertyColor.
    The Python type/TypeAlias will be converted to a literal for XML.
    Type str will be "s", bool will be "b", etc.
    PropertyFrame converts to:
        {"x":[1][0], "y":[1][1], "w":[1][2], "h":[1][3]}

Example:
    ("name", "Craig")

    <property type="s">
        <key>name</key>
        <value>Craig</value>
    </property>

    ("frame",(0,0,100,100))

    <property type="r">
        <key>frame</key>
        <value>
            <x>0</x>
            <y>0</y>
            <w>100</w>
            <h>100</h>
        </value>
    </property>

"""
ValueType: TypeAlias = Literal["x", "y", "touch", "text", "page"]
ValueDefault: TypeAlias = float | int | bool | str
Value: TypeAlias = tuple[ValueType, bool, bool, float | int | bool | str, int]
""" 
Value:
    [0] - ValueKey: Any of the allowed literals.
    [1] - locked: Boolean.
    [2] - lockedDefaultCurrent: Boolean.
    [3] - ValueDefault: str, bool or float. "x" and "y" use floats, "touch" is bool, "text" is str.
    [4] - defaultPull: Integer between 0 and 100.
"""

"""
LOWER MESSAGE TYPES:
"""
PartialType: TypeAlias = Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"]
ConversionType: TypeAlias = Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"]
Partial = NewType(
    "Partial",
    tuple[
        PartialType,
        ConversionType,
        str,
        int,
        int,
    ],
)
""" Partial:
This is the unit with which the OSC message is constructed.
So in a message like track/1/fx/8, the partials are: "track", "1", "fx", "8".
They can be dynamic, so if the Control name is "fx" the partial would look like: track/1/name/8. 

[0] - PartialType: Any of the allowed literals.
[1] - PartialConversion: Any of the allowed literals. 
[2] - value: Depends on the Partial Type. 
CONSTANT: Value is any string, frequently "/".
INDEX: Any int, as str.
VALUE: Any of the allowed ValueKey literals.
PROPERTY: Any str.
[3] - scaleMin: Range of Value.
[4] - scaleMax: Range of Value.
"""
TriggerType: TypeAlias = Literal["ANY", "RISE", "FALL"]
Trigger = NewType("Trigger", tuple[ValueType, TriggerType])
"""
Trigger:

This is the Value that triggers the OSC/MIDI/LOCAL message.

    [0] - TriggerType: Any of the valid literals ["x", "y", "touch", "text"].
    [1] - TriggerCondition: Any of the valid literals ["ANY", "RISE", "FALL"].
"""
MidiMsgType: TypeAlias = Literal[
    "NOTE_OFF",
    "NOTE_ON",
    "POLYPRESSURE",
    "CONTROLCHANGE",
    "PROGRAMCHANGE",
    "CHANNELPRESSURE",
    "PITCHBEND",
    "SYSTEMEXCLUSIVE",
]
MidiMsg = NewType(
    "MidiMsg",
    tuple[
        MidiMsgType,
        int,
        str,
        str,
    ],
)
"""
Midi Message:

    [0] - MidiMessageType: One of the valid literals.
    [1] - MidiChannel: Integer, typical 1-16 midi channel.
    [2] - data1: Depends, WIP.
    [3] - data2: Depends, WIP.
"""
MidiValue = NewType("MidiValue", tuple[PartialType, str, int, int])
"""
MidiValue:

    [0] - MidiValueType: Any of the valid literals. ["CONSTANT", "INDEX", "VALUE", "PROPERTY"]
    [1] - key: Depends on the MidiValueType. Can be a ValueType or PropertyKey, etc.
    [2] - scaleMin: int 0 to 127 
    [3] - scaleMax: int 0 to 127
"""
MsgConfig = NewType("MsgConfig", tuple[bool, bool, bool, bool, str])
"""
Connection: 

    [0] - Enabled: Bool.
    [1] - Send: Bool.
    [2] - Receive: Bool.
    [3] - Feedback: Bool.
    [4] - Connections (str as binary), so connection 1 is 00001, connection 2 is 00010, both are 00011.
"""
LocalSrc = NewType(
    "LocalSrc",
    tuple[
        PartialType,
        ConversionType,
        str,
        int,
        int,
    ],
)
"""
LocalSrc:

    [0] - Valid Literal Type
    [1] - Valid Literal Conversion
    [2] - Source Value/Property/etc 
    [3] - Min range
    [4] - Max range
"""
LocalDst = NewType("LocalDst", tuple[PartialType, str, str])
"""
LocalDst:
    [0] - Destination Type
    [1] - Destination Var
    [2] - Destination ID
"""

""" 
HIGHER MESSAGE TYPES
"""
MessageMIDI = NewType(
    "MessageMIDI",
    tuple[
        Literal["midi"], MsgConfig, tuple[Trigger, ...], MidiMsg, tuple[MidiValue, ...]
    ],
)
MessageOSC = NewType(
    "MessageOSC",
    tuple[
        Literal["osc"],
        MsgConfig,
        tuple[Trigger, ...],
        tuple[Partial, ...],
        tuple[Partial, ...],
    ],
)
"""
MessageOSC:
    [0] - Tag: osc
    [1] - MsgConfig: Tuple of Enabled, Send, Receive, Feedback, Connections.
    [2] - Triggers: Tuple of Trigger.
    [3] - Address: Construct a message with tuple of Partial.
    [4] - Arguments: Construct arguments with tuple of Partial.
"""
"""
MessageMIDI:

    [0] - Tag: midi.
    [1] - MsgConfig: Tuple of Enabled, Send, Receive, Feedback, Connections.
    [2] - Triggers (tuple). 
    [3] - Message: See MidiMessage.
    [4] - Value (tuple): See :type:`tosclib.elements.MidiValue`
"""
MessageLOCAL = NewType(
    "MessageLOCAL",
    tuple[Literal["local"], bool, tuple[Trigger, ...], LocalSrc, LocalDst],
)
"""
MessageLOCAL:

    [0] - Tag: local.
    [1] - Enabled: Bool.
    [2] - Triggers: Tuple of Trigger. 
    [3] - Source: Tuple of value, valid literal.
    [4] - Target: Tuple of value, id.
"""
Message: TypeAlias = MessageOSC | MessageMIDI | MessageLOCAL
"""Any of the possible message types."""

"""
CONTROL PROTOCOL
"""


class Control(Protocol):
    """Protocol for Control classes.

    Args:
        type (ControlType): Required field. ControlType Literal.
        id (str, optional): Random uuid4. Defaults to None.
        values (list[Value], optional): List of Value objects. Defaults to None.
        messages (list[Message], optional): List of Message objects. Defaults to None.
        children (list[Control], optional): List of Node objects. Defaults to None.
        args (Property): Pass any Property to create extra Property attributes.
        kwargs (PropertyValue): Pass any keywords with PropertyValues to create extra Property attributes.

    Note:

        This represents a Touch OSC Control but it's not an XML Element.

    Example:

        .. code-block:: python

            class Button:
                type: ControlType = "BOX"
                ...

            class Group:
                type: ControlType = "GROUP"
                ...

            button = Button(("name", "play")) # with args
            group = Group(name = "menu") # with kwargs

            assert button.name == ("name", "play")
            assert group.name == ("name", "menu")
            assert button.type != group.type

            group.children.append(button)


    Returns:
        Control: Protocol.
    """

    type: ControlType
    id: str
    values: list[Value]
    messages: list[Message]
    children: list["Control"]

    def __init__(self, id: str | None, *args: Property, **kwargs: PropertyValue):
        ...

    def get_prop(self, key: str) -> Property:
        """Get a Property (key, value) from its key."""
        ...

    def get_frame(self) -> tuple[int, ...]:
        """Get a tuple of integers, xywh."""
        ...

    def get_color(self) -> tuple[float, ...]:
        """Get a tuple of floats, rgba."""
        ...

    def set_prop(self, prop: Property) -> "Control":
        """

        Args:
            prop (Property):

        Returns:
            Control: chain.
        """
        ...

    def set_frame(self, frame: tuple[int, ...]) -> "Control":
        """

        Args:
            frame (tuple[int, ...]):

        Returns:
            Control: chain.
        """
        ...

    def set_color(self, color: tuple[float, ...]) -> "Control":
        """

        Args:
            color (tuple[float, ...]):

        Returns:
            Control: chain.
        """
        ...
