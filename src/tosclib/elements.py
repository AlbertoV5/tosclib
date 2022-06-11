"""
This module contains Constants as Type Aliases and Literals.
"""

from typing import Literal, NewType, TypeAlias
import uuid

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
"""Valid literals for <node type:ControlType>"""
PropertyType: TypeAlias = Literal["b", "c", "r", "f", "i", "s"]
"""Valid literals for <property type:PropertyType>
    b: boolean, c: color, r: frame, f: float, i: int, s: string
"""
Property: TypeAlias = str | int | float | bool | tuple[int, ...] | tuple[float, ...]
"""
Property:
    [0] - PropertyValue: Any str, int, float, bool, PropertyFrame or PropertyColor.
    The Python type/TypeAlias will be converted to a literal for XML.
    Type str will be "s", bool will be "b", etc.
    PropertyFrame converts to:
        {"x":[1][0], "y":[1][1], "w":[1][2], "h":[1][3]}

Example:
    name = "Craig"

    <property type="s">
        <key>name</key>
        <value>Craig</value>
    </property>

    frame = (0,0,100,100)

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
Value = NewType(
    "Value",
    tuple[Literal["x", "y", "touch", "text"], bool, bool, float | bool | str, int],
)
""" 
Value:
    [0] - ValueKey: Any of the allowed literals.
    [1] - locked: Boolean.
    [2] - lockedDefaultCurrent: Boolean.
    [3] - ValueDefault: str, bool or float. "x" and "y" use floats, "touch" is bool, "text" is str.
    [4] - defaultPull: Integer between 0 and 100.
"""
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
    "MidiValue", tuple[str, Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"], int, int]
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
Triggers = NewType("Triggers", tuple[Trigger, ...])
"""Tuple of Trigger"""
Address = NewType("Address", tuple[Partial, ...])
"""Tuple of Partial"""
Arguments = NewType("Arguments", tuple[Partial, ...])
"""Tuple of Partial"""
MessageOSC = NewType("MessageOSC", tuple[MsgConfig, Triggers, Address, Arguments])
"""
MessageOSC:

    [0] - MsgConfig: Tuple of Enabled, Send, Receive, Feedback, Connections.
    [1] - Triggers: Tuple of Trigger.
    [2] - Address: Construct a message with tuple of Partial.
    [3] - Arguments: Construct arguments with tuple of Partial.
"""
msgo = MessageOSC(
    (
        MsgConfig((True, True, True, False, "00001")),
        Triggers((Trigger(("x", "ANY")),)),
        Address(
            (
                Partial(("CONSTANT", "STRING", "/", 0, 1)),
                Partial(("PROPERTY", "STRING", "name", 0, 1)),
            )
        ),
        Arguments((Partial(("VALUE", "FLOAT", "x", 0, 1)),)),
    )
)
MidiMsgs = NewType("MidiMsgs", tuple[MidiMsg, ...])
"""Tuple of MidiMsg"""
MidiValues = NewType("MidiValues", tuple[MidiValue, ...])
"""Tuple of MidiValue"""
MessageMIDI = NewType("MessageMIDI", tuple[MsgConfig, Triggers, MidiMsgs, MidiValues])
"""
MessageMIDI:

    [0] - MsgConfig: Tuple of Enabled, Send, Receive, Feedback, Connections.
    [1] - Triggers (tuple). 
    [2] - Message (tuple): See MidiMessage.
    [3] - Value (tuple): See :type:`tosclib.elements.MidiValue`
"""
LocalSrc = NewType(
    "LocalSrc", tuple[str, Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"]]
)
"""[0] - Source Value/Property/etc, [1] - Valid Literal"""
LocalDst = NewType("LocalDst", tuple[str, str])
"""[0] - Target Value/Property, [1] - Target ID"""
LocalCon = NewType(
    "LocalCon", tuple[int, int, Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"]]
)
"""[0] - Min range, [1] - Max range, [2] - Valid Literal"""
MessageLOCAL = NewType(
    "MessageLOCAL", tuple[bool, Triggers, LocalSrc, LocalDst, LocalCon]
)
"""
MessageLOCAL:

    [0] - Enabled: Bool.
    [1] - Triggers: Tuple of Trigger. 
    [2] - Source: Tuple of value, valid literal.
    [3] - Target: Tuple of value, id.
    [4] - Con: Tuple of Min, Max, valid literal.
