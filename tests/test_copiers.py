import logging
import tosclib as tosc
from tosclib.properties import *
import pytest
from .profiler import profile
import inspect

def create_different_groups():
    template1 = tosc.Group(name = "template1", frame = (0,0,800,800))
    group1 = tosc.Group(name = "group2", frame = (0,0,400,400))
    template1.children.append(group1)

    template2 = tosc.Group(name = "template2")
    group2 = tosc.Group(name ="group2")
    template2.children.append(group2)
    return group1, group2

def add_properties_to_one_group(group):
    propList = []
    for func in inspect.getmembers(PropsGroup, predicate=inspect.isfunction):
        if "__" in func[0]:
            continue
        p = func[1]()
        # logging.warning(prop)
        propList.append(p)
        assert group.set_prop(p)
    return propList

def copy_properties_group_to_other_group(group1, group2):
    assert group1 is not group2
    assert tosc.copy_properties(group1, group2)

def check_copied_properties_on_other_group(group):
    propList = []
    for p in vars(group):
        if p in tosc.NOT_PROPERTIES:
            continue
        prop = getattr(group, p)
        propList.append(p)
        assert group.get_prop(p) == prop
    return propList

@profile
def test_copiers():

    group1, group2 = create_different_groups()
    propList1 = add_properties_to_one_group(group1)
    copy_properties_group_to_other_group(group1, group2)
    propList2 = check_copied_properties_on_other_group(group2)
    assert propList1.sort() == propList2.sort()
    
    # # VALUES

    # assert node.createValue(tosc.Value())
    # assert tosc.moveValues(node, node2, "touch")
    # assert node2.getValue("touch") is not None
    # assert node2.setValue(tosc.Value("touch", "1")) is not None
    # assert node2.getValueParam("touch", "locked").text == "1"

    # # COPY MESSAGES
    # assert node.createOSC() is not None
    # assert node.createMIDI() is not None
    # assert node.createLOCAL() is not None

    # assert tosc.moveMessages(node, node2, ControlElements.OSC)
    # with pytest.raises(ValueError):
    #     assert tosc.copyMessages(node, node2, ControlElements.OSC)

    # assert tosc.copyMessages(node, node2, ControlElements.MIDI)
    # assert node.removeMIDI()
    # assert node.removeLOCAL()
    # assert node2.removeOSC()

    # # COPY CHILDREN
    # controlsList = []
    # for c in ControlType:
    #     child = tosc.Node(node.createChild(c))
    #     child.setName(c.value)
    #     controlsList.append(c.value)

    # assert tosc.copyChildren(
    #     node,
    #     node2,
    #     ControlType.BOX,
    #     ControlType.BUTTON,
    #     ControlType.ENCODER,
    #     ControlType.GROUP,
    # )

    # with pytest.raises(ValueError):
    #     assert tosc.copyChildren(node2, node2, ControlType.FADER)

    # childList = []
    # for n1 in node.children:
    #     n1 = tosc.Node(n1)
    #     childList.append(n1.getPropertyValue("name").text)
    # for n2 in node2.children:
    #     n2 = tosc.Node(n2)
    #     childList.append(n2.getPropertyValue("name").text)

    # assert controlsList.sort() == childList.sort()
