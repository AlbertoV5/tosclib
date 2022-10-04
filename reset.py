from typing import Literal, Protocol, TypeAlias, Any
from pydantic import BaseModel
from pprint import pprint
import xmltodict
import json

PropertyType: TypeAlias = Literal["b", "c", "r", "f", "i", "s"]
PropertyValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | tuple[float, float, float, float]
    | tuple[int, int, int, int]
)
ValueDefault: TypeAlias = bool | float | int | str
ValueKey: TypeAlias = Literal["touch", "x", "y", "page", "text"]
Condition: TypeAlias = Literal["ANY", "RISE", "FALL"]
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
NodeType = Literal[
    "BOX",
    "BUTTON",
    "ENCODER",
    "FADER",
    "GRID",
    "GROUP",
    "LABEL",
    "PAGE",
    "RADAR",
    "RADIAL",
    "RADIO",
    "TEXT",
    "XY",
]
MessageType = Literal["osc", "midi", "local"]


class Trigger(BaseModel):
    var: ValueKey = "x"
    condition: Condition = "ANY"


class Partial(BaseModel):
    type: SourceType = "CONSTANT"
    conversion: Conversion = "STRING"
    value: str = "/"
    scaleMin: int = 0
    scaleMax: int = 1


class MidiMessage(BaseModel):
    type: MidiType = "CONTROLCHANGE"
    channel: int = 0
    data1: str = "0"
    data2: str = "0"


class MidiValue(BaseModel):
    key: str | None = ""
    scaleMax: int = 15
    scaleMin: int = 0
    type: SourceType = "CONSTANT"


class Property(BaseModel):
    attr_type: PropertyType
    key: str
    value: PropertyValue

    # def __init__(__pydantic_self__, **data) -> None:
    #     # redundant
    #     super().__init__(**data)
    #     match __pydantic_self__.attr_type:
    #         case 'b':
    #             __pydantic_self__.value = bool(__pydantic_self__.value)
    #         case 'i':
    #             __pydantic_self__.value = int(__pydantic_self__.value)
    #         case 'f':
    #             __pydantic_self__.value = float(__pydantic_self__.value)
    #         case 's':
    #             __pydantic_self__.value = str(__pydantic_self__.value)
    #         case 'c':
    #             __pydantic_self__.value = {k: float(v) for k, v in __pydantic_self__.value.items()}
    #         case 'r':
    #             __pydantic_self__.value = {k: int(v) for k, v in __pydantic_self__.value.items()}
    #         case _:
    #             __pydantic_self__.value = str(__pydantic_self__.value)


class Value(BaseModel):
    name: ValueKey = "touch"
    locked: bool = False
    locked_dc: bool = False
    default: ValueDefault = False
    pull: int = 0


class MIDI(BaseModel):
    enabled: bool = True
    send: bool = True
    receive: bool = True
    feedback: bool = False
    connections: str = "11111"
    triggers: list[Trigger] = [Trigger()]
    message: MidiMessage = MidiMessage()
    values: list[MidiValue] = [
        MidiValue(),
        MidiValue(type="INDEX", key="", scaleMin=0, scaleMax=1),
        MidiValue(type="VALUE", key="x", scaleMin=0, scaleMax=127),
    ]


class OSC(BaseModel):
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


class LOCAL(BaseModel):
    enabled: bool = True
    triggers: list[Trigger] = [Trigger()]
    type: SourceType = "VALUE"
    conversion: Conversion = "FLOAT"
    value: str = "x"
    scaleMin: int = 0
    scaleMax: int = 1
    dstType: SourceType = "VALUE"
    dstVar: str = ""
    dstID: str = ""


Message: TypeAlias = OSC | MIDI | LOCAL


class Node(BaseModel):
    attr_ID: str
    attr_type: NodeType
    properties: list[Property]
    values: list[Value]
    messages: dict[MessageType, list[Message]] | None
    children: list["Node"] | None


class Root(BaseModel):
    attr_version: float
    node: Node


class Template:
    root: Root
    filepath: str
    encoding: str = "UTF-8"

    def __init__(self, filepath: str):
        self.filepath = filepath
        with open(filepath, "rb") as file:
            self.root = Root(
                **xmltodict.parse(
                    file, attr_prefix="attr_", postprocessor=self.postprocessor
                )["lexml"]
            )

    def __repr__(self):
        return f"Template: {self.root.node.attr_ID}, {self.filepath}"

    def postprocessor(self, path: tuple, key: str, value: str):
        """Reorganize elements based on their structural patterns.

        Args:
            path (tuple): The structure of the path to the element.
            key (str): The key of the element, tag.
            value (str): The value of the element, text, attr.

        Returns:
            str, Any: Modified key, value structure.
        """
        # One-step patterns.
        # Match all stages on which the last element is the desired one.
        # We are using this to fix nested dictionaries and dictionaries that
        # should be a list of dictionaries. So we are replacing key:value with value
        # as well as value with [value].
        match path[-1]:
            case ("properties", None):
                return key, value["property"]
            case ("children", None):
                return key, value["node"] if isinstance(value["node"], list) else [
                    value["node"]
                ]
            case ("messages", None):
                k = next(iter(value))
                return key, value if isinstance(value[k], list) else {k: [value[k]]}
        # Two-step patterns.
        # If we want to change a pattern that appears with multiple parents, we can do it
        # by forcing a two step match where we match the parent and the element.
        # Here we use it for restructuring dictionaries into tuples and converting
        # strings to boolean, int or float, as well as similar procedures to the
        # one-step matching but making sure we are under a specific parent.
        match path[-2:]:
            case ((_, {"type": "c"}), ("value", None)):
                return key, tuple(float(value[k]) for k in dict(value))
            case ((_, {"type": "r"}), ("value", None)):
                return key, tuple(int(value[k]) for k in dict(value))
            case ((_, {"type": "b"}), ("value", None)):
                return key, True if value in ("1", "true") else False
            case ((_, {"type": "i"}), ("value", None)):
                return key, int(value)
            case ((_, {"type": "f"}), ("value", None)):
                return key, int(value)
            case (("node", _), ("values", None)):
                return key, value["value"] if isinstance(value["value"], list) else [
                    value["value"]
                ]
            case (_, ("path" | "arguments", None)):
                return key, value["partial"] if isinstance(
                    value["partial"], list
                ) else [value["partial"]]
            case (_, ("triggers", None)):
                return key, value["trigger"] if isinstance(
                    value["trigger"], list
                ) else [value["trigger"]]
            case (("midi", None), ("values", _)):
                return key, value["value"]
        return key, value


# XML to dict
f = "docs/demos/files/msgs.xml"
t = Template(f)
print(t.root.node)
# pprint(node['children'][0]['messages'])
# nx = Node(**node)
# pprint(nx.children[0].messages)
