"""General Layout shortcuts"""

from copy import deepcopy
from .tosc import *
from .tosc import ElementTOSC
from .elements import Property, ControlElements
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
        if elements := source.properties.findall(f"*[{Property.Elements.KEY}='{arg}']"):
            [target.properties.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {args}")
    return True


def moveProperties(source: ElementTOSC, target: ElementTOSC, *args):
    elements = []
    if args is None:
        elements = source.properties
    for arg in args:
        if e := source.properties.findall(f"*[{Property.Elements.KEY}='{arg}']"):
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
        if elements := source.values.findall(f"*[{Property.Elements.KEY}='{arg}']"):
            [target.values.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {args}")
    return True


def moveValues(source: ElementTOSC, target: ElementTOSC, *args: str):
    elements = []
    if args is None:
        elements = source.values
    for arg in args:
        if e := source.values.findall(f"*[{Property.Elements.KEY}='{arg}']"):
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
        if elements := source.messages.findall(f"./{arg}"):
            [target.messages.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {args}")
    return True


def moveMessages(source: ElementTOSC, target: ElementTOSC, *args: str):
    elements = []
    if args is None:
        elements = source.messages
    for arg in args:
        if e := source.messages.findall(f"./{arg}"):
            elements += e
        else:
            raise ValueError(f"Failed to find all elements with {args}")

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
            f"./{ControlElements.NODE}[@type='{arg}']"
        ):
            [target.children.append(deepcopy(e)) for e in elements]
        else:
            raise ValueError(f"Failed to find all elements with {args}")
    return True


def moveChildren(source: ElementTOSC, target: ElementTOSC, *args: str):
    elements = []
    if args is None:
        elements = source.children
    for arg in args:
        if e := source.children.findall(f"./{ControlElements.NODE}[@type='{arg}']"):
            elements += e
        else:
            raise ValueError(f"Failed to find all elements with {args}")

    [target.children.append(deepcopy(e)) for e in elements]
    [source.children.remove(e) for e in elements]
    return True


""" 
ARRANGE AND LAYOUT
"""


def arrangeChildren(
    parent: ElementTOSC, rows: int, columns: int, zeroPad: bool = False
) -> bool:
    """Get n number of children and arrange them in rows and columns"""
    number = len(parent.children)
    number = rows * columns

    fw = int(parent.getPropertyParam("frame", "w").text)
    fh = int(parent.getPropertyParam("frame", "h").text)
    w, h = fw / rows, fh / columns
    N = np.asarray(range(0, number)).reshape(rows, columns)
    X = np.asarray([(N[0][:columns] * w) for i in range(rows)]).reshape(1, number)
    Y = np.repeat(N[0][:rows] * h, columns).reshape(1, number)
    XYN = np.stack((X, Y, N.reshape(1, number)), axis=2)[0]

    for x, y, n in XYN:
        if zeroPad and n >= len(parent.children):
            continue
        e = ElementTOSC(parent.children[int(n)])
        e.setFrame((x, y, w, h))

    return True


def colorChecker(color):
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
            else tuple(
                *tuple(int(color[i : i + 2], 16) / 255 for i in (0, 2, 4)),
                1,
            )
        )
    else:
        raise TypeError(f"{color} type is not a valid color.")


def layoutColumn(func):
    """Create a column of groups with a color gradient."""

    def wrapper(
        *,
        size: tuple[float] = (1, 2, 1),
        frame: tuple[float] = (0, 0, 640, 1600),
        colors: tuple[tuple] = ((0.25, 0.25, 0.25, 1.0), (0.25, 0.25, 0.25, 1.0)),
    ):
        colors = tuple(colorChecker(i) for i in colors)  # make sure is normalized

        layout = ElementTOSC(createGroup())
        layout.setFrame(frame)
        groups = [addGroupTo(layout) for i, r in enumerate(size)]
        [g.setName(f"group{str(i+1)}") for i, g in enumerate(groups)]

        H = frame[3] * (np.asarray(size) / np.sum(size))
        W = [frame[2] for i in size]
        Y = [frame[1] + np.sum(H[0 : i[0]]) for i, v in np.ndenumerate(H)]
        X = np.asarray(tuple(0 for i in size))

        F = np.asarray(((X), (Y), (W), (H))).T
        [g.setFrame(f) for f, g in zip(F, groups)]

        C = np.linspace(colors[0], colors[1], len(size))
        [g.setColor(c) for c, g in zip(C, groups)]

        func(groups)  # Do stuff to the groups

        return layout

    return wrapper


def layoutRow(func):
    """Create a row of groups with a color gradient."""

    def wrapper(
        *,
        size: tuple[float] = (1, 2, 1),
        frame: tuple[float] = (0, 0, 1600, 640),
        colors: tuple[tuple] = ((0.25, 0.25, 0.25, 1.0), (0.25, 0.25, 0.25, 1.0)),
    ):
        colors = tuple(colorChecker(i) for i in colors)  # make sure is normalized

        layout = ElementTOSC(createGroup())
        layout.setFrame(frame)
        groups = [addGroupTo(layout) for i, r in enumerate(size)]
        [g.setName(f"group{str(i+1)}") for i, g in enumerate(groups)]

        # TO DO : Optimize
        W = frame[2] * (np.asarray(size) / np.sum(size))
        H = [frame[3] for i in size]
        X = [frame[0] + np.sum(W[0 : i[0]]) for i, v in np.ndenumerate(W)]
        Y = np.asarray(tuple(0 for i in size))

        F = np.asarray(((X), (Y), (W), (H))).T
        [g.setFrame(f) for f, g in zip(F, groups)]

        C = np.linspace(colors[0], colors[1], len(size))
        [g.setColor(c) for c, g in zip(C, groups)]

        func(groups)

        return layout

    return wrapper


def layoutGrid(func):
    """Create an x*y grid of groups.

    colorStyle:
        Select a gradient style.
        0 = horizontal gradient
        1 = vetical gradient
        2 = sequential gradient 1
        3 = sequential gradient 2
        >= 4 = centered/mirrored gradient, moves position with number

    """

    def wrapper(
        *,
        size: int = (4, 4),
        frame: tuple[float] = (0, 0, 800, 1200),
        colors: tuple[tuple] = (
            (0.25, 0.25, 0.25, 1.0),
            (0.5, 0.5, 0.5, 1.0),
        ),
        colorStyle: int = 0,
    ):
        colors = tuple(colorChecker(i) for i in colors)

        layout = ElementTOSC(createGroup())
        layout.setFrame(frame)
        groups = [addGroupTo(layout) for i in range(int(size[0] * size[1]))]

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
        F = np.asarray(((X), (Y), (W), (H))).T
        [g.setFrame(f) for f, g in zip(F, groups)]

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
            raise ValueError(f"{colorStyle} is not valid.")

        [g.setColor(c) for c, g in zip(C, groups)]

        [g.setName(f"group{str(i+1)}") for i, g in enumerate(groups)]
        func(groups)

        return layout

    return wrapper
