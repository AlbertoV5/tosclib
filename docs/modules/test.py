from dataclasses import dataclass
from typing import NamedTuple
import tosclib as tosc
from tosclib import Control, Property, Value
import re
from tosclib.tosc import ControlType, ElementTOSC, PropertyType
import numpy as np

def createNumpad():
    
    fx, fy, fw, fh = 0, 0, 200, 400
    cr, cg, cb, ca = 0.25, 0.25, 0.25, 1.0
    
    group = ElementTOSC.newGroup()
    group.setName("Numpad")
    group.setFrame(fx, fy, fw, fh)
    
    groupValue = group.addGroup()
    groupHide = group.addGroup()
    groupSend = group.addGroup()
    bGroupList = []
    
    n = 9
    d = 3
    w = fw/d
    h = fh/d
    N = np.asarray(range(0,n)).reshape(d,d)
    X = np.asarray([(N[0]*w)for i in range(d)]).reshape(1, 9)
    Y = np.repeat(N[0]*h, d).reshape(1, 9)
    XYN = np.stack((X,Y,(N.reshape(1,9)+1)), axis=2)[0]

    for x,y,n in XYN:
        # print("x",x,"y",y,"n",n)
        # GROUP with args
        g, b, l = group.addGroup(ControlType.BUTTON, ControlType.LABEL)
        g.setFrame(x,y,w,h)
        g.setName(f"group{int(n)}")
        # LABEL
        l.setFrame(0,0,w,h)
        l.setColor(1,1,1,1)
        l.setBackground(False)
        l.createValue(Value(key="text", default = f"{int(n)}"))
        l.createProperty(Property(PropertyType.INTEGER, Control.LABEL.SIZE, "48"))
        # BUTTON
        b.setFrame(0,0,w,h)
        b.setColor(cr, cg, cb, ca)
        b.setScript(f"""
function onValueChanged(key)
    if (key == "x" and self.values.x == 1) then
        self.parent.parent.children.numvalue:notify(self.parent.name)
    end
end""")
        bGroupList.append(g)


    root = tosc.createTemplate()
    root.append(group.node)
    tosc.write(root, "docs/modules/test.tosc")



if __name__ == "__main__":
    createNumpad()
