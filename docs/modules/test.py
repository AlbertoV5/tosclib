from dataclasses import dataclass
from typing import NamedTuple
import tosclib as tosc
from tosclib import Control, Property, Value
import re
from tosclib.tosc import ControlType, ElementTOSC, PropertyType
import numpy as np


def createNumpad():

    fx, fy, fw, fh = 0, 0, 200, 300
    cr, cg, cb, ca = 0.25, 0.25, 0.25, 1.0

    grpNums = ElementTOSC.fromGroup()
    grpNums.setName("Numpad")
    grpNums.setFrame(fx, fy, fw, fh)

    groupValue = grpNums.addGroup()
    groupHide = grpNums.addGroup()
    groupSend = grpNums.addGroup()

    n = 9
    d = 3
    w = fw / d
    h = fh / d
    N = np.asarray(range(0, n)).reshape(d, d)
    X = np.asarray([(N[0] * w) for i in range(d)]).reshape(1, 9)
    Y = np.repeat(N[0] * h, d).reshape(1, 9)
    N = np.asarray([np.flip(N[i]) for i in range(d)])
    XYN = np.stack((X, Y, np.flip(N.reshape(1, 9) + 1)), axis=2)[0]

    label1 = Control.LABEL(textSize=48, background=False)
    label1.build("textSize", "background")
    print(label1.props)

    for x, y, n in XYN:
        grp, btn, lbl = grpNums.addGroup(ControlType.BUTTON, ControlType.LABEL)
        grp.setFrame(x, y, w, h)
        grp.setName(f"group{int(n)}")

        label1.frame = [0, 0, w, h]
        label1.build("frame")
        label1.injectTo(lbl)
        lbl.createValue(Value(key="text", default=f"{int(n)}"))

        btn.setFrame(0, 0, w, h)
        btn.setColor(cr, cg, cb, ca)
        btn.setScript(
            f"""
function onValueChanged(key)
    if (key == "x" and self.values.x == 1) then
        self.parent.parent.children.numvalue:notify(self.parent.name)
    end
end"""
        )

    root = tosc.createTemplate()
    root.append(grpNums.node)
    tosc.write(root, "docs/modules/test.tosc")


if __name__ == "__main__":
    createNumpad()
