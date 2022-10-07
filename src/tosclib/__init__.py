"""
tosclib

Modules:

    template:
    control:
    message:
    value:
    property:
"""
# from .tosclib import *
from .template import Root, Template
from .control import Control, ControlType
from .message import (
    Osc,
    Midi,
    Local,
    Trigger,
    Partial,
    MidiValue,
    MidiMessage,
    MessageDirectory,
    MidiType,
    SourceType,
    Conversion,
    TriggerCondition,
)
from .value import Value, X, Y, Text, Touch, Page, ValueDefault, ValueKey, ValueOptions
from .property import Property, PropertyType, PropertyValue, PropertyOptions

__version__ = "1.0.0"