"""
# Values: TypeAlias = tuple[Value, ...] | None
Values = NewType("Values", tuple[Value, ...])
Messages = NewType("Messages", tuple[MessageOSC | MessageMIDI | MessageLOCAL, ...])
Children = NewType("Children", tuple["Control", ...])


class Control:
    def __init__(
        self,
        type: ControlType,
        id: str = None,
        values: Values = None,
        messages: Messages = None,
        children: Children = None,
        **kwargs: Property
    ):
        """The base class of a Touch OSC Control. Not an XML Element.

        Args:
            type (ControlType): Required field. ControlType Literal.
            id (str, optional): Random uuid4. Defaults to None.
            values (Values, optional): Tuple of Value objects. Defaults to None.
            messages (Messages, optional): Tuple of Message objects. Defaults to None.
            children (tuple[&quot;Node&quot;], optional): Tuple of Node objects. Defaults to None.
            kwargs (dict[str, Property]): Pass any extra keyword arguments as Property objects.
        """
        self.id: str = str(uuid.uuid4()) if id is None else id
        self.type: ControlType = type
        self.values: Values | None = None if values is None else values
        self.messages: Messages | None = None if messages is None else messages
        self.children: Children | None = None if children is None else children

        for k in kwargs:
            setattr(self, k, kwargs[k])


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


def msg_midimsgs(*args: MidiMsg) -> MidiMsgs:
    """Midi Messages factory"""
    return MidiMsgs(tuple(arg for arg in args))


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
    key: str = "x", typ: Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"] = "VALUE"
) -> LocalSrc:
    """Local Source factory"""
    return LocalSrc((key, typ))


def msg_localdst(key: str = " ", id: str = " ") -> LocalDst:
    """Local Destination factory"""
    return LocalDst((key, id))


def msg_localcon(
    minRange: int = 0,
    maxRange: int = 1,
    conversion: Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"] = "STRING",
) -> LocalCon:
    """Local Conversion factory"""
    return LocalCon((minRange, maxRange, conversion))


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
    messages: MidiMsgs = None,
    values: MidiValues = None,
) -> MessageMIDI:
    """MIDI Message Factory"""
    config = msg_config() if config is None else config
    triggers = msg_triggers() if triggers is None else triggers
    messages = msg_midimsgs() if messages is None else messages
    values = msg_midivals() if values is None else values
    return MessageMIDI((config, triggers, messages, values))


def local(
    enabled: bool = None,
    triggers: Triggers = None,
    source: LocalSrc = None,
    destination: LocalDst = None,
    conversion: LocalCon = None,
) -> MessageLOCAL:
    """LOCAL Message factory"""
    enabled = True if enabled is None else enabled
    triggers = msg_triggers() if triggers is None else triggers
    source = msg_localsrc() if source is None else source
    destination = msg_localdst() if destination is None else destination
    conversion = msg_localcon() if conversion is None else conversion
    return MessageLOCAL((enabled, triggers, source, destination, conversion))


# class PropertyFactory:
#     @classmethod
#     def buildAny(
#         cls,
#         key:str,
#         value: int | bool | float | str | tuple[int,...] | tuple[float,...]
#     ) -> property:
#         """_summary_
#         Args:
#             key (_type_): _description_
#             value (int | bool | float | str | tuple[int] | tuple[float]):
#             Whatever value with one of those python types.
#             Tuples of ints are considered Frames.
#             Tuples of floats are considered Colors.

#         Raises:
#             ValueError:
#             If value type is not compatible with TouchOSC's equivalent.

