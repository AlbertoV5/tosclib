"""
tosclib
"""
# from .tosclib import *
from .template import Root, Template
from .control import Control, ControlType
from .message import (
    Osc,
    Midi,
    Local,
    Gamepad,
    Trigger,
    Partial,
    MidiValue,
    MidiMessage,
    MidiType,
    SourceType,
    Conversion,
    TriggerCondition,
    GamepadInput,
)
from .value import Value, X, Y, Text, Touch, Page, ValueDefault, ValueKey, ValueOptions
from .property import Property, PropertyType, PropertyValue, PropertyOptions

__version__ = "1.0.0"
