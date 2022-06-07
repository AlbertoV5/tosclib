from typing import List
from tosclib.elements import ControlType, Property, PropertyFactory
from tosclib.tosc import ElementTOSC, createTemplate, write
from tosclib.layout import layoutGrid, layoutRow, layoutColumn
from .profiler import profile
from logging import debug
import inspect

# from memory_profiler import profile

"""
Layouts are decorators that receive a parent ElementTOSC, ControlType for children, 
size and color and append a bunch of children whose frames and color follow the
type of layout as well as size and colors specified.

To define a layout, add one of the preset layouts: layoutColumn, layoutRow, etc.
to your function and set that function to receive a list of ElementTOSC.
Then return any number of Property objects that you want to add to the parent
ElementTOSC (the parent ElementTOSC will be renamed as layout).

The order of the function is:

1. Obtain the frame of the parent ElementTOSC.
2. Check the size and colors and calculate arrays for Frame and Color.
3. Create a bunch of children Controls and set their properties to the array.
4. Then the decorated function happens.
5. Finally apply any Properties from the func(children) to the parent ElementTOSC.

Because your function will be executed towards the end, you can add any number of 
nested layouts to the children as they will have their frame and color set already.

You can also use the space in your function to add any Messages, Values, etc. to
the children Elements.

"""


@layoutRow
def layout3(children:list[ElementTOSC]):
    return (
        PropertyFactory.outline(False),
        PropertyFactory.tag("row"),)


@layoutColumn
def layout2(children:list[ElementTOSC]):
    return (
        PropertyFactory.name("lay2"), 
        PropertyFactory.outline(False),)


@layoutGrid
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
