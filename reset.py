"""
tosclib

This file re-implements the entire tosclib parsing module using:
    1. xmltodict
    2. pydantic

TODO:
    1. Methods for models
    2. Rewrite layouts
"""
from typing import Literal, TypeAlias
from pydantic import BaseModel
from uuid import uuid4
import xmltodict
import zlib

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
    type: SourceType = "CONSTANT"
    key: str | None = ""
    scaleMin: int = 0
    scaleMax: int = 15


class Property(BaseModel):
    at_type: PropertyType
    key: str
    value: PropertyValue

    def __init__(__pydantic_self__, **data) -> None:
        """Enforces types based on self.at_type property."""
        super().__init__(**data)
        match __pydantic_self__.at_type:
            case "b":
                __pydantic_self__.value = (
                    True if __pydantic_self__.value == "1" else False
                )
            case "i":
                __pydantic_self__.value = int(__pydantic_self__.value)
            case "f":
                __pydantic_self__.value = float(__pydantic_self__.value)
            case "s":
                __pydantic_self__.value = str(__pydantic_self__.value)
            case "c":
                __pydantic_self__.value = tuple(
                    float(v) for v in __pydantic_self__.value
                )
            case "r":
                __pydantic_self__.value = tuple(int(v) for v in __pydantic_self__.value)
            case _:
                __pydantic_self__.value = str(__pydantic_self__.value)


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
    dstVar: str | None = None
    dstID: str | None = None


Messages: TypeAlias = (
    dict[Literal["osc"], list[OSC]]
    | dict[Literal["midi"], list[MIDI]]
    | dict[Literal["local"], list[LOCAL]]
)


class Node(BaseModel):
    at_ID: str = str(uuid4())
    at_type: NodeType = "GROUP"
    properties: list[Property] | None
    values: list[Value] | None
    messages: Messages | None
    children: list["Node"] | None

    def __getitem__(self, item):
        return self.children[item]


class Root(BaseModel):
    at_version: float
    node: Node


class Template:
    """Wrapper for loading and dumping xml <-> pydantic models"""

    root: Root
    filepath: str
    encoding: str = "UTF-8"

    def __init__(self, filepath: str):
        """Load a compressed .tosc or uncompressed .xml file and parse it.
        From XML to dictionary to Pydantic models.

        Args:
            filepath (str): .tosc file path.
        """
        self.filepath = filepath
        unzip = lambda x: zlib.decompress(x) if filepath.split(".")[1] == "tosc" else x
        with open(filepath, "rb") as file:
            self.root = Root(
                **xmltodict.parse(
                    unzip(file.read()),
                    attr_prefix="at_",
                    postprocessor=self.decode_postprocessor,
                )["lexml"]
            )

    def dump(self, filepath: str, pretty=True):
        """Write uncompressed .xml file.

        Args:
            filepath (str): XML file path.
        """
        with open(filepath, "w") as file:
            xmltodict.unparse(
                {"lexml": self.root.dict()},
                pretty=pretty,
                attr_prefix="at_",
                preprocessor=self.encode_preprocessor,
                output=file,
            )

    def dumps(self, pretty=True):
        """Returns a string representation.

        Returns:
            (str): XML string.
        """
        return xmltodict.unparse(
            {"lexml": self.root.dict()},
            pretty=pretty,
            attr_prefix="at_",
            preprocessor=self.encode_preprocessor,
        )

    def save(self, filepath: str):
        """Write contents to a compressed file.

        Args:
            filepath (str): File path.
        """
        with open(filepath, "wb") as file:
            file.write(
                zlib.compress(
                    xmltodict.unparse(
                        {"lexml": self.root.dict()},
                        attr_prefix="at_",
                        preprocessor=self.encode_preprocessor,
                    ).encode(self.encoding)
                )
            )

    def __repr__(self):
        return f"Template: {self.root.node.at_ID}, {self.filepath}"

    def decode_postprocessor(self, path: tuple, key: str, value: str):
        """Reorganize elements based on their patterns.

        Args:
            path (tuple): The structure of the path to the element.
            key (str): The key of the element, tag.
            value (str): The value of the element, text, attr.

        Returns:
            str, Any: Modified key, value structure.

        Description:

            1. One-step patterns.
            Match all stages on which the last element is the desired one.
            We are using this to fix nested dictionaries and dictionaries that
            should be a list of dictionaries. So we are replacing key:value with value
            as well as value with [value].

            2. Two-step patterns.
            If we want to change a pattern that appears with multiple parents, we can do it
            by forcing a two step match where we match the parent and the element.
            Here we use it for restructuring dictionaries into tuples and converting
            strings to boolean, int or float, as well as similar procedures to the
            one-step matching but making sure we are under a specific parent.
        """
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

        match path[-2:]:
            case ((_, {"type": "c"}), ("value", None)):
                return key, tuple(value[k] for k in dict(value))
            case ((_, {"type": "r"}), ("value", None)):
                return key, tuple(value[k] for k in dict(value))
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

    def encode_preprocessor(self, key: str, value: str):
        """Prepare encoding by key, value pattern matching.
        Reverts all the unpacking done from the encoding function.

        Args:
            key (str): Dictionary key from pydantic model attr.
            value (str): Dictionary value.

        Returns:
            (tuple): key, value pair with value modified.

        Description:
            The callback doesn't provide a path because the data is a dictionary
            so we only have key, value to match against element tag and content.
        """
        match key, value:
            case ("properties", list()):
                return key, {"property": value}
            case ("values", list()):
                return key, {"value": value}
            case ("children", list()):
                return key, {"node": value}
            case ("triggers", list()):
                return key, {"trigger": value}
            case ("path" | "arguments", list()):
                return key, {"partial": value}
            case ("value", (float(), float(), float(), float())):
                return key, {"r": value[0], "g": value[1], "b": value[2], "a": value[3]}
            case ("value", (int(), int(), int(), int())):
                return key, {"x": value[0], "y": value[1], "w": value[2], "h": value[3]}
            case ("value", bool()):
                return key, "0" if value == False else "1"
        return key, value


# XML to dict
f = "docs/demos/files/msgs.tosc"
t = Template(f)
# print(t.root.node[2].messages)
t.dump("deleteme.xml")
t.save("deleteme.tosc")
# n = Node()
# print(n)
