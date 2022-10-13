"""Control Module"""
# Parsing
from pydantic import BaseModel, Field
from typing import Literal, TypeAlias
from uuid import UUID, uuid4

# Local
from .message import Gamepad, Osc, Midi, Local, Messages
from .value import ValueOptions
from .property import Frame, PropertyOptions


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


class Control(BaseModel):
    """Model for the Template's Control.
    The XML file labels a 'control' as 'node'.

    Access the Control's children via index notation.

    Example:
        first_child = control[0]

    https://hexler.net/touchosc/manual/editor-control
    """

    at_type: ControlType = "GROUP"
    at_ID: UUID = Field(default_factory=uuid4)
    properties: list[PropertyOptions] = Field(
        default_factory=lambda: [Frame("frame", (0, 0, 400, 400))]
    )
    values: list[ValueOptions] = Field(default_factory=lambda: [])
    messages: Messages = Field(default_factory=Messages)
    children: list["Control"] = Field(default_factory=lambda: [], repr=False)

    class Config:
        validate_assignment = True

    def __getitem__(self, item):
        return self.children[item]

    def __iter__(self):
        return iter(self.children)

    def add_controls(self, data: list["Control"], validate: bool = False) -> "Control":
        """Append all controls in given list to this control's children."""
        for d in data:
            self.children.append(d)
        return self.validate(self.dict()) if validate else self

    def add_properties(
        self, data: list[PropertyOptions], validate: bool = False
    ) -> "Control":
        """Append all properties in given list to this Control's properties."""
        for d in data:
            self.properties.append(d)
        return self.validate(self.dict()) if validate else self

    def add_values(self, data: list[ValueOptions], validate: bool = False) -> "Control":
        """Append all values in given list to this Control's values."""
        for d in data:
            self.values.append(d)
        return self.validate(self.dict()) if validate else self

    def add_midi(self, data: list[Midi], validate: bool = False) -> "Control":
        for d in data:
            self.messages.midi.append(d)
        return self.validate(self.dict()) if validate else self

    def add_osc(self, data: list[Osc], validate: bool = False) -> "Control":
        for d in data:
            self.messages.osc.append(d)
        return self.validate(self.dict()) if validate else self

    def add_local(self, data: list[Local], validate: bool = False) -> "Control":
        for d in data:
            self.messages.local.append(d)
        return self.validate(self.dict()) if validate else self

    def add_gamepad(self, data: list[Gamepad], validate: bool = False) -> "Control":
        for d in data:
            self.messages.gamepad.append(d)
        return self.validate(self.dict()) if validate else self

    def dumps(self, indent=2, exclude={"children"}, **kwargs) -> str:
        return self.json(indent=indent, exclude=exclude, **kwargs)
