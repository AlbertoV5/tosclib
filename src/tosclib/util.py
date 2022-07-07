"""Utility Functions"""
from .core import Control, NOT_PROPERTIES
from copy import deepcopy


__all__ = ["copy_properties", "copy_values", "copy_messages", "copy_children"]


def copy_properties(source: Control, target: Control) -> Control:
    """Getattr of all properties from one Control and setattr to another.

    Args:
        source (Control):
        target (Control):

    Returns:
        Control: target for chaining.
    """
    for p in vars(source):
        if p not in NOT_PROPERTIES:
            setattr(target, p, getattr(source, p))
    return target


def copy_values(source: Control, target: Control) -> Control:
    """Deep copy of values list.

    Args:
        source (Control):
        target (Control):

    Returns:
        Control: target for chaining.
    """
    target.values = deepcopy(source.values)
    return target


def copy_messages(source: Control, target: Control) -> Control:
    """Deep copy of messages list.

    Args:
        source (Control):
        target (Control):

    Returns:
        Control: target for chaining.
    """
    target.messages = deepcopy(source.messages)
    return target


def copy_children(source: Control, target: Control) -> Control:
    """Deep copy of children list.

    Args:
        source (Control):
        target (Control):

    Returns:
        Control: target for chaining.
    """
    target.children = deepcopy(source.children)
    return target
