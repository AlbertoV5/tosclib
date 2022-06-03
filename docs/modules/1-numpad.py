import cProfile
import pstats
import tosclib as tosc
from tosclib import Control, Value
from tosclib.tosc import ControlType, ElementTOSC

"""WORK IN PROGRESS June-2-2022"""
def createNumpad():
    """Let's start by creating a group and set basic properties"""
    root = tosc.createTemplate()
    main = ElementTOSC(root[0])
    fx, fy, fw, fh = 0, 0, 200, 400
    main.setName("Numpad")
    main.setFrame(fx, fy, fw, fh)

    """Second group to avoid having many elements in top layer"""
    grpNums = tosc.addGroup(main)
    tosc.copyProperties(main, grpNums, "frame", "name")
    deleteme = ElementTOSC(tosc.createTemplate())
    tosc.copyProperties(main, deleteme, "frame", "name")
    
    tosc.moveProperties(deleteme, main, "name", "frame")

    """Let's build the templates for the controls inside the subgroups"""
    n, rows, columns = 9, 3, 3
    w, h = fw / rows, fh / columns
    frame = [0, 0, w, h]
    color = [0.25, 0.25, 0.25, 1.0]
    
    labelTemplate = Control.Label(
        name="label", textSize=48, background=False, frame=frame
    )
    buttonTemplate = Control.Button(name="button", frame=frame, color=color)
    with open("docs/modules/button.lua", "r") as file:
        buttonTemplate.script = file.read()
    
    labelTemplate.build("name", "textSize", "background", "frame")
    buttonTemplate.build("name", "frame", "color", "script")

    """Create the actual <node> Elements. In this case using a specific sequence"""
    # fmt: off
    sequence = (7,8,9,
                4,5,6,
                1,2,3,)
    # fmt: on
    for i in sequence:
        grp, btn, lbl = tosc.addGroup(grpNums, ControlType.BUTTON, ControlType.LABEL)
        grp.setName(f"{int(i)}")
        buttonTemplate.applyTo(btn)
        labelTemplate.applyTo(lbl)
        lbl.createValue(Value(key="text", default=f"{int(i)}"))

    """Automatically position all children by row and column, 'zero-padding' optional"""
    grpNums.arrangeChildren(3, 3, True)

    """Save it as a template"""
    # tosc.write(root, "docs/modules/numpad.tosc")


if __name__ == "__main__":
    with cProfile.Profile() as pr:
        createNumpad()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="test.prof")
    