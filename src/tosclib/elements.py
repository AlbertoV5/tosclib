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

from typing import Literal, NewType, Protocol, TypeAlias, Callable

__all__ = [
    # Enums
    "ElementTag",
    "ControlType",
    "ControlList",
    # Properties
    "PropertyType",
    "PropertyValue",
    "Property",
    # Values
    "Value",
    "Values",
    # Messages
    "MsgConfig",
    "Partial",
    "Trigger",
    "MidiMsg",
    "MidiValue",
    "MidiValues",
    "LocalSrc",
    "LocalDst",
    "Triggers",
    "Address",
    "Arguments",
    "MessageOSC",
    "MessageMIDI",
    "MessageLOCAL",
    "Message",
    "Messages",
    # Children
    "Children",
    "Control",
]

ElementTag: TypeAlias = Literal[
    "node",
    "properties",
    "values",
    "messages",
    "children",
    "property",
    "value",
    "osc",
    "midi",
    "local",
    "gamepad",
]
"""Valid literals for xml element tags."""
ControlType: TypeAlias = Literal[
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
]
ControlList: list[ControlType] = [
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
]
"""Valid literals for <node type:ControlType>"""
PropertyType: TypeAlias = Literal["b", "c", "r", "f", "i", "s"]
"""Valid literals for <property type:PropertyType>
    b: boolean, c: color, r: frame, f: float, i: int, s: string
"""
PropertyValue: TypeAlias = (
    str | int | float | bool | tuple[int, ...] | tuple[float, ...]
)
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
Value: TypeAlias = tuple[
    Literal["x", "y", "touch", "text"], bool, bool, float | bool | str, int
]
""" 
Value:
    [0] - ValueKey: Any of the allowed literals.
    [1] - locked: Boolean.
    [2] - lockedDefaultCurrent: Boolean.
    [3] - ValueDefault: str, bool or float. "x" and "y" use floats, "touch" is bool, "text" is str.
    [4] - defaultPull: Integer between 0 and 100.
"""
Values: TypeAlias = list[Value]
Partial = NewType(
    "Partial",
    tuple[
        Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"],
        Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"],
        str,
        int,
        int,
    ],
)
""" 
Partial:
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
Trigger = NewType(
    "Trigger", tuple[Literal["x", "y", "touch", "text"], Literal["ANY", "RISE", "FALL"]]
)
"""
Trigger:

This is the Value that triggers the OSC/MIDI/LOCAL message.

    [0] - TriggerType: Any of the valid literals ["x", "y", "touch", "text"].
    [1] - TriggerCondition: Any of the valid literals ["ANY", "RISE", "FALL"].
"""
MidiMsg = NewType(
    "MidiMsg",
    tuple[
        Literal[
            "NOTE_OFF",
            "NOTE_ON",
            "POLYPRESSURE",
            "CONTROLCHANGE",
            "PROGRAMCHANGE",
            "CHANNELPRESSURE",
            "PITCHBEND",
            "SYSTEMEXCLUSIVE",
        ],
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
MidiValue = NewType(
    "MidiValue", tuple[Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"], str, int, int]
)
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
Triggers: TypeAlias = tuple[Trigger, ...]
"""Tuple of Trigger"""
Address: TypeAlias = tuple[Partial, ...]
"""Tuple of Partial"""
Arguments: TypeAlias = tuple[Partial, ...]
"""Tuple of Partial"""
MessageOSC = NewType(
    "MessageOSC", tuple[Literal["osc"], MsgConfig, Triggers, Address, Arguments]
)
"""
MessageOSC:
    [0] - Tag: osc
    [1] - MsgConfig: Tuple of Enabled, Send, Receive, Feedback, Connections.
    [2] - Triggers: Tuple of Trigger.
    [3] - Address: Construct a message with tuple of Partial.
    [4] - Arguments: Construct arguments with tuple of Partial.
"""
MidiValues: TypeAlias = tuple[MidiValue, ...]
"""Tuple of MidiValue"""
MessageMIDI = NewType(
    "MessageMIDI", tuple[Literal["midi"], MsgConfig, Triggers, MidiMsg, MidiValues]
)
"""
MessageMIDI:

    [0] - Tag: midi.
    [1] - MsgConfig: Tuple of Enabled, Send, Receive, Feedback, Connections.
    [2] - Triggers (tuple). 
    [3] - Message: See MidiMessage.
    [4] - Value (tuple): See :type:`tosclib.elements.MidiValue`
"""
LocalSrc = NewType(
    "LocalSrc",
    tuple[
        Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"],
        Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"],
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
LocalDst = NewType(
    "LocalDst", tuple[Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"], str, str]
)
"""
LocalDst:
    [0] - Destination Type
    [1] - Destination Var
    [2] - Destination ID
"""
MessageLOCAL = NewType(
    "MessageLOCAL", tuple[Literal["local"], bool, Triggers, LocalSrc, LocalDst]
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
Messages: TypeAlias = list[MessageOSC | MessageMIDI | MessageLOCAL]

Properties: TypeAlias = list[Property]
Children: TypeAlias = list["Control"]


class Control(Protocol):
    """The Control Type Protocol. Touch OSC Control

    Attributes:
        type(ControlType): Any of the valid literals.
        id(str): Any hash function result as str.
        values(Values|[]]): The Control's Values.
        messages(Values|[]]): The Control's Messages.
        children(Children|[]]): The Control's Control children.

    """

    type: ControlType
    id: str
    values: Values
    messages: Messages
    children: Children

    def get_prop(self, key: str) -> Property:
        ...

    def get_frame(self) -> tuple[int, ...]:
        ...

    def get_color(self) -> tuple[float, ...]:
        ...

    def set_prop(self, *args: Property) -> "Control":
        ...