#         Returns:
#             Property: _description_
#         """
#         if isinstance(value, str):
#             return cls.buildString(key, value)
#         elif isinstance(value, bool):
#             return cls.buildBoolean(key, value)
#         elif isinstance(value, int):
#             return cls.buildInteger(key, value)
#         elif isinstance(value, float):
#             return cls.buildFloat(key, value)
#         elif isinstance(value, tuple) and cls.isTupleInts(value):
#             return cls.buildFrame(key, value)
#         elif isinstance(value, tuple) and all(isinstance(x, float) for x in value):
#             return cls.buildColor(key, value)
#         else:
#             raise ValueError(f"""
# {key}-{value} type is not a valid PropertyType.
# Make sure all types in the tuples match.""")

#     @classmethod
#     def isTupleInts(cls, val:tuple[object,...]) -> TypeGuard[tuple[int,...]]:
#         return all(isinstance(x, int) for x in val)

#     @classmethod
#     def buildBoolean(cls, key: str, value: bool) -> Property:
#         return Property(PropertyType.BOOLEAN.value, key, repr(int(value)))

#     @classmethod
#     def buildString(cls, key: str, value: str) -> Property:
#         return Property(PropertyType.STRING.value, key, value)

#     @classmethod
#     def buildInteger(cls, key: str, value: int) -> Property:
#         return Property(PropertyType.INTEGER.value, key, repr(value))

#     @classmethod
#     def buildFloat(cls, key: str, value: float) -> Property:
#         return Property(PropertyType.FLOAT.value, key, repr(value))

#     @classmethod
#     def buildColor(cls, key: str, value: tuple[float,...]) -> Property:
#         return Property(
#             PropertyType.COLOR.value,
#             key,
#             "",
#             {
#                 "r": repr(value[0]),
#                 "g": repr(value[1]),
#                 "b": repr(value[2]),
#                 "a": repr(value[3]),
#             },
#         )

#     @classmethod
#     def buildFrame(cls, key: str, value: tuple[int,...]) -> Property:
#         return Property(
#             PropertyType.FRAME.value,
#             key,
#             "",
#             {
#                 "x": repr(value[0]),
#                 "y": repr(value[1]),
#                 "w": repr(value[2]),
#                 "h": repr(value[3]),
#             },
#         )

#     @classmethod
#     def name(cls, value: str) -> Property:
#         return cls.buildString("name", value)

#     @classmethod
#     def tag(cls, value: str) -> Property:
#         return cls.buildString("tag", value)

#     @classmethod
#     def script(cls, value: str) -> Property:
#         return cls.buildString("script", value)

#     @classmethod
#     def frame(cls, params: tuple[int,...]) -> Property:
#         return cls.buildFrame("frame", params)

#     @classmethod
#     def color(cls, params: tuple[float,...]) -> Property:
#         return cls.buildColor("color", params)

#     @classmethod
#     def locked(cls, value: bool) -> Property:
#         return cls.buildBoolean("locked", value)

#     @classmethod
#     def visible(cls, value: bool) -> Property:
#         return cls.buildBoolean("visible", value)

#     @classmethod
#     def interactive(cls, value: bool) -> Property:
#         return cls.buildBoolean("interactive", value)

#     @classmethod
#     def background(cls, value: bool) -> Property:
#         return cls.buildBoolean("background", value)

#     @classmethod
#     def outline(cls, value: bool) -> Property:
#         return cls.buildBoolean("outline", value)

#     @classmethod
#     def outlineStyle(cls, value: int) -> Property:
#         return cls.buildInteger("outline", value)

#     @classmethod
#     def textColor(cls, params: tuple[float,...]) -> Property:
#         return cls.buildColor("textColor", params)

#     @classmethod
#     def textSize(cls, value: int) -> Property:
#         return cls.buildInteger("textSize", value)


# class ValueFactory:
#     @classmethod
#     def build(
#         cls,
#         key:str,
#         value: int | bool | float | str | tuple[int,...] | tuple[float,...]
#     ):
#         return
