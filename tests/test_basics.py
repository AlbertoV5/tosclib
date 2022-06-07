import tosclib as tosc
from .profiler import profile
from tosclib import Value, Partial, ControlType, OSC


@profile
def test_basics():
    """Misc tests"""
    root = tosc.createTemplate()
    element = tosc.ElementTOSC(root[0])

    element.setName("Craig")
    tag = "Scottish"
    element.setTag(tag)
    element.createValue(Value())

    element.showValue("touch")
    element.setValue(Value("touch", "1", "1", "true", "1"))

    element.createOSC(
        message=tosc.OSC(
            "0",
            "0",
            "0",
            "1",
            "00001",
            [tosc.Trigger()],
            [tosc.Partial(), tosc.Partial()],
            [Partial(), Partial()],
        )
    )

    element.setColor((1, 0, 0, 1))
    element.setFrame((0, 0, 1, 1))

    count = 0
    for i in dir(tosc.ElementTOSC):
        if "__" not in i:
            count += 1

    tag2 = tosc.pullValueFromKey2(root, "name", "Craig", "tag")

    assert tag == tag2

    """NESTED"""

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
        assert button.setName(f"button{i}") is not None
        assert button.setFrame((i * 100, 0, 100, 50)) is not None
        assert button.setColor((1 - i / lim, 0, lim, 1)) is not None
        assert button.createValue(Value(key="x")) is not None
        assert button.createOSC(msg) is not None
        assert button.isControlType(ControlType.BUTTON)

    for i in range(lim):
        assert group.findChildByName(f"button{i}") is not None

    buttonBad = group.createChild(ControlType.BUTTON)
    buttonBad.append(tosc.testFromString("<name>buttonBad</name>"))
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

    return "tests/test_basics.prof"
