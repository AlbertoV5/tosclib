"""Control Module"""
from typing import Literal, TypeAlias
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

from .message import Gamepad, Osc, Midi, Local, Messages
from .value import Value, ValueOptions
from .property import Property, Frame, PropertyValue, PropertyOptions


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

    def add_controls(self, controls: list["Control"]) -> "Control":
        """Append all controls in given list to this control's children."""
        for control in controls:
            if not isinstance(control, Control):
                raise TypeError(f"{control} is not a valid Control")
            self.children.append(control)
        return self

    def add_property(self, property: PropertyOptions) -> "Control":
        if not isinstance(property, Property):
            raise TypeError(f"{property} is not a valid Property")
        self.properties.append(property)
        return self

    def add_value(self, value: ValueOptions) -> "Control":
        if not isinstance(value, Value):
            raise TypeError(f"{value} is not a valid Value")
        self.values.append(value)
        return self

    def add_osc(self, osc: Osc) -> "Control":
        if not isinstance(osc, Osc):
            raise TypeError(f"{osc} is not a valid Osc")
        self.messages.osc.append(osc)
        return self

    def add_midi(self, midi: Midi) -> "Control":
        if not isinstance(midi, Midi):
            raise TypeError(f"{midi} is not a valid Midi")
        self.messages.midi.append(midi)
        return self

    def add_local(self, local: Local) -> "Control":
        if not isinstance(local, Local):
            raise TypeError(f"{local} is not a valid Local")
        self.messages.local.append(local)
        return self

    def add_gamepad(self, gamepad: Gamepad) -> "Control":
        if not isinstance(gamepad, Gamepad):
            raise TypeError(f"{gamepad} is not a valid Local")
        self.messages.gamepad.append(gamepad)
        return self

    def dumps(self, indent=2, exclude={"children"}, **kwargs):
        return self.json(indent=indent, exclude=exclude, **kwargs)

    def set_prop(self, key: str, value: PropertyValue) -> "Control":
        self.properties = [p.set(value) if p.key == key else p for p in self.properties]
        return self
