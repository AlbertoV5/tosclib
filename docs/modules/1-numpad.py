import cProfile
import pstats
import tosclib as tosc
from tosclib import Control, Value
from tosclib.elements import LOCAL, Trigger
from tosclib.tosc import ControlType, ElementTOSC

"""WORK IN PROGRESS June-2-2022"""

def layout():
    """Let's start by creating a group and set basic properties"""
    root = tosc.createTemplate()
    main = ElementTOSC(root[0])
    
    main.setName("Numpad")
    main.setFrame(0, 0, 200, 400)

    """Second group to place numbers in"""
    numGrp, topGrp, botGrp = (tosc.addGroup(main) for i in range(3))

    numGrp.setName("Numbers")
    numGrp.setFrame(main.getX, main.getH*0.2, main.getW, main.getH*0.8)
    
    topGrp.setName("DisplaySend")
    botGrp.setName("ClrZeroDel")
    


def createNumpad():
    """Let's start by creating a group and set basic properties"""
    root = tosc.createTemplate()
    main = ElementTOSC(root[0])
    fx, fy, fw, fh = 0, 0, 200, 400
    main.setName("Numpad")
    main.setFrame(fx, fy, fw, fh)

    """Second group to place numbers in"""
    numGrp = tosc.addGroup(main)
    numGrp.setName("Numbers")
    nx, ny, nw, nh = 0, 0, 200, 300
    numGrp.setFrame(nx, ny, nw, nh)

    """Let's build the templates for the controls inside the subgroups"""
    n, rows, columns = 9, 3, 3
    w, h = nw / rows, nh / columns
    frame = [0, 0, w, h]
    color = [0.25, 0.25, 0.25, 1.0]

    labelT = Control.Label(name="label", textSize=48, background=False, frame=frame)
    buttonT = Control.Button(name="button", frame=frame, color=color)
    with open("docs/modules/button.lua", "r") as file:
        buttonT.script = file.read()

    valueGrp, valueLbl, sendGrp = tosc.addGroup(main, ControlType.LABEL, ControlType.GROUP)
    valLocal = LOCAL(
        enabled = "1",
        triggers = [Trigger("touch", "ANY")],
        type = "NAME",
        conversion = "STRING",
        value = "name",
        scaleMin = "0",
        scaleMax = "1",
        dstType = "STRING",
        dstVar = "text",
        dstID = valueLbl.getID(),
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
        grp, btn, lbl = tosc.addGroup(numGrp, ControlType.BUTTON, ControlType.LABEL)
        grp.setName(f"{int(i)}")
        btn.createLOCAL(valLocal)
        [btn.createProperty(prop) for prop in buttonT.props]
        [lbl.createProperty(prop) for prop in labelT.props]
        lbl.createValue(Value(key="text", default=f"{int(i)}"))

    """Automatically position all children by row and column, 'zero-padding' optional"""
    tosc.arrangeChildren(numGrp, 3, 3, True)

    """Save it as a template"""
    tosc.write(root, "docs/modules/numpad.tosc")


if __name__ == "__main__":
    with cProfile.Profile() as pr:
        createNumpad()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="test.prof")
