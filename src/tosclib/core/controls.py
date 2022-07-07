"""
Hexler's Controls
"""
from typing import Type, TypeAlias
from .elements import *
from .constants import (
    NOT_PROPERTIES,
    BOX,
    BUTTON,
    ENCODER,
    FADER,
    GRID,
    GROUP,
    LABEL,
    PAGE,
    PAGER,
    RADAR,
    RADIAL,
    RADIO,
    TEXT,
    XY,
)
import uuid


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
    "CONTROL_BUILDERS",
]


class ControlBuilder:
    def __init__(
        self,
        type: ControlType,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        children: list[Control] = None,
        *args: Property,
        **kwargs: PropertyValue,
    ):
        """Control Factory.

        Not an XML Element. An Object with lists of type-hinted tuples.
        Pass either Property *args or PropertyValue **kwargs to create Property attributes.

        Args:
            type (ControlType): Required field. ControlType Literal.
            id (str, optional): Random uuid4. Defaults to None.
            values (Values, optional): Tuple of Value objects. Defaults to None.
            messages (list[Message], optional): Tuple of Message objects. Defaults to None.
            children (tuple[&quot;Node&quot;], optional): Tuple of Node objects. Defaults to None.
            args (Property): Pass any Property to create extra Property attributes.
            kwargs (PropertyValue): Pass any keywords with PropertyValues to create extra Property attributes.

        Example (using a subclass of ControlBuilder):

            class Box(ControlBuilder):
                type: ControlType = "BOX"
                ...

            box = Box(("name", "boxy)) # with args
            box = Box(name = "boxy") # with kwargs

            assert box.name == ("name", "boxy")
            assert box.type == "BOX"
        """
        self.id: str = str(uuid.uuid4()) if id is None else id
        self.type: ControlType = type
        self.values: list[Value] = [] if values is None else values
        self.messages: list[Message] = [] if messages is None else messages
        self.children: list[Control] = [] if children is None else children

        for a in args:
            setattr(self, a[0], a)

        for k in kwargs:
            setattr(self, k, (k, kwargs[k]))

    def __repr__(self):
        return f"""
Control:
    {self.type}, {self.id}
Values:
    {self.values}
Properties:
    {list(getattr(self, p) for p in vars(self) if p not in NOT_PROPERTIES)}
Messages:
    {self.messages}
Children:
    {self.children}
"""

    def get_prop(self, key: str) -> Property:
        """Get the Property of a Control"""
        p: Property = getattr(self, key)
        if p is not None:
            return p
        raise KeyError(f"{p} is not a valid Property.")

    def get_frame(self) -> tuple[int, ...]:
        return getattr(self, "frame")[1]

    def get_color(self) -> tuple[float, ...]:
        return getattr(self, "color")[1]

    def set_prop(self, prop: Property) -> Control:
        """Set the Property of a Control"""
        setattr(self, prop[0], prop)
        return self

    def set_frame(self, frame: tuple[int, ...]) -> Control:
        setattr(self, "frame", ("frame", frame))
        return self

    def set_color(self, color: tuple[float, ...]) -> Control:
        setattr(self, "color", ("color", color))
        return self


class Box(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(BOX, id, values, messages, None, **kwargs)


class Button(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(BUTTON, id, values, messages, None, **kwargs)


class Encoder(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(ENCODER, id, values, messages, None, **kwargs)


class Fader(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(FADER, id, values, messages, None, **kwargs)


class Grid(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        children: list[Control] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(GRID, id, values, messages, children, **kwargs)


class Group(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        children: list[Control] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(GROUP, id, values, messages, children, **kwargs)


class Label(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(LABEL, id, values, messages, None, **kwargs)


class Page(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        children: list[Control] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(GROUP, id, values, messages, children, **kwargs)


class Pager(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        children: list[Control] = None,
        **kwargs: PropertyValue,
    ):
        children = (
            list[Control]([Page(), Page(), Page()]) if children is None else children
        )
        super().__init__(PAGER, id, values, messages, children, **kwargs)


class Radial(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(RADIAL, id, values, messages, None, **kwargs)


class Radar(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(RADAR, id, values, messages, None, **kwargs)


class Radio(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(RADIO, id, values, messages, None, **kwargs)


class Text(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(TEXT, id, values, messages, None, **kwargs)


class Xy(ControlBuilder):
    def __init__(
        self,
        id: str = None,
        values: list[Value] = None,
        messages: list[Message] = None,
        **kwargs: PropertyValue,
    ):
        super().__init__(XY, id, values, messages, None, **kwargs)


CONTROL_BUILDERS: dict[ControlType, Type[Control]] = {
    BOX: Box,
    BUTTON: Button,
    ENCODER: Encoder,
    FADER: Fader,
    GRID: Grid,
    GROUP: Group,
    LABEL: Label,
    PAGE: Page,
    PAGER: Pager,
    RADIAL: Radial,
    RADAR: Radar,
    RADIO: Radio,
    TEXT: Text,
    XY: Xy,
}
"""Dictionary of Control Builders."""
