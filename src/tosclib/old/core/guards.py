""" 
TYPE GUARDS SECTION:
"""
from typing import TypeGuard

from .elements import (
    PropertyValue,
    TriggerType,
    PartialType,
    ConversionType,
    MidiMsgType,
    ValueKey,
    ControlType,
)

from .constants import (
    VALUE_KEYS,
    TRIGGER_TYPES,
    PARTIAL_TYPES,
    CONVERSION_TYPES,
    MIDI_MESSAGE_TYPES,
    CONTROL_TYPES,
)

__all__ = [
    "eval_bool",
    "is_value_key",
    "is_trigger_type",
    "is_partial_type",
    "is_conversion_type",
    "is_midi_msg_type",
    "is_control_type",
]


def eval_bool(v: str | None) -> bool:
    return True if v == "1" or v == "true" else False


def is_frame(v: PropertyValue) -> TypeGuard[tuple[int, ...]]:
    if isinstance(v, tuple):
        return all(isinstance(x, int) for x in v)
    return False


def is_color(v: PropertyValue) -> TypeGuard[tuple[float, ...]]:
    if isinstance(v, tuple):
        return all(isinstance(x, float) for x in v)
    return False


def is_value_key(v: str | None) -> TypeGuard[ValueKey]:
    assert v in VALUE_KEYS
    return True


def is_trigger_type(v: str | None) -> TypeGuard[TriggerType]:
    assert v in TRIGGER_TYPES
    return True


def is_partial_type(v: str | None) -> TypeGuard[PartialType]:
    assert v in PARTIAL_TYPES
    return True


def is_conversion_type(v: str | None) -> TypeGuard[ConversionType]:
    assert v in CONVERSION_TYPES
    return True


def is_midi_msg_type(v: str | None) -> TypeGuard[MidiMsgType]:
    assert v in MIDI_MESSAGE_TYPES
    return True


def is_control_type(v: str | None) -> TypeGuard[ControlType]:
    assert v in CONTROL_TYPES
    return True
