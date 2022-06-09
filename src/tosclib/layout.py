"""
General Layout shortcuts.

Layouts are decorators that receive a parent ElementTOSC, ControlType 
for children, size and color and create a bunch of children whose 
frames align inside the parent's frame.

To define a layout, add one of the preset layouts: layoutColumn, 
layoutRow, etc.to your function and set that function to receive a 
list of ElementTOSC. Then return a list[Property] (Properties)
that you want to add to the layout.

The order is:

1. Calculate Frame and Color arrays
2. Create the children Controls and transform them.
3. Then the decorated function happens.
4. You can return a list[Property] (Properties) to apply to the layout.
5. Then the layout is returned to whoever called the decorated function.

Because your function will be executed towards the end, you can add
any number of nested layouts to the children as they will have their 
frame and color set already.

The decorated function is also a good place to add Values and Messages
to the children.

All Layouts are currently built in top > bottom, left > right order.
"""

from copy import deepcopy
from typing import Any, Callable
from .tosc import ElementTOSC
from .elements import (
    ControlElements,
    controlType,
    ControlType,
)
from .controls import (
    Properties,
)
import numpy as np


"""

ARRANGE AND LAYOUT

"""

def colorChecker(color: Any) -> tuple:
    """Allow for passing rgba in 0-255, 0-1 and hex, then convert to 0-1"""
    if isinstance(color[0], int):
        return tuple(i / 255 for i in color)
    elif isinstance(color[0], float):
        return color
    elif isinstance(color[0], str):
        color = color.replace("#", "")
        return (
            tuple(int(color[i : i + 2], 16) / 255 for i in (0, 2, 4, 6))
            if len(color) > 7
            else tuple(int(color[i : i + 2], 16) / 255 for i in (0, 2, 4)) + (1,)
        )
    else:
        raise TypeError(f"{color} type is not a valid color.")


"""

LAYOUT FUNCTIONS

"""


def Layout(
    layout: ElementTOSC,
    controlT: controlType,
    F: np.ndarray,
    C: np.ndarray,
    func: Callable[[list[ElementTOSC]], Properties],
):
    """Basic process to append multiple properties to a layout of controls"""

    children = [ElementTOSC(layout.createChild(controlT)) for i in range(F.shape[0])]
    for g, f, c in zip(children, F, C):
        g.setFrame(f.astype(int))
        g.setColor(c)

    # Add extra properties to the parent, optional return
    properties: Properties = func(children)
    if properties is not None:
        [layout.createProperty(p) for p in properties]

    return layout


def column(func):
    """Create a column of groups with a color gradient.

    Args:
        parent: The Control that becomes the layout.
        controlType: The Control type of the generated children.
        size: The size and ratio of the columns, (1,2,1) means 3 columns with 1:2:1 ratio.
        colors: Tuple of two colors for linear gradient.
    """

    def wrapper(
        parent: ElementTOSC,
        controlType: controlType,
        size: tuple = (1, 2, 1),
        colors: tuple = (
            (0.25, 0.25, 0.25, 1.0), (0.25, 0.25, 0.25, 1.0)),
    ):
        colors = tuple(colorChecker(i) for i in colors)  # makes sure is normalized
        frame = parent.getFrame()

        H = frame[3] * (np.asarray(size) / np.sum(size))
        W = [frame[2] for i in size]
        Y = np.cumsum(np.concatenate(([0], H)))[:-1]
        X = np.resize((0), len(size))
        F = np.asarray((X, Y, W, H, X)).T
        C = np.linspace(colors[0], colors[1], len(size))
        return Layout(parent, controlType, F, C, func)

    return wrapper


def row(func):
    """Create a row of groups with a color gradient.

    Args:
        parent: The Control that becomes the layout.
        controlType: The Control type of the generated children.
        size: The size and ratio of the rows, (1,2,1) means 3 rows with 1:2:1 ratio.
        colors: Tuple of two colors for linear gradient.
    """

    def wrapper(
        parent: ElementTOSC,
        controlType: ControlType,
        size: tuple = (1, 2, 1),
        frame: tuple = (0, 0, 1600, 640),
        colors: tuple | str = ((0.25, 0.25, 0.25, 1.0), (0.25, 0.25, 0.25, 1.0)),
    ):
        colors = tuple(colorChecker(i) for i in colors)  # makes sure is normalized
        frame = parent.getFrame()

        H = np.resize(frame[3], len(size)) # type: ignore
        W = frame[2] * (np.asarray(size) / np.sum(size))
        Y = np.resize((0), len(size))
        X = np.cumsum(np.concatenate(([0], W)))[:-1]
        F = np.asarray((X, Y, W, H, X)).T
        C = np.linspace(colors[0], colors[1], len(size))
        return Layout(parent, controlType, F, C, func)

    return wrapper


def grid(func):
    """Create an x*y grid of groups.

    Args:
        parent: The Control that becomes the layout.
        controlType: The Control type of the generated children.
        size: the row x column size in tuple, ej (4,4) or (5, 3), etc
        colors: tuple of two colors gradient, see colorStyle
        colorStyle:
            Select a gradient style.
            0: horizontal gradient
            1: vetical gradient
            2: sequential gradient 1
            3: sequential gradient 2
            >= 4: centered/mirrored gradient, moves position with number

    """

    def wrapper(
        parent: ElementTOSC,
        controlType: ControlType,
        size: tuple = (4, 4),
        colors: tuple=  (
            (0.25, 0.25, 0.25, 1.0),
            (0.5, 0.5, 0.5, 1.0),
        ),
        colorStyle: int = 0,
    ):

        if (frame:=parent.getFrame()) is None:
            raise ValueError(f"{parent} has no frame.")

        colors = tuple(colorChecker(i) for i in colors)

        w = frame[2] / size[0]
        h = frame[3] / size[1]
        M = np.asarray(
            tuple(
                (row, column)
                for row in np.arange(stop=frame[2], step=w) # type: ignore
                for column in np.arange(stop=frame[3], step=h) # type: ignore
            )
        ).T

        X = M[0]
        Y = M[1]
        W = np.repeat(w, X.size)
        H = np.repeat(h, Y.size)
        F = np.asarray((X, Y, W, H, X)).T

        # TO DO : Optimize
        if colorStyle == 0:  # horizontal
            C = np.linspace(colors[0], colors[1], size[0])
            C = np.repeat(C.T, size[1]).T.reshape(4, size[0] * size[1]).T
        elif colorStyle == 1:  # vertical
            C = np.linspace(colors[0], colors[1], size[1])
            C = np.asarray(np.resize(C, size[0] * C.size)).reshape(size[0] * size[1], 4)
        elif colorStyle == 2:  # sequential
            C = np.linspace(colors[0], colors[1], size[0] * size[1])
        elif colorStyle == 3:  # sequential inverted
            C = np.linspace(colors[0], colors[1], size[0] * size[1])
            C = np.asarray([C[i :: size[0]] for i in range(size[0])]).reshape(
                size[0] * size[1], 4
            )
        elif colorStyle >= 4:  # centered / mirrored
            C = np.linspace(colors[0], colors[1], size[0] * size[1])
            C = np.roll(C, colorStyle * 4)
            C[0:colorStyle] = np.flip(
                np.roll(C, (-1 - colorStyle) * 4)[0:colorStyle], axis=0
            )
        else:
            raise ValueError(f"{colorStyle} is not a valid colorStyle.")

        return Layout(parent, controlType, F, C, func)

    return wrapper
