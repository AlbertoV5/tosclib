"""provide layout decorators"""
import tosclib as tosc
from tosclib import layout


@layout.row
def layout3(children: list[tosc.Control]):
    return (
        tosc.property("outline", False),
        tosc.property("tag", "row"),
    )


@layout.column
def layout2(children: list[tosc.Control]):
    return (tosc.property("lay2", False), tosc.property("outline", False))


@layout.grid
def mainLayout(children: list[tosc.Control]):

    layout2(children[4], "BUTTON", size=(1, 1, 1, 1), colors=bgColor)
    layout3(children[6], "FADER", size=(2, 2), colors=bgColor)

    return (tosc.property("name", "lay1"),)


# GLOBALS
bgColor = ("#CE6A85", "#5C374C")


def test_layout():

    frame = (0, 0, 1600, 1600)
    root = tosc.createTemplate(frame=frame)
    group = tosc.Group(root[0], props={"frame": frame})
    assert mainLayout(group, "GROUP", (3, 3), ("#CE6A85", "#5C374C"))
    assert tosc.write(root, "tests/output/test_layout.tosc")
