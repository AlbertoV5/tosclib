"""
tosclib

This file re-implements the entire tosclib parsing module using:
    1. xmltodict
    2. pydantic

TODO:
    1. Methods for models
    2. Rewrite layouts
"""
from pydantic import BaseModel, Field
from typing import Literal, TypeAlias
from pathlib import Path
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
ControlType = Literal[
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
    """Model for Message's Trigger.
    https://hexler.net/touchosc/manual/editor-messages-midi#trigger
    """

    var: ValueKey = "x"
    condition: Condition = "ANY"

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


class Property(BaseModel):
    """Model for the Control's Property.
    https://hexler.net/touchosc/manual/editor-control-properties
    """

    at_type: PropertyType
    key: str
    value: PropertyValue

    def __init__(__pydantic_self__, **data) -> None:
        """Enforces types based on self.at_type property.
        at_type: PropertyType
        key: str
        value: PropertyValue
        """
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

    class Config:
        validate_assignment = True


class Value(BaseModel):
    """Model for the Control's Values.
    https://hexler.net/touchosc/manual/editor-control-values
    """

    name: ValueKey = "touch"
    locked: bool = False
    locked_dc: bool = False
    default: ValueDefault = False
    pull: int = 0

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


Messages: TypeAlias = (
    dict[Literal["osc"], list[Osc]]
    | dict[Literal["midi"], list[Midi]]
    | dict[Literal["local"], list[Local]]
)


class Control(BaseModel):
    """Model for the Template's Control.
    The XML file labels a 'control' as 'node'.

    Access the Control's children via index notation.

    Example:
        child = control[0]

    https://hexler.net/touchosc/manual/editor-control
    """

    at_ID: str = str(uuid4())
    at_type: ControlType = "GROUP"
    properties: list[Property] = Field(default_factory=lambda: [])
    values: list[Value] = Field(default_factory=lambda: [])
    messages: Messages = Field(default_factory=lambda: [])
    children: list["Control"] = Field(default_factory=lambda: [], repr=False)

    def __getitem__(self, item):
        return self.children[item]

    def dumps(self, indent=2, exclude={"children"}, **kwargs):
        return self.json(indent=indent, exclude=exclude, **kwargs)

    class Config:
        validate_assignment = True


class Root(BaseModel):
    """Model for the XML root. Kept for structural consistency with XML."""

    at_version: float = 3.0
    control: Control = Field(default_factory=lambda: Control())

    class Config:
        validate_assignment = True


class Template:
    """Represents a .tosc file.

    It will parse and unparse the data from XML to Pydantic models and back.
    It doesn't deal with the structural content of the file and will keep a Root model
    before the first Control.

    Example:

        .. code-block::

            t = Template('myfile.tosc')
            msg = Midi()
            t.root.control[0].messages.append(msg)
            t.save('newfile.tosc')
    """

    root: Root
    encoding: str = "UTF-8"

    def __init__(self, filepath: str | Path | None = None):
        """Load a compressed .tosc or uncompressed .xml file and parse it.
        From XML to dictionary to Pydantic models.

        If filepath is None, it will create a new Template from defaults.

        Args:
            filepath (str): .tosc file path.
        """
        if filepath is None:
            self.root = Root()
            return None
        ext = (
            filepath.suffix
            if isinstance(filepath, Path)
            else f".{filepath.split('.')[1]}"
        )
        if ext not in (".xml", ".tosc"):
            raise ValueError(f"{ext} is not a valid file extension.")
        with open(filepath, "rb") as file:
            self.root = Root(
                **xmltodict.parse(
                    zlib.decompress(file.read()) if ext == ".tosc" else file.read(),
                    attr_prefix="at_",
                    postprocessor=self.decode_postprocessor,
                    encoding=self.encoding,
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
                indent="  ",
                attr_prefix="at_",
                preprocessor=self.encode_preprocessor,
                output=file,
                encoding=self.encoding,
            )

    def dumps(self, pretty=True):
        """Returns a string representation.

        Returns:
            (str): XML string.
        """
        return xmltodict.unparse(
            {"lexml": self.root.dict()},
            pretty=pretty,
            indent="  ",
            attr_prefix="at_",
            preprocessor=self.encode_preprocessor,
            encoding=self.encoding,
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
                        encoding=self.encoding,
                    )
                )
            )

    def __repr__(self):
        return f"Template. Root: {self.root.control.at_ID}"

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
