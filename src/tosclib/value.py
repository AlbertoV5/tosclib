"""Value Module"""
from typing import Literal, TypeAlias
from pydantic import BaseModel


ValueDefault: TypeAlias = bool | float | int | str
ValueKey: TypeAlias = Literal["touch", "x", "y", "page", "text"]


class Value(BaseModel):
    """Model for the Control's Values.
    https://hexler.net/touchosc/manual/editor-control-values
    """

    key: ValueKey
    locked: bool
    lockedDefaultCurrent: bool
    default: ValueDefault
    defaultPull: int

    class Config:
        validate_assignment = True


class X(Value):
    key: Literal["x"] = "x"
    locked: bool = False
    lockedDefaultCurrent: bool = False
    default: float = 0
    defaultPull: int = 0

    def __init__(
        __pydantic_self__,
        key: Literal["x"] = "x",
        locked: bool = False,
        lockedDefaultCurrent: bool = False,
        default: float = 0,
        defaultPull: int = 0,
    ) -> None:
        super().__init__(
            key=key,
            locked=locked,
            lockedDefaultCurrent=lockedDefaultCurrent,
            default=default,
            defaultPull=defaultPull,
        )


class Y(Value):
    key: Literal["y"] = "y"
    locked: bool = False
    lockedDefaultCurrent: bool = False
    default: float = 0
    defaultPull: int = 0

    def __init__(
        __pydantic_self__,
        key: Literal["y"] = "y",
        locked: bool = False,
        lockedDefaultCurrent: bool = False,
        default: float = 0,
        defaultPull: int = 0,
    ) -> None:
        super().__init__(
            key=key,
            locked=locked,
            lockedDefaultCurrent=lockedDefaultCurrent,
            default=default,
            defaultPull=defaultPull,
        )


class Text(Value):
    key: Literal["text"] = "text"
    locked: bool = False
    lockedDefaultCurrent: bool = False
    default: str = ""
    defaultPull: int = 0

    def __init__(
        __pydantic_self__,
        key: Literal["text"] = "text",
        locked: bool = False,
        lockedDefaultCurrent: bool = False,
        default: str = "",
        defaultPull: int = 0,
    ) -> None:
        super().__init__(
            key=key,
            locked=locked,
            lockedDefaultCurrent=lockedDefaultCurrent,
            default=default,
            defaultPull=defaultPull,
        )


class Touch(Value):
    key: Literal["touch"] = "touch"
    locked: bool = False
    lockedDefaultCurrent: bool = False
    default: bool = False
    defaultPull: int = 0

    def __init__(
        __pydantic_self__,
        key: Literal["touch"] = "touch",
        locked: bool = False,
        lockedDefaultCurrent: bool = False,
        default: bool = False,
        defaultPull: int = 0,
    ) -> None:
        super().__init__(
            key=key,
            locked=locked,
            lockedDefaultCurrent=lockedDefaultCurrent,
            default=default,
            defaultPull=defaultPull,
        )


class Page(Value):
    key: Literal["page"] = "page"
    locked: bool = False
    lockedDefaultCurrent: bool = False
    default: int = 0
    defaultPull: int = 0

    def __init__(
        __pydantic_self__,
        key: Literal["page"] = "page",
        locked: bool = False,
        lockedDefaultCurrent: bool = False,
        default: int = 0,
        defaultPull: int = 0,
    ) -> None:
        super().__init__(
            key=key,
            locked=locked,
            lockedDefaultCurrent=lockedDefaultCurrent,
            default=default,
            defaultPull=defaultPull,
        )


ValueOptions: TypeAlias = X | Y | Touch | Text | Page
