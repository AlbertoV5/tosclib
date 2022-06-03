from tosclib import tosc
from tosclib.tosc import OSC, ControlType, Partial, Trigger, Value
from tosclib.tosc import Control
import sys
import xml.etree.ElementTree as ET
import time


def test_nested():

    root = tosc.createTemplate()
    parent = tosc.ElementTOSC(root[0])

    group = tosc.ElementTOSC(parent.createChild(ControlType.GROUP))
    msg = OSC(
        arguments=[
            Partial(),
            Partial("PROPERTY", "parent.name"),
            Partial(),
            Partial("PROPERTY", "name"),
        ]
    )

    lim = 8
    for i in range(lim):
        button = tosc.ElementTOSC(group.createChild(ControlType.BUTTON))
        assert button.setName(f"button{i}")
        assert button.setFrame(i * 100, 0, 100, 50)
        assert button.setColor(1 - i / lim, 0, lim, 1)
        assert button.createValue(Value(key="x"))
        assert button.createOSC(msg)
        assert button.isControlType(ControlType.BUTTON)

    for i in range(lim):
        assert group.findChildByName(f"button{i}")

    buttonBad = group.createChild(ControlType.BUTTON)
    ET.SubElement(buttonBad, "name").text = "buttonBad"
    assert group.findChildByName("buttonBad") is None

    buttonBetter = tosc.ElementTOSC(buttonBad)
    assert tosc.copyProperties(button, buttonBetter)
    assert tosc.copyValues(button, buttonBetter)
    assert tosc.copyMessages(button, buttonBetter)

    group2 = tosc.ElementTOSC(parent.createChild(ControlType.GROUP))
    assert tosc.copyChildren(group, group2)
    assert group2.setControlType(ControlType.GRID)

    for child in group.children:
        child = tosc.ElementTOSC(child)
        child.setBackground(False)
        child.setLocked(True)
        child.setVisible(False)
        child.setOutline(True)
        child.setInteractive(False)
        child.setScript(
            """
function init()
    self.values.x = 1
end
"""
        )
