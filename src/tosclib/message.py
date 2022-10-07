"""Message Module"""
from typing import Literal, TypeAlias, TypedDict
from pydantic import BaseModel, Field

from .value import ValueKey


TriggerCondition: TypeAlias = Literal["ANY", "RISE", "FALL"]
SourceType: TypeAlias = Literal["CONSTANT", "INDEX", "VALUE", "PROPERTY"]
Conversion: TypeAlias = Literal["BOOLEAN", "INTEGER", "FLOAT", "STRING"]
MidiType: TypeAlias = Literal[
    "NOTE_OFF",
    "NOTE_ON",
    "POLYPRESSURE",
    "CONTROLCHANGE",
    "PROGRAMCHANGE",
    "CHANNELPRESSURE",
    "PITCHBEND",
    "SYSTEMEXCLUSIVE",
]


class Trigger(BaseModel):
    """Model for Message's Trigger.
    https://hexler.net/touchosc/manual/editor-messages-midi#trigger
    """

    var: ValueKey = "x"
    condition: TriggerCondition = "ANY"

    class Config:
        validate_assignment = True


class Partial(BaseModel):
    """Model for Argument and Path's Partial.
    https://hexler.net/touchosc/manual/editor-messages-osc#partials
    """

    type: SourceType = "CONSTANT"
    conversion: Conversion = "STRING"
    value: str = "/"
    scaleMin: int = 0
    scaleMax: int = 1

    class Config:
        validate_assignment = True


class MidiMessage(BaseModel):
    """Model for the Midi Message's Matching
    https://hexler.net/touchosc/manual/editor-messages-midi#matching
    """

    type: MidiType = "CONTROLCHANGE"
    channel: int = 0
    data1: str = "0"
    data2: str = "0"

    class Config:
        validate_assignment = True


class MidiValue(BaseModel):
    """Model for the Midi Message's Type and its data.
    https://hexler.net/touchosc/manual/editor-messages-midi#type
    """

    type: SourceType = "CONSTANT"
    key: str | None = ""
    scaleMin: int = 0
    scaleMax: int = 15

    class Config:
        validate_assignment = True


class Midi(BaseModel):
    """Model for the Control's Midi Message
    https://hexler.net/touchosc/manual/editor-messages-midi
    """

    enabled: bool = True
    send: bool = True
    receive: bool = True
    feedback: bool = False
    connections: str = Field(default="11111", min_length=5, max_length=5)
    triggers: list[Trigger] = [Trigger()]
    message: MidiMessage = MidiMessage()
    values: list[MidiValue] = [
        MidiValue(),
        MidiValue(type="INDEX", key="", scaleMin=0, scaleMax=1),
        MidiValue(type="VALUE", key="x", scaleMin=0, scaleMax=127),
    ]

    class Config:
        validate_assignment = True


class Osc(BaseModel):
    """Model for the Control's Osc Message
    https://hexler.net/touchosc/manual/editor-messages-osc
    """

    enabled: bool = True
    send: bool = True
    receive: bool = True
    feedback: bool = False
    connections: str = "11111"
    triggers: list[Trigger] = [Trigger()]
    path: list[Partial] = [
        Partial(),
        Partial(type="PROPERTY", conversion="STRING", value="name"),
    ]
    arguments: list[Partial] = [Partial(type="VALUE", conversion="FLOAT", value="x")]

    class Config:
        validate_assignment = True


class Local(BaseModel):
    """Model for the Control's Local Message.
    https://hexler.net/touchosc/manual/editor-messages-local
    """

    enabled: bool = True
    triggers: list[Trigger] = [Trigger()]
    type: SourceType = "VALUE"
    conversion: Conversion = "FLOAT"
    value: str = "x"
    scaleMin: int = 0
    scaleMax: int = 1
    dstType: SourceType = "VALUE"
    dstVar: str | None = None
    dstID: str | None = None

    class Config:
        validate_assignment = True


# class MessageDirectory(TypedDict):
#     osc: list[Osc]
#     midi: list[Midi]
#     local: list[Local]


MessageDirectory: TypeAlias = (
    dict[Literal["osc"], list[Osc]]
    | dict[Literal["midi"], list[Midi]]
    | dict[Literal["local"], list[Local]]
)
