"""General Layout shortcuts"""

from copy import deepcopy
import math
from .tosc import *
from .tosc import ElementTOSC
from .elements import Property, ControlElements
from .controls import Control
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


def layoutColumn(func):
    """Create a column of groups with a color gradient."""

    def wrapper(
        *,
        size: tuple[float] = (1, 2, 1),
        frame: tuple[float] = (0, 0, 640, 1600),
        gradient: tuple[tuple] = ((0.25, 0.25, 0.25, 1.0), (0.25, 0.25, 0.25, 1.0)),
    ):

        layout = ElementTOSC(createGroup())
        layout.setFrame(frame)
        groups = [addGroupTo(layout) for i, r in enumerate(size)]
        [g.setName(f"group{str(i+1)}") for i, g in enumerate(groups)]

        H = frame[3] * (np.asarray(size) / np.sum(size))
        W = [frame[2] for i in size]
        Y = [frame[1] + np.sum(H[0 : i[0]]) for i, v in np.ndenumerate(H)]
        X = [frame[0] for i in size]

        F = np.asarray(((X), (Y), (W), (H))).T
        [g.setFrame(f) for f, g in zip(F, groups)]

        C = np.linspace(gradient[0], gradient[1], len(size))
        [g.setColor(c) for c, g in zip(C, groups)]

        func(groups)  # Add elements to the groups

        return layout

    return wrapper


def layoutGrid(func):
    """Create a a:b grid of equal size groups"""
    def wrapper(
        *,
        size: int = (4, 4),
        frame: tuple[float] = (0, 0, 800, 1200),
        gradient: tuple[tuple] = (
            (0.25, 0.25, 0.25, 1.0),
            (1.0, 0.5, 0.5, 1.0),
            (0.5, 0.5, 1.0, 1.0),
        ),
        gradientStyle: int = 0,
    ):
        """TO DO: Add gradient and gradient style"""

        layout = ElementTOSC(createGroup())
        layout.setFrame(frame)
        groups = [addGroupTo(layout) for i in range(int(size[0] * size[1]))]
        [g.setName(f"group{str(i+1)}") for i, g in enumerate(groups)]

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

        CX = np.linspace(gradient[0], gradient[1], size[0])
        CY = np.linspace(gradient[0], gradient[2], size[1])
        C = (
            np.asarray(tuple(0.5 * (row + column) for row in CY for column in CX))
            .T.reshape(4, int(size[0]*size[1]))
            .T
        )
        [g.setColor(c) for c, g in zip(C, groups)]

        func(groups)  # Add elements to the groups

        return layout

    return wrapper
