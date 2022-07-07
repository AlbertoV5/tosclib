""" 
TYPE GUARDS SECTION:
"""
from typing import TypeGuard

from .constants import (
    ValueType,
    TriggerType,
    PartialType,
    ConversionType,
    MidiMsgType,
    ControlType,
    VALUE_TYPES,
    TRIGGER_TYPES,
    PARTIAL_TYPES,
    CONVERSION_TYPES,
    MIDI_MESSAGE_TYPES,
    CONTROL_TYPES,
)

__all__ = [
    "is_value_type",
    "is_trigger_type",
    "is_partial_type",
    "is_conversion_type",
    "is_midi_msg_type",
    "is_control_type",
]


def is_value_type(v: str | None) -> TypeGuard[ValueType]:
    if v in VALUE_TYPES:
        return True
    return False


def is_trigger_type(v: str | None) -> TypeGuard[TriggerType]:
    if v in TRIGGER_TYPES:
        return True
    return False


def is_partial_type(v: str | None) -> TypeGuard[PartialType]:
    if v in PARTIAL_TYPES:
        return True
    return False


def is_conversion_type(v: str | None) -> TypeGuard[ConversionType]:
    if v in CONVERSION_TYPES:
        return True
    return False


def is_midi_msg_type(v: str | None) -> TypeGuard[MidiMsgType]:
    if v in MIDI_MESSAGE_TYPES:
        return True
    return False


def is_control_type(v: str | None) -> TypeGuard[ControlType]:
    if v in CONTROL_TYPES:
        return True
    return False
