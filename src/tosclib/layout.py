"""General Layout shortcuts"""

from copy import deepcopy
from typing import Callable
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
COPY AND MOVE
"""


def copyProperties(source: ElementTOSC, target: ElementTOSC, *args: str):
    """Args can be any number of property keys"""
    if args is None:
        [target.properties.append(deepcopy(e)) for e in source.properties]
        return True
    for arg in args:
        if elements := source.properties.findall(f"*[key='{arg}']"):
            [target.properties.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {args}")
    return True


def moveProperties(source: ElementTOSC, target: ElementTOSC, *args):
    elements = []
    if args is None:
        elements = source.properties
    for arg in args:
        if e := source.properties.findall(f"*[key='{arg}']"):
            elements += e
        else:
            raise ValueError(f"Failed to find all elements with {args}")

    [target.properties.append(deepcopy(e)) for e in elements]
    [source.properties.remove(e) for e in elements]
    return True


def copyValues(source: ElementTOSC, target: ElementTOSC, *args: str):
    """Args can be any number of value keys"""
    if args is None:
        [target.values.append(deepcopy(e)) for e in source.values]
        return True
    for arg in args:
        if elements := source.values.findall(f"*[key='{arg}']"):
            [target.values.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {args}")
    return True


def moveValues(source: ElementTOSC, target: ElementTOSC, *args: str):
    elements = []
    if args is None:
        elements = source.values
    for arg in args:
        if e := source.values.findall(f"*[key='{arg}']"):
            elements += e
        else:
            raise ValueError(f"Failed to find all elements with {args}")

    [target.values.append(deepcopy(e)) for e in elements]
    [source.values.remove(e) for e in elements]
    return True


def copyMessages(source: ElementTOSC, target: ElementTOSC, *args: str):
    """Args can be ControlElements.OSC, MIDI, LOCAL, GAMEPAD"""
    if args is None:
        [target.messages.append(deepcopy(e)) for e in source.messages]
        return True
    for arg in args:
        if elements := source.messages.findall(f"./{arg.value}"):
            [target.messages.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {arg.value}")
    return True


def moveMessages(source: ElementTOSC, target: ElementTOSC, *args: str):
    elements = []
    if args is None:
        elements = source.messages
    for arg in args:
        if e := source.messages.findall(f"./{arg.value}"):
            elements += e
        else:
            raise ValueError(f"Failed to find all elements with {arg.value}")

    [target.messages.append(deepcopy(e)) for e in elements]
    [source.messages.remove(e) for e in elements]
    return True


def copyChildren(source: ElementTOSC, target: ElementTOSC, *args: str):
    """Args can be ControlType.BOX, BUTTON, etc."""
    if args is None:
        [target.children.append(deepcopy(e)) for e in source.children]
        return True
    for arg in args:
        if elements := source.children.findall(
            f"./{ControlElements.NODE.value}[@type='{arg.value}']"
        ):
            [target.children.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {arg.value}")
    return True


def moveChildren(source: ElementTOSC, target: ElementTOSC, *args: str):
    elements = []
    if args is None:
        elements = source.children
    for arg in args:
        if e := source.children.findall(
            f"./{ControlElements.NODE}[@type='{arg.value}']"
        ):
            elements += e
        else:
            raise ValueError(f"Failed to find all elements with {arg.value}")

    [target.children.append(deepcopy(e)) for e in elements]
    [source.children.remove(e) for e in elements]
    return True


"""

ARRANGE AND LAYOUT

"""


# def arrangeChildren(
#     parent: ElementTOSC, rows: int, columns: int, zeroPad: bool = False
# ) -> bool:
#     """Get n number of children and arrange them in rows and columns.

#     Args:
#         parent: Element that has the children
#         rows: how many rows
#         columns: how many columns
#         zeroPad: allows to have incomplete rows/columns of children.
#     """
#     number = len(parent.children)
#     number = rows * columns

#     fw = int(parent.getPropertyParam("frame", "w").text)
#     fh = int(parent.getPropertyParam("frame", "h").text)
#     w, h = fw / rows, fh / columns
#     N = np.asarray(range(0, number)).reshape(rows, columns)
#     X = np.asarray([(N[0][:columns] * w) for i in range(rows)]).reshape(1, number)
#     Y = np.repeat(N[0][:rows] * h, columns).reshape(1, number)
#     XYN = np.stack((X, Y, N.reshape(1, number)), axis=2)[0]

#     for x, y, n in XYN:
#         if zeroPad and n >= len(parent.children):
#             continue
#         e = ElementTOSC(parent.children[int(n)])
#         e.setFrame((x, y, w, h))

#     return True


def colorChecker(color: tuple[tuple]):
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
        g.setFrame(f)
        g.setColor(c)

    # Add extra properties to the parent, optional return
    properties: Properties = func(children)
    if properties is not None:
        [layout.createProperty(p) for p in properties]

    return layout


def layoutColumn(func):
    """Create a column of groups with a color gradient.

    Args:
        size: The size and ratio of the columns, (1,2,1) means 3 columns with 1:2:1 ratio.
        frame: Parent frame, all children adapt to it.
        colors: Tuple of two colors for linear gradient.
    """

    def wrapper(
        parent: ElementTOSC,
        controlType: ControlType,
        size: tuple = (1, 2, 1),
        colors: tuple[tuple] = ((0.25, 0.25, 0.25, 1.0), (0.25, 0.25, 0.25, 1.0)),
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


def layoutRow(func):
    """Create a row of groups with a color gradient.

    Args:
        size: The size and ratio of the rows, (1,2,1) means 3 rows with 1:2:1 ratio.
        frame: Parent frame, all children adapt to it.
        colors: Tuple of two colors for linear gradient.

    """

    def wrapper(
        parent: ElementTOSC,
        controlType: ControlType,
        size: tuple = (1, 2, 1),
        frame: tuple = (0, 0, 1600, 640),
        colors: tuple[tuple] = ((0.25, 0.25, 0.25, 1.0), (0.25, 0.25, 0.25, 1.0)),
    ):
        colors = tuple(colorChecker(i) for i in colors)  # makes sure is normalized
        frame = parent.getFrame()

        H = np.resize(frame[3], len(size))
        W = frame[2] * (np.asarray(size) / np.sum(size))
        Y = np.resize((0), len(size))
        X = np.cumsum(np.concatenate(([0], W)))[:-1]
        F = np.asarray((X, Y, W, H, X)).T
        C = np.linspace(colors[0], colors[1], len(size))
        return Layout(parent, controlType, F, C, func)

    return wrapper


def layoutGrid(func):
    """Create an x*y grid of groups.

    Args:
        size: the row x column size in tuple, ej (4,4) or (5, 3), etc
        frame: parent frame, all children adapt to it
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
        size: int = (4, 4),
        colors: tuple[tuple] = (
            (0.25, 0.25, 0.25, 1.0),
            (0.5, 0.5, 0.5, 1.0),
        ),
        colorStyle: int = 0,
    ):

        frame = parent.getFrame()
        colors = tuple(colorChecker(i) for i in colors)

        w = frame[2] / size[0]
        h = frame[3] / size[1]
        M = np.asarray(
            tuple(
                (row, column)
                for row in np.arange(stop=frame[2], step=w)
                for column in np.arange(stop=frame[3], step=h)
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
