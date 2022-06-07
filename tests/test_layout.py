from typing import List
from tosclib.elements import ControlType, Property
from tosclib.tosc import ElementTOSC, createTemplate, write
from tosclib.layout import layoutGrid, layoutRow, layoutColumn
from .profiler import profile
from logging import debug
import inspect

# from memory_profiler import profile

"""
Layouts are decorator functions that receive size, frame, color, etc
and return a Group Control that holds n number of groups.

To define a layout, add one of the preset layouts: layoutColumn, layoutRow, etc.
to your function and set that function to receive a layout ElementTOSC and
return any number of Property objects, which will be added to all the 
children Controls of the layout GROUP.

The reason for this configuration is so the process of appending properties
to all subgroups is only done in one iteration. 
This includes r,g,b,a and x,y,w,h params of color and frame respectively.

Then on your own function you can modify the top GROUP (refered to as layout)
to have any other properties you want like name, tag, script, etc.

In order to add children, messages or values to the children controls of layout
you will need to do your own iterations wherever you want in the code. 

Just remember that the frame, color and your own properties are set after the
return statement of the decorated function.
"""


@layoutRow
def lay2b(children:List[ElementTOSC]):
    return (
        Property.outline(False),
        Property.tag("row"),)


@layoutColumn
def lay2(children:List[ElementTOSC]):
    return (
        Property.name("lay2"), 
        Property.outline(False),)


@layoutGrid
def lay1(children:List[ElementTOSC]):
    """Layout
    
    Args:
        children: This receives the children list after frame, color processing

    Returns:
        args: you can return a list of properties to apply to the parent
    """

    # Create nested layouts
    lay2(children[4], ControlType.BUTTON, size = (1,1,1,1), colors = bgColor)
    lay2b(children[6], ControlType.FADER, size=(2,2), colors=bgColor)

    return (Property.name("lay1"),)


# GLOBALS
bgColor = ("#CE6A85", "#5C374C")


@profile
def test_layout():

    # TO DO: Expand layout tests!
    frame = (0, 0, 1600, 1600)

    root = createTemplate(frame=frame)
    node = ElementTOSC(root[0])
    
    lay1(node, ControlType.GROUP, (3,3), ("#CE6A85", "#5C374C"))
    
    # assert isinstance(rootosc, ElementTOSC)
    # assert isinstance(columnLayout, ElementTOSC)
    # assert isinstance(gridLayout, ElementTOSC)
    # assert isinstance(rowLayout, ElementTOSC)
    # assert node.append(gridLayout)
    # assert node.append(columnLayout)
    # assert node.append(rowLayout)
    assert write(root, "tests/test_layout.tosc")
