"""
Types based on Hexler's Touch OSC Enumerations.

Using typing to define specific tuple shapes and Literals.

The result is no regular classes for these data structures,
this means that most of the logical work relies on the factory
and converter methods in other modules. 

"""
from typing import ClassVar, Literal, TypeAlias, NewType, Protocol

__all__ = [
    # Property
    "PropertyType",
    "PropertyValue",
    "Property",
    # Value
    "ValueKey",
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
    "MessageType",
    # Control
    "ControlType",
    "Control",
]


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
PropertyType: TypeAlias = Literal["b", "c", "r", "f", "i", "s"]
"""PropertyType"""
PropertyValue: TypeAlias = (
    str | int | float | bool | tuple[int, ...] | tuple[float, ...]
)
"""PropertyValue"""
# Property: TypeAlias = tuple[str, PropertyValue]
Property = NewType("Property", tuple[str, PropertyValue])
""" 
    - key: str
    - value (str | int | float | bool | tuple[int,...] | tuple[float,...])
"""
ValueKey: TypeAlias = Literal["x", "y", "page", "touch", "text"]
"""ValueKey"""
ValueDefault: TypeAlias = float | int | bool | str
"""ValueDefault"""
# Value: TypeAlias = tuple[ValueKey, bool, bool, float | int | bool | str, int]
Value = NewType("Value", tuple[ValueKey, bool, bool, float | int | bool | str, int])
"""Value"""
PartialType: TypeAlias = Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"]
"""PartialType"""
ConversionType: TypeAlias = Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"]
"""ConversionType"""
Partial = NewType("Partial", tuple[PartialType, ConversionType, str, int, int])
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
Trigger = NewType("Trigger", tuple[ValueKey, TriggerType])
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
Args:
    Tag ("osc")
    MsgConfig (MsgConfig)
    Triggers (tuple[Trigger, ...])
    Path (tuple[Partial, ...])
    Arguments (tuple[Partial, ...])
"""
MessageMIDI = NewType(
    "MessageMIDI",
    tuple[
        Literal["midi"], MsgConfig, tuple[Trigger, ...], MidiMsg, tuple[MidiValue, ...]
    ],
)
"""
Args:

    Tag ("midi")
    MsgConfig (MsgConfig)
    Triggers (tuple[Trigger,...])
    Message (MidiMsg)
    Value (tuple[MidiValue,...])
"""
MessageLOCAL = NewType(
    "MessageLOCAL",
    tuple[Literal["local"], bool, tuple[Trigger, ...], LocalSrc, LocalDst],
)
"""
Args:
    Tag ("local")
    Enabled (bool)
    Triggers (tuple[Trigger, ...])
    LocalSrc (LocalSrc)
    LocalDst (LocalDst)
"""
MessageType: TypeAlias = Literal["osc", "midi", "local"]
Message: TypeAlias = MessageOSC | MessageMIDI | MessageLOCAL

"""
CONTROL PROTOCOL
"""


class Control(Protocol):
    """Protocol for Control classes.

    This represents a Touch OSC Control. It's not an XML Element.

    Args:
        type (ControlType): Required Control class identifier, BOX, BUTTON, etc.
        id (str, optional): Custom id, defaults to random uuid4.
        props (dict[str, PropertyValue]): Dict of Property stored as {str, PropertyValue}.
        values (list[Value], optional): List of Value type tuples.
        messages (list[Message], optional): List of Message type tuples.
        children (list[Control], optional): List of Control objects.

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
        Control: Control.
    """

    id: str
    type: ClassVar[ControlType]
    props: dict[str, PropertyValue]
    values: dict[ValueKey, Value]
    messages: list[Message]
    children: list["Control"]

    def __init__(self, id=None, props=None, values=None, messages=None, children=None):
        ...

    def get(self, key: str) -> PropertyValue:
        ...

    def set(self, key: str, value: PropertyValue) -> "Control":
        ...

    def get_frame(self) -> tuple[int, ...]:
        ...

    def get_color(self) -> tuple[float, ...]:
        ...

    def set_frame(self, frame: tuple[int, ...]) -> "Control":
        ...

    def set_color(self, color: tuple[float, ...]) -> "Control":
        ...
