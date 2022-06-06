import unittest
from tosclib.elements import ControlType, Property
from tosclib.controls import Control
from tosclib.tosc import ElementTOSC, createTemplate, write
from tosclib.layout import layoutGrid, layoutRow, layoutColumn
from .profiler import profile
from logging import debug

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


@layoutColumn
def columns(layout: ElementTOSC):
    layout.setName("Column")
    return ControlType.BUTTON, (
        Property("b", "outline", "0"),
        Property("s", "tag", "col"),
    )


@layoutRow
def row(layout: ElementTOSC):
    layout.setName("Row")
    return ControlType.FADER, (
        Property("b", "outline", "0"),
        Property("s", "tag", "row"),
    )


@layoutGrid
def grid(layout: ElementTOSC):
    layout.setName("Grid")
    return ControlType.XY, (
        Property("b", "outline", "0"),
        Property("s", "tag", "grid"),
    )


@profile
def test_layout():

    # TO DO: Expand layout tests!
    frame = (0, 0, 1600, 1600)

    root = createTemplate(frame=frame)
    rootosc = ElementTOSC(root[0])

    columnLayout: ElementTOSC = columns(
        size=tuple(1 for i in range(4)),
        frame=(0, 0, 400, 1200),
        colors=((0.8, 0.8, 0.8, 1.0), (0.2, 0.2, 0.2, 1.0)),
    )

    rowLayout: ElementTOSC = row(
        frame=(0, 1200, 1600, 400), colors=("#3E8989FF", "#564D65FF")
    )

    gridLayout: ElementTOSC = grid(
        frame=(400, 0, 1200, 1200),
        size=(5, 3),
        colors=("#3E8989FF", "#564D65FF"),
        colorStyle=0,
    )

    assert isinstance(rootosc, ElementTOSC)
    assert isinstance(columnLayout, ElementTOSC)
    assert isinstance(gridLayout, ElementTOSC)
    assert isinstance(rowLayout, ElementTOSC)
    assert rootosc.append(gridLayout)
    assert rootosc.append(columnLayout)
    assert rootosc.append(rowLayout)
    assert write(root, "tests/test_layout.tosc")
