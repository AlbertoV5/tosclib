import tosclib as tosc
import pytest
from tosclib.tosc import ControlElements, ControlType
import time


def timer(func):
    def wrapper():
        start = time.process_time()
        for i in range(1000):
            func()
        end = time.process_time()
        print("-", end - start)

    return wrapper


@timer
def test_copiers():

    root = tosc.createTemplate()
    node = tosc.ElementTOSC(root[0])

    root2 = tosc.createTemplate()
    node2 = tosc.ElementTOSC(root2[0])

    # COPY PROPERTIES
    assert node.setName("node1")
    assert node2.setName("node2")
    assert node2.setFrame(0, 0, 100, 100)
    assert node2.setColor(1, 0, 0, 1)

    propList = [p.tag for p in node2.properties]
    assert node2.copyProperties(node, True, "frame", "color")
    assert node.getProperty("frame")
    assert node.getProperty("color")
    propListCopied = [p.tag for p in node.properties]
    assert propList.sort() == propListCopied.sort()

    # VALUES

    assert node.createValue(tosc.Value())
    assert node.copyValues(node2, True, "touch")
    assert node2.getValue("touch")
    assert node2.setValue(tosc.Value("touch", "1"))
    assert node2.getValueParam("touch", "locked").text == "1"

    # COPY MESSAGES
    assert node.createOSC()
    assert node.createMIDI()
    assert node.createLOCAL()

    assert node.copyMessages(node2, True, ControlElements.OSC)
    with pytest.raises(ValueError):
        assert node.copyMessages(node2, False, ControlElements.OSC)

    assert node.copyMessages(node2, False, ControlElements.MIDI)
    assert node.removeMIDI()
    assert node.removeLOCAL()
    assert node2.removeOSC()

    # COPY CHILDREN
    controlsList = []
    for var in vars(ControlType):
        if not "_" in var:
            child = tosc.ElementTOSC(node.createChild(var))
            child.setName(var.lower())
            controlsList.append(var.lower())

    assert node.copyChildren(
        node2,
        False,
        ControlType.BOX,
        ControlType.BUTTON,
        ControlType.ENCODER,
        ControlType.GROUP,
    )

    with pytest.raises(ValueError):
        assert node2.copyChildren(node2, False, ControlType.FADER)

    childList = []
    for n1 in node.children:
        n1 = tosc.ElementTOSC(n1)
        childList.append(n1.getPropertyValue("name").text)
    for n2 in node2.children:
        n2 = tosc.ElementTOSC(n2)
        childList.append(n2.getPropertyValue("name").text)

    assert controlsList.sort() == childList.sort()
