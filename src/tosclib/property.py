"""Property Module"""
from typing import Literal, TypeAlias
from pydantic import BaseModel


PropertyType: TypeAlias = Literal["b", "c", "r", "f", "i", "s"]
PropertyValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | tuple[float, float, float, float]
    | tuple[int, int, int, int]
)


class Property(BaseModel):
    """Model for the Control's Property.
    https://hexler.net/touchosc/manual/editor-control-properties
    """

    at_type: PropertyType
    key: str
    value: PropertyValue

    def __init__(
        __pydantic_self__, at_type: PropertyType, key: str, value: PropertyValue
    ) -> None:
        """Enforces types based on self.at_type property.

        Args:
            at_type: PropertyType
            key: str
            value: PropertyValue
        """
        super().__init__(at_type=at_type, key=key, value=value)
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

    def set(self, value: PropertyValue) -> "Property":
        """Set value and return self"""
        self.value = value
        return self


class Boolean(Property):
    at_type: Literal["b"] = "b"
    key: str
    value: bool

    def __init__(
        __pydantic_self__, key: str, value: bool, at_type: Literal["b"] = "b"
    ) -> None:
        super().__init__(at_type=at_type, key=key, value=value)


class Integer(Property):
    at_type: Literal["i"] = "i"
    key: str
    value: int

    def __init__(
        __pydantic_self__, key: str, value: int, at_type: Literal["i"] = "i"
    ) -> None:
        super().__init__(at_type=at_type, key=key, value=value)


class Float(Property):
    at_type: Literal["f"] = "f"
    key: str
    value: float

    def __init__(
        __pydantic_self__, key: str, value: float, at_type: Literal["f"] = "f"
    ) -> None:
        super().__init__(at_type=at_type, key=key, value=value)


class String(Property):
    at_type: Literal["s"] = "s"
    key: str
    value: str

    def __init__(
        __pydantic_self__, key: str, value: str, at_type: Literal["s"] = "s"
    ) -> None:
        super().__init__(at_type=at_type, key=key, value=value)


class Frame(Property):
    at_type: Literal["r"] = "r"
    key: str
    value: tuple[int, int, int, int]

    def __init__(
        __pydantic_self__,
        key: str,
        value: tuple[int, int, int, int],
        at_type: Literal["r"] = "r",
    ) -> None:
        super().__init__(at_type=at_type, key=key, value=value)


class Color(Property):
    at_type: Literal["c"] = "c"
    key: str
    value: tuple[float, float, float, float]

    def __init__(
        __pydantic_self__,
        key: str,
        value: tuple[float, float, float, float],
        at_type: Literal["c"] = "c",
    ) -> None:
        super().__init__(at_type=at_type, key=key, value=value)


PropertyOptions: TypeAlias = Boolean | Integer | Float | String | Frame | Color
