import cProfile
import pstats
import tosclib as tosc
from tosclib import Control, Value
from tosclib.elements import LOCAL, Trigger
from tosclib.tosc import ControlType, ElementTOSC
from tosclib.layout import layoutColumn

"""WORK IN PROGRESS June-2-2022"""
""" CURRENTLY DEPRECATED FOR >0.3.0"""

@layoutColumn
def numpadLayout(groups: list[ElementTOSC]) -> ElementTOSC:
    # do stuff to the layout
    top, mid, bot = groups[0], groups[1], groups[2]


def main():

    root = tosc.createTemplate(0, 0, 400, 400)
    layout: ElementTOSC = numpadLayout(ratio=(1, 2, 1), frame=(0, 0, 400, 400))

    frame = nx, ny, nw, nh = layout.getFrame()
    numGrp = layout.children[1]

    n, rows, columns = 9, 3, 3
    w, h = nw / rows, nh / columns
    frame = (0, 0, w, h)
    color = (0.25, 0.25, 0.25, 1.0)

    labelT = Control.Label(name="label", textSize=48, background=False, frame=frame)
    buttonT = Control.Button(name="button", frame=frame, color=color)
    with open("docs/modules/button.lua", "r") as file:
        buttonT.script = file.read()

    valueGrp, valueLbl, sendGrp = tosc.addGroupTo(
        layout, ControlType.LABEL, ControlType.GROUP
    )
    valLocal = LOCAL(
        enabled="1",
        triggers=[Trigger("touch", "ANY")],
        type="NAME",
        conversion="STRING",
        value="name",
        scaleMin="0",
        scaleMax="1",
        dstType="STRING",
        dstVar="text",
        dstID=valueLbl.getID(),
    )

    labelT.build("name", "textSize", "background", "frame")
    buttonT.build("name", "frame", "color", "script")

    """Create the actual <node> Elements. In this case using a specific sequence"""
    # fmt: off
    sequence = (7,8,9,
                4,5,6,
                1,2,3,)
    # fmt: on
    for i in sequence:
        grp, btn, lbl = tosc.addGroupTo(numGrp, ControlType.BUTTON, ControlType.LABEL)
        grp.setName(f"{int(i)}")
        btn.createLOCAL(valLocal)
        [btn.createProperty(prop) for prop in buttonT.props]
        [lbl.createProperty(prop) for prop in labelT.props]
        lbl.createValue(Value(key="text", default=f"{int(i)}"))

    """Automatically position all children by row and column, 'zero-padding' optional"""
    tosc.arrangeChildren(numGrp, 3, 3, True)

    """Save it as a template"""
    tosc.write(layout, "docs/modules/numpad.tosc")


if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="test.prof")
