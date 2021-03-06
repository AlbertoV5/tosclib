from typing import List
from tosclib.elements import ControlType, Property, PropertyFactory
from tosclib.tosc import ElementTOSC, createTemplate, write
from tosclib import layout
from .profiler import profile
from logging import debug
import inspect

# from memory_profiler import profile


@layout.row
def layout3(children:list[ElementTOSC]):
    return (
        PropertyFactory.outline(False),
        PropertyFactory.tag("row"),)


@layout.column
def layout2(children:list[ElementTOSC]):
    return (
        PropertyFactory.name("lay2"), 
        PropertyFactory.outline(False),)


@layout.grid
def mainLayout(children:list[ElementTOSC]):
    """Decorator receives ElementTOSC, ControlType, size, colors and colorStyle"""

    # Create nested layouts
    layout2(children[4], ControlType.BUTTON, size = (1,1,1,1), colors = bgColor)
    layout3(children[6], ControlType.FADER, size=(2,2), colors=bgColor)

    return (PropertyFactory.name("lay1"),)


# GLOBALS
bgColor = ("#CE6A85", "#5C374C")


@profile
def test_layout():
    
    frame = (0, 0, 1600, 1600)

    root = createTemplate(frame=frame)
    node = ElementTOSC(root[0])
    
    assert mainLayout(node, ControlType.GROUP, (3,3), ("#CE6A85", "#5C374C")) is node
    assert write(root, "tests/test_layout.tosc")
