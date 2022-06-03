import tosclib as tosc
from tosclib import Control, Value
from tosclib.tosc import ControlType, ElementTOSC

"""WORK IN PROGRESS June-2-2022"""
def createNumpad():
    """Let's start by creating a group and set basic properties"""
    root = tosc.createTemplate()
    main = ElementTOSC(root[0])
    fx, fy, fw, fh = 0, 0, 200, 300
    main.setName("Numpad")
    main.setFrame(fx, fy, fw, fh)

    """Second group to avoid having many elements in top layer"""
    grpNums = main.addGroup()
    main.copyProperties(grpNums, False, "frame", "name")

    """Let's build the templates for the controls inside the subgroups"""
    n, r, c = 9, 3, 3
    w, h = fw / r, fh / c
    frame = [0, 0, w, h]
    color = [0.25, 0.25, 0.25, 1.0]
    
    labelTemplate = Control.LABEL(
        name="label", textSize=48, background=False, frame=frame
    )
    buttonTemplate = Control.BUTTON(name="button", frame=frame, color=color)
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
        grp, btn, lbl = grpNums.addGroup(ControlType.BUTTON, ControlType.LABEL)
        grp.setName(f"{int(i)}")
        buttonTemplate.applyTo(btn)
        labelTemplate.applyTo(lbl)
        lbl.createValue(Value(key="text", default=f"{int(i)}"))

    """Automatically position all children by row and column, 'zero-padding' optional"""
    grpNums.fitChildren(3, 3, True)

    """Save it as a template"""
    tosc.write(root, "docs/modules/numpad.tosc")


if __name__ == "__main__":
    createNumpad()
