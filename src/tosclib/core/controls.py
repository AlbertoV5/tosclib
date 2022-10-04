"""
Hexler's Controls
"""
from dataclasses import dataclass, field
from typing import ClassVar, Type
from .guards import is_color, is_frame
from .elements import (
    ControlType,
    Value,
    Message,
    Property,
    Control,
    PropertyValue,
    ValueKey,
)
from .constants import CONTROL_TYPES
from uuid import UUID, uuid4


__all__ = [
    "Box",
    "Button",
    "Encoder",
    "Fader",
    "Grid",
    "Group",
    "Label",
    "Page",
    "Pager",
    "Radial",
    "Radar",
    "Radio",
    "Text",
    "Xy",
    "CONTROLS",
]


@dataclass
class ControlBuilder:
    type: ClassVar[ControlType]
    id: str = field(default_factory=lambda: str(uuid4()))
    props: dict[str, PropertyValue] = field(default_factory=lambda: {})
    values: dict[ValueKey, Value] = field(default_factory=lambda: {})
    messages: list[Message] = field(default_factory=lambda: [])
    children: list[Control] = field(default_factory=lambda: [])

    def set(self, key: str, value: PropertyValue) -> Control:
        self.props[key] = value
        return self

    def get(self, key: str) -> PropertyValue:
        return self.props[key]

    def get_frame(self) -> tuple[int, ...]:
        frame = self.props["frame"]
        if not is_frame(frame):
            raise ValueError(f"{self} has no valid frame.")
        return frame

    def get_color(self) -> tuple[float, ...]:
        color = self.props["color"]
        if not is_color(color):
            raise ValueError(f"{self} has no valid color.")
        return color

    def set_frame(self, frame: tuple[int, ...]) -> "Control":
        self.props["frame"] = frame
        return self

    def set_color(self, color: tuple[float, ...]) -> "Control":
        self.props["frame"] = color
        return self


def is_ctrl(v: Control):
    return v


@dataclass
class Box(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.BOX


@dataclass
class Button(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.BUTTON


@dataclass
class Encoder(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.ENCODER


@dataclass
class Fader(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.FADER


@dataclass
class Grid(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.GRID
    children: list[Control] = field(default_factory=lambda: [])


@dataclass
class Group(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.GROUP
    children: list[Control] = field(default_factory=lambda: [])


@dataclass
class Label(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.LABEL


@dataclass
class Page(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.GROUP


@dataclass
class Pager(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.PAGER
    children: list[Control] = field(default_factory=lambda: [Page(), Page(), Page()])


@dataclass
class Radial(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.RADIAL


@dataclass
class Radar(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.RADAR


@dataclass
class Radio(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.RADIO


@dataclass
class Text(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.TEXT


@dataclass
class Xy(ControlBuilder):
    type: ClassVar[ControlType] = CONTROL_TYPES.XY


CONTROLS: dict[ControlType, Type[Control]] = {
    CONTROL_TYPES.BOX: Box,
    CONTROL_TYPES.BUTTON: Button,
    CONTROL_TYPES.ENCODER: Encoder,
    CONTROL_TYPES.FADER: Fader,
    CONTROL_TYPES.GRID: Grid,
    CONTROL_TYPES.GROUP: Group,
    CONTROL_TYPES.LABEL: Label,
    CONTROL_TYPES.PAGE: Page,
    CONTROL_TYPES.PAGER: Pager,
    CONTROL_TYPES.RADIAL: Radial,
    CONTROL_TYPES.RADAR: Radar,
    CONTROL_TYPES.RADIO: Radio,
    CONTROL_TYPES.TEXT: Text,
    CONTROL_TYPES.XY: Xy,
}
"""Dictionary of Control Builders."""
